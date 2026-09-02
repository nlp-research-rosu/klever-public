#!/usr/bin/env bash
set -uo pipefail

scratch_root=/tmp/audit-work/96-count-up-to
evidence_root=/audit-output/evidence

printf 'Mutation: outer-loop increment changes from +1 to +2.\n'
python3 "$scratch_root/py2mpy.py" \
  "$evidence_root/solution-body-mutation.py" \
  > "$evidence_root/solution-body-mutation.mpy"
translate_status=$?
printf 'translator_exit=%d\n' "$translate_status"

command=(
  krun
  "$evidence_root/solution-body-mutation.mpy"
  --definition
  "$scratch_root/semantic-fresh-kompiled"
  -cN=5
  --output
  pretty
)
printf 'COMMAND:'
printf ' %q' "${command[@]}"
printf '\n'

output=$("${command[@]}" 2>&1)
run_status=$?
printf '%s\n' "$output"
printf 'EXIT_STATUS: %d\n' "$run_status"

if [[ "$translate_status" -ne 0 || "$run_status" -ne 0 ]]; then
  exit 1
fi
if ! grep -q 'Module' <<< "$output"; then
  printf 'FAIL: mutated program unexpectedly left no residual Module term\n'
  exit 1
fi
if ! grep -q '<result>' <<< "$output" || ! grep -Fq '.K' <<< "$output"; then
  printf 'FAIL: expected unchanged empty result cell was not visible\n'
  exit 1
fi
if grep -q 'cons (' <<< "$output"; then
  printf 'FAIL: mutated program unexpectedly fabricated a list result\n'
  exit 1
fi
printf 'PASS: exact lowering rejected the body mutation; execution stayed at the residual AST.\n'
