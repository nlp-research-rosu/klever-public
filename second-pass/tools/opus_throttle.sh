#!/usr/bin/env bash
# opus_throttle.sh — quota-aware scheduler for opus runs. PURELY EXTERNAL:
# touches nothing inside docker/; it just decides WHEN to invoke the validated
# Claude one-task wrapper, one task at a time.
#
# Policy (per user spec): assume each opus run costs ~15% of the 5-hour window
# and keep a 10% buffer. Before firing a run, read the usage endpoint and
# project: usage + 15 * (running_opus + 1). Fire only if the projection stays
# <= 90. Otherwise wait (or sleep until the window resets when nothing is
# running and usage alone is too high). Parallelism is additionally capped.
#
# Queue: all four supported opus condition folders, with control conditions
# before Kit treatments. The one-task wrapper infers the condition, prompt,
# and Kit-only Compose override from the config name. Use --validate-queue to
# check the complete 4 x 24 folder set without contacting Docker or Anthropic.
set -u
DEFAULT_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="${HUMANEVAL_BENCHMARK_ROOT:-$DEFAULT_REPO}"
COST_PCT=15
CEILING=90
MAX_PAR="${MAX_PAR:-4}"
EXPECTED_CONFIGS=(
  claude-code-opus-xhigh-4-8-bare
  claude-code-opus-xhigh-4-8-semantics
  claude-code-opus-xhigh-4-8-kit
  claude-code-opus-xhigh-4-8-kit-semantics
)
declare -a SELECTED_PROBLEMS=()

log() { echo "[$(date '+%m-%d %H:%M:%S')] $*"; }

usage_pct() {  # prints integer percent, 999 on any failure, 998 on dead auth
  python3 - <<'PY'
import json, subprocess
try:
    tok = json.load(open('/home/yuqing/.claude/.credentials.json'))['claudeAiOauth']['accessToken']
    out = subprocess.run(['curl','-s','-m','20','https://api.anthropic.com/api/oauth/usage',
                          '-H',f'Authorization: Bearer {tok}',
                          '-H','anthropic-beta: oauth-2025-04-20'],
                         capture_output=True, text=True, timeout=30).stdout
    d = json.loads(out)
    if 'five_hour' not in d:
        print(998 if 'error' in d and 'rate' not in str(d).lower() else 999)
    else:
        print(int(d['five_hour']['utilization']))
except Exception:
    print(999)
PY
}

reset_secs() {  # seconds until window reset (+180 buffer), fallback 1200
  python3 - <<'PY'
import json, subprocess, datetime
try:
    tok = json.load(open('/home/yuqing/.claude/.credentials.json'))['claudeAiOauth']['accessToken']
    out = subprocess.run(['curl','-s','-m','20','https://api.anthropic.com/api/oauth/usage',
                          '-H',f'Authorization: Bearer {tok}',
                          '-H','anthropic-beta: oauth-2025-04-20'],
                         capture_output=True, text=True, timeout=30).stdout
    d = json.loads(out)
    t = datetime.datetime.fromisoformat(d['five_hour']['resets_at'])
    now = datetime.datetime.now(datetime.timezone.utc)
    print(max(120, int((t-now).total_seconds()) + 180))
except Exception:
    print(1200)
PY
}

running_opus() {
  docker ps -q 2>/dev/null | while read -r id; do
    docker inspect "$id" --format '{{range .Mounts}}{{if eq .Destination "/work"}}{{.Source}}{{end}}{{end}}' 2>/dev/null
  done | grep -c "runs/claude-code-opus-" || true
}

load_selected_problems() {
  local output
  if ! output=$(python3 - "$REPO/data/selection.json" <<'PY'
import json
import re
import sys

path = sys.argv[1]
try:
    selected = json.load(open(path))["selected"]
    if not isinstance(selected, list) or len(selected) != 24:
        raise ValueError("selection must contain exactly 24 entries")
    problems = []
    for entry in selected:
        problem = entry["id"]
        if not isinstance(problem, str) or not re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._-]*", problem
        ):
            raise ValueError(f"unsafe selected problem id: {problem!r}")
        problems.append(problem)
    if len(set(problems)) != len(problems):
        raise ValueError("selected problem ids must be unique")
except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
    print(f"invalid selection: {error}", file=sys.stderr)
    raise SystemExit(2)
print("\n".join(problems))
PY
  ); then
    return 2
  fi
  mapfile -t SELECTED_PROBLEMS <<< "$output"
}

validate_queue() {
  local config problem task errors=0 expected=0
  if [[ -L "$REPO/runs" || ! -d "$REPO/runs" ]]; then
    echo "queue validation failed: runs root must be a real directory: $REPO/runs" >&2
    return 2
  fi
  for config in "${EXPECTED_CONFIGS[@]}"; do
    if [[ -L "$REPO/runs/$config" || ! -d "$REPO/runs/$config" ]]; then
      echo "queue validation failed: missing real config directory: $config" >&2
      errors=1
      continue
    fi
    for problem in "${SELECTED_PROBLEMS[@]}"; do
      expected=$((expected + 1))
      task="$REPO/runs/$config/$problem"
      if [[ -L "$task" || ! -d "$task" ]]; then
        echo "queue validation failed: missing real task directory: $config/$problem" >&2
        errors=1
      fi
    done
  done
  [[ $errors -eq 0 ]] || return 2
  printf 'validated %d expected task folders\n' "$expected"
}

# Reset folders whose run died on session-limit / auth errors so they re-queue.
reset_bad() {
  local config problem m d
  for config in "${EXPECTED_CONFIGS[@]}"; do
    for problem in "${SELECTED_PROBLEMS[@]}"; do
      m="$REPO/runs/$config/$problem/metrics.json"
      [[ -f "$m" ]] || continue
      if python3 -c "
import json, os
d = json.load(open('$m'))
if d.get('exit_code', 0) == 0: raise SystemExit(1)
co = os.path.join(os.path.dirname('$m'), 'claude-output.json')
txt = ''
try: txt = json.load(open(co)).get('result') or ''
except Exception: pass
bad = ('session limit' in txt) or ('Failed to authenticate' in txt) or ('Not logged in' in txt)
raise SystemExit(0 if bad else 1)" 2>/dev/null; then
        d="$(dirname "$m")"
        find "$d" -mindepth 1 -maxdepth 1 ! -name prompt.py ! -name py2mpy.py \
             ! -name run-input.json ! -name reference-semantics -exec rm -rf {} +
        log "reset limit/auth-failed task: ${d#$REPO/runs/}"
      fi
    done
  done
}

next_task() {  # prints "config prob" or nothing; control conditions first
  local cfg problem d
  for cfg in "${EXPECTED_CONFIGS[@]}"; do
    for problem in "${SELECTED_PROBLEMS[@]}"; do
      d="$REPO/runs/$cfg/$problem"
      [[ -f "$d/metrics.json" ]] && continue
      # skip tasks already running (container mounted on this dir)
      if docker ps -q | while read -r id; do docker inspect "$id" --format '{{range .Mounts}}{{if eq .Destination "/work"}}{{.Source}}{{end}}{{end}}'; done | grep -qx "${d%/}"; then
        continue
      fi
      echo "$cfg $problem"
      return
    done
  done
}

main() {
  if [[ $# -gt 1 || ( $# -eq 1 && "${1:-}" != "--validate-queue" ) ]]; then
    echo "usage: $0 [--validate-queue]" >&2
    return 2
  fi
  load_selected_problems || return $?
  validate_queue || return $?
  [[ ${1:-} == "--validate-queue" ]] && return 0

  log "opus throttle started (cost=${COST_PCT}%/run, ceiling=${CEILING}%, max_par=${MAX_PAR})"
  while :; do
    reset_bad
    TASK=$(next_task)
    if [[ -z "$TASK" ]]; then
      if [[ "$(running_opus)" -gt 0 ]]; then sleep 120; continue; fi
      log "ALL OPUS TASKS COMPLETE"
      return 0
    fi
    R=$(running_opus)
    if [[ "$R" -ge "$MAX_PAR" ]]; then sleep 90; continue; fi
    PCT=$(usage_pct)
    if [[ "$PCT" -eq 998 ]]; then
      log "auth dead — run 'claude auth login', throttle exiting"
      return 2
    fi
    if [[ "$PCT" -eq 999 ]]; then sleep 300; continue; fi
    PROJ=$((PCT + COST_PCT * (R + 1)))
    if [[ "$PROJ" -le "$CEILING" ]]; then
      CFG="${TASK%% *}"; PROB="${TASK##* }"
      log "usage=${PCT}% running=$R projected=${PROJ}% <= ${CEILING}% — firing $CFG/$PROB"
      cp ~/.claude/.credentials.json "$REPO/docker/claude-code/secrets/claude/.credentials.json" 2>/dev/null
      chmod 600 "$REPO/docker/claude-code/secrets/claude/.credentials.json" 2>/dev/null
      bash "$REPO/docker/claude-code/run_task.sh" "$CFG" "$PROB" \
        >> "$REPO/_setup/opus_throttle_tasks.log" 2>&1 &
      sleep 45   # stagger spawns so usage/running counts settle
    else
      if [[ "$R" -eq 0 ]]; then
        S=$(reset_secs)
        log "usage=${PCT}% projected=${PROJ}% > ${CEILING}% with nothing running — sleeping ${S}s to window reset"
        sleep "$S"
      else
        sleep 180
      fi
    fi
  done
}

main "$@"
