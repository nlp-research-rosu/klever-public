#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work
status=0

run_check() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
}

printf 'GENERATED_SEMANTICS boundary\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'UNEXPECTED_PRESENT: /reference/reference-semantics\n'
  status=1
else
  printf 'EXPECTED_ABSENT: /reference/reference-semantics\n'
fi

printf 'Required artifact types\n'
for path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/rollout-2026-07-22T07-55-11-019f89e4-f694-7913-995d-aa11955108b3.jsonl \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh
do
  if [[ -f "$path" && ! -L "$path" ]]; then
    stat --printf='REGULAR %a %s %n\n' "$path"
  else
    printf 'BAD_TYPE_OR_MISSING: %s\n' "$path"
    status=1
  fi
done

run_check cmp -s /candidate/prompt.py /reference/prompt.py
run_check cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run_check sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py

printf '$ python3 %q %q > %q\n' \
  "$scratch/source/py2mpy.py" \
  "$scratch/source/solution.py" \
  "$scratch/regenerated-solution.mpy"
python3 "$scratch/source/py2mpy.py" "$scratch/source/solution.py" \
  > "$scratch/regenerated-solution.mpy"
rc=$?
printf 'EXIT_STATUS: %d\n' "$rc"
if (( rc != 0 )); then
  status=1
fi

run_check cmp -s \
  "$scratch/regenerated-solution.mpy" \
  "$scratch/source/solution.mpy"
run_check sha256sum \
  "$scratch/regenerated-solution.mpy" \
  "$scratch/source/solution.mpy"

printf 'FINAL_STATUS: %d\n' "$status"
exit "$status"
