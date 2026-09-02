#!/usr/bin/env bash
# run_matrix.sh [--jobs N] [--config <name>]... [--dry-run]
#
# Runs every opencode-* (config x problem) task under runs/ through run_task.sh.
# Same behavior as the claude-code matrix driver: resumable (skips folders that
# already contain metrics.json), concurrency-capped, --dry-run to preview.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"

JOBS=2
DRY=0
declare -a CONFIGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --jobs)    JOBS="$2"; shift 2 ;;
    --config)  CONFIGS+=("$2"); shift 2 ;;
    --dry-run) DRY=1; shift ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

if [[ ${#CONFIGS[@]} -eq 0 ]]; then
  mapfile -t CONFIGS < <(cd "$REPO/runs" && ls -d opencode-*/ 2>/dev/null | sed 's#/##')
fi
[[ ${#CONFIGS[@]} -gt 0 ]] || { echo "no opencode-* configs under runs/" >&2; exit 1; }

declare -a TASK_CONFIGS=()
declare -a TASK_PROBLEMS=()
skipped=0
for c in "${CONFIGS[@]}"; do
  for d in "$REPO/runs/$c"/*/; do
    [[ -d "$d" ]] || continue
    p="$(basename "$d")"
    if [[ -f "$d/metrics.json" ]]; then skipped=$((skipped+1)); continue; fi
    TASK_CONFIGS+=("$c")
    TASK_PROBLEMS+=("$p")
  done
done

echo "opencode matrix: ${#TASK_CONFIGS[@]} task(s) to run, $skipped already done, jobs=$JOBS" >&2
for i in "${!TASK_CONFIGS[@]}"; do
  printf '  %s %s\n' "${TASK_CONFIGS[$i]}" "${TASK_PROBLEMS[$i]}" >&2
done
[[ $DRY -eq 1 ]] && exit 0
[[ ${#TASK_CONFIGS[@]} -gt 0 ]] || exit 0

matrix_rc=0
{
  for i in "${!TASK_CONFIGS[@]}"; do
    printf '%s\0%s\0' "${TASK_CONFIGS[$i]}" "${TASK_PROBLEMS[$i]}"
  done
} | xargs -0 -r -P "$JOBS" -n 2 bash -c '
  bash "$0" "$@"
  rc=$?
  if [[ $rc -ne 0 ]]; then
    printf "FAILED:" >&2
    printf " %q" "$@" >&2
    printf "\n" >&2
  fi
  exit "$rc"
' "$HERE/run_task.sh" || matrix_rc=$?

echo "" >&2
echo "=== SUMMARY (from metrics.json) ===" >&2
for c in "${CONFIGS[@]}"; do
  for d in "$REPO/runs/$c"/*/; do
    m="$d/metrics.json"
    [[ -f "$m" ]] || continue
    python3 -c "
import json
m=json.load(open('$m'))
peak=m.get('mem_peak_bytes')
peak='%.1fG'%(peak/2**30) if isinstance(peak,int) else '?'
print(f\"{'$c'}/{'$(basename "$d")'}: exit={m['exit_code']} dur={m['duration_s']}s peak={peak} timed_out={m['timed_out']}\")"
  done
done

exit "$matrix_rc"
