#!/usr/bin/env bash
# Run ONE headless OpenCode session, confined to /work (the mounted task dir),
# under a wall-clock timeout. Records duration, exit code, and the container's
# peak memory to /work/metrics.json; saves the session output to
# /work/opencode-output.log, the tail (for the RESULT line) to
# /work/opencode-last.txt, and the full session storage to /work/opencode-trace/.
set -uo pipefail

MODEL="${MODEL:-openrouter/moonshotai/kimi-k3}"   # opencode provider/model id
TIMEOUT_S="${TIMEOUT_S:-3600}"

# API keys: export every key present in the mounted secrets file.
# OPENROUTER_API_KEY -> openrouter provider; GLM_API_KEY -> ZHIPU_API_KEY
# (Z.ai / GLM coding plan provider).
if [[ -f /auth/api_key.json ]]; then
  eval "$(python3 - <<'PYEOF'
import json
d = json.load(open('/auth/api_key.json'))
if d.get('OPENROUTER_API_KEY'): print(f"export OPENROUTER_API_KEY='{d['OPENROUTER_API_KEY']}'")
if d.get('GLM_API_KEY'): print(f"export ZHIPU_API_KEY='{d['GLM_API_KEY']}'")
PYEOF
)"
fi
if [[ -z "${OPENROUTER_API_KEY:-}" && -z "${ZHIPU_API_KEY:-}" ]]; then
  echo "No API key found (env or /auth/api_key.json)" >&2
  exit 2
fi

# Resolve the prompt: container args  >  $PROMPT  >  /work/PROMPT.txt
if [[ "$#" -gt 0 ]]; then
  PROMPT_TEXT="$*"
elif [[ -n "${PROMPT:-}" ]]; then
  PROMPT_TEXT="$PROMPT"
elif [[ -f /work/PROMPT.txt ]]; then
  PROMPT_TEXT="$(cat /work/PROMPT.txt)"
else
  echo "No prompt found. Pass it as args, set \$PROMPT, or put it in /work/PROMPT.txt" >&2
  exit 2
fi

START_EPOCH=$(date +%s)
# < /dev/null is load-bearing: with an attached-but-open stdin pipe (e.g.
# docker compose run from a background process), opencode blocks forever
# waiting to read piped stdin before processing the message argument.
# --print-logs gives live progress in opencode-stderr.log.
#
# Bounded auto-continue: the endpoint sometimes returns an empty response,
# which opencode treats as session-over (no error, no retry). If the session
# ends without the required RESULT: line and wall clock remains, continue the
# SAME session with a neutral nudge. Condition-neutral infrastructure retry.
DEADLINE=$((START_EPOCH + TIMEOUT_S))
CONTINUES=0
: > /tmp/opencode-output.log
: > /tmp/opencode-stderr.log
RC=0
while :; do
  REMAIN=$((DEADLINE - $(date +%s)))
  if [[ "$REMAIN" -le 0 ]]; then RC=124; break; fi
  if [[ "$CONTINUES" -eq 0 ]]; then
    ARGS=("$PROMPT_TEXT")
  else
    ARGS=(--continue "continue")
  fi
  timeout --signal=TERM --kill-after=60 "$REMAIN" \
    opencode run --pure --print-logs --log-level WARN -m "$MODEL" "${ARGS[@]}" \
    < /dev/null \
    >> /tmp/opencode-output.log 2>> /tmp/opencode-stderr.log
  RC=$?
  [[ "$RC" -eq 124 ]] && break
  grep -aq "^RESULT:" /tmp/opencode-output.log && break
  CONTINUES=$((CONTINUES + 1))
  [[ "$CONTINUES" -gt 4 ]] && break
done
# Buffered outside /work so a tidying agent cannot delete its own record.
cp /tmp/opencode-output.log /work/opencode-output.log 2>/dev/null || true
cp /tmp/opencode-stderr.log /work/opencode-stderr.log 2>/dev/null || true
END_EPOCH=$(date +%s)

# Tail of the output (where the RESULT: line lives) for quick parsing.
tail -n 120 /tmp/opencode-output.log > /work/opencode-last.txt 2>/dev/null || true

# Preserve the full session storage (turn-by-turn trace) before the container dies.
if [[ -d "$HOME/.local/share/opencode" ]]; then
  mkdir -p /work/opencode-trace
  cp -r "$HOME/.local/share/opencode/." /work/opencode-trace/ 2>/dev/null || true
fi

MEM_PEAK=null
for f in /sys/fs/cgroup/memory.peak /sys/fs/cgroup/memory/memory.max_usage_in_bytes; do
  if [[ -r "$f" ]]; then MEM_PEAK="$(cat "$f")"; break; fi
done

TIMED_OUT=false
[[ "$RC" -eq 124 ]] && TIMED_OUT=true

cat > /work/metrics.json <<EOF
{
  "agent": "opencode",
  "model": "$MODEL",
  "timeout_s": $TIMEOUT_S,
  "continues": $CONTINUES,
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
