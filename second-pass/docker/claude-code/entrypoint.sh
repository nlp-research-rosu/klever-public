#!/usr/bin/env bash
# Run ONE headless Claude Code session, confined to /work (the mounted task dir),
# under a wall-clock timeout. Records duration, exit code, and the container's
# peak memory usage to /work/metrics.json; saves the session's stdout/stderr to
# /work/claude-output.json and /work/claude-stderr.log.
set -uo pipefail

MODEL="${MODEL:-opus}"                                   # opus (=4.8) | fable (=5) | full id
EFFORT="${EFFORT:-xhigh}"                                # low | medium | high | xhigh | max
PERMISSION_MODE="${PERMISSION_MODE:-bypassPermissions}"  # container is the sandbox
OUTPUT_FORMAT="${OUTPUT_FORMAT:-json}"                   # json gives cost/usage records
TIMEOUT_S="${TIMEOUT_S:-3600}"                           # hard per-problem wall clock

# Seed an isolated, ephemeral config dir from the read-only mounted OAuth token.
# Each container gets its OWN config (parallel-safe); nothing is written back to
# the host. Skipped when using ANTHROPIC_API_KEY (no /auth mount).
CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
mkdir -p "$CFG"
if [[ -f /auth/.credentials.json && ! -f "$CFG/.credentials.json" ]]; then
  cp /auth/.credentials.json "$CFG/.credentials.json"
  chmod 600 "$CFG/.credentials.json"
fi

# Kit condition (mirrors the codex runner): install the kit skills into the
# ephemeral config's skills folder so Claude Code discovers them natively.
# Kit runs drop --safe-mode because it disables skills; the ephemeral config
# contains ONLY the seeded kit, so the profile stays otherwise clean.
SAFE_FLAG="--safe-mode"
if [[ "${KIT:-0}" == "1" && -d /kit-skills ]]; then
  mkdir -p "$CFG/skills"
  cp -r /kit-skills/. "$CFG/skills/"
  SAFE_FLAG=""
fi

# Resolve the prompt: container args  >  $PROMPT  >  /work/PROMPT.txt
if [[ "$#" -gt 0 ]]; then
  PROMPT_ARGS=("$@")
elif [[ -n "${PROMPT:-}" ]]; then
  PROMPT_ARGS=("$PROMPT")
elif [[ -f /work/PROMPT.txt ]]; then
  PROMPT_ARGS=("$(cat /work/PROMPT.txt)")
else
  echo "No prompt found. Pass it as args, set \$PROMPT, or put it in /work/PROMPT.txt" >&2
  exit 2
fi

START_EPOCH=$(date +%s)
timeout --signal=TERM --kill-after=60 "$TIMEOUT_S" claude -p \
  --model "$MODEL" \
  --effort "$EFFORT" \
  $SAFE_FLAG \
  --strict-mcp-config \
  --disallowedTools 'Bash(git *)' \
  --permission-mode "$PERMISSION_MODE" \
  --output-format "$OUTPUT_FORMAT" \
  "${PROMPT_ARGS[@]}" \
  > /tmp/claude-output.json 2> /tmp/claude-stderr.log
RC=$?
# Outputs are buffered OUTSIDE /work so a tidying agent cannot delete its own
# record mid-run; they land in the task folder only now, at exit.
cp /tmp/claude-output.json /work/claude-output.json 2>/dev/null || true
cp /tmp/claude-stderr.log /work/claude-stderr.log 2>/dev/null || true
END_EPOCH=$(date +%s)

# Preserve the full turn-by-turn transcript (Claude Code session JSONL, written
# under the ephemeral config) into the task folder before the container dies.
if compgen -G "$CFG/projects/*/*.jsonl" > /dev/null 2>&1; then
  mkdir -p /work/claude-trace
  cp "$CFG"/projects/*/*.jsonl /work/claude-trace/ 2>/dev/null || true
fi

# Peak memory of the whole container (claude + every K subprocess).
# cgroup v2 first, v1 fallback; null if neither is readable.
MEM_PEAK=null
for f in /sys/fs/cgroup/memory.peak /sys/fs/cgroup/memory/memory.max_usage_in_bytes; do
  if [[ -r "$f" ]]; then MEM_PEAK="$(cat "$f")"; break; fi
done

TIMED_OUT=false
[[ "$RC" -eq 124 ]] && TIMED_OUT=true   # 137 = SIGKILL (kill-after or OOM) — see exit_code

cat > /work/metrics.json <<EOF
{
  "model": "$MODEL",
  "effort": "$EFFORT",
  "output_format": "$OUTPUT_FORMAT",
  "timeout_s": $TIMEOUT_S,
  "start_epoch": $START_EPOCH,
  "end_epoch": $END_EPOCH,
  "duration_s": $((END_EPOCH - START_EPOCH)),
  "exit_code": $RC,
  "timed_out": $TIMED_OUT,
  "mem_peak_bytes": $MEM_PEAK
}
EOF

echo "metrics: duration=$((END_EPOCH - START_EPOCH))s exit=$RC timed_out=$TIMED_OUT mem_peak=$MEM_PEAK" >&2
exit "$RC"
