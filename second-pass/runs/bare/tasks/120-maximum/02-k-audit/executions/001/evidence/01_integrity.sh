#!/usr/bin/env bash
set -u

status=0

run_check() {
  description=$1
  shift
  printf 'CHECK: %s\n' "$description"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  check_status=$?
  printf 'EXIT_STATUS: %d\n\n' "$check_status"
  if (( check_status != 0 )); then
    status=1
  fi
}

run_check "GENERATED_SEMANTICS forbids a trusted reference-semantics mount" \
  test ! -e /reference/reference-semantics

for required in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-53-51-019f89ac-cd7c-7301-94b5-c31f4b35c569.jsonl
do
  run_check "required artifact is a regular, non-symlink file: $required" \
    test -f "$required" -a ! -L "$required"
done

run_check "candidate prompt is byte-identical to trusted prompt" \
  cmp -s /candidate/prompt.py /reference/prompt.py
run_check "candidate translator is byte-identical to trusted translator" \
  cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run_check "run-input.json parses as JSON" \
  python3 -m json.tool /candidate/run-input.json
run_check "metrics.json parses as JSON" \
  python3 -m json.tool /candidate/metrics.json
run_check "structured trace is valid JSONL" \
  python3 -c 'import json,sys; p=sys.argv[1]; rows=[json.loads(line) for line in open(p, encoding="utf-8")]; print(f"valid_jsonl_records={len(rows)}")' \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-53-51-019f89ac-cd7c-7301-94b5-c31f4b35c569.jsonl

run_check "hash trusted and candidate provenance artifacts" \
  sha256sum \
    /reference/canonical.py /reference/prompt.py /reference/py2mpy.py \
    /candidate/prompt.py /candidate/py2mpy.py \
    /candidate/solution.py /candidate/solution.mpy \
    /candidate/semantic.k /candidate/verification.k /candidate/spec.k

printf 'UNTRUSTED GENERATION CLAIM EXTRACT\n'
rg -n \
  'RESULT:|#Top|exit code|exited|succeeded|failed|timed out|timed_out|krun|kprove|kompile' \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-53-51-019f89ac-cd7c-7301-94b5-c31f4b35c569.jsonl \
  | tail -n 160
extract_status=${PIPESTATUS[0]}
printf 'EXTRACT_RG_EXIT_STATUS: %d\n\n' "$extract_status"

printf 'CANDIDATE SOURCE ARTIFACT TYPES (compiled trees intentionally excluded)\n'
find /candidate -maxdepth 1 -printf '%y %f -> %l\n' | sort
find_status=${PIPESTATUS[0]}
printf 'FIND_EXIT_STATUS: %d\n\n' "$find_status"

printf 'OVERALL_EXIT_STATUS: %d\n' "$status"
exit "$status"
