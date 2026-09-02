#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/52-below-threshold
failures=0

printf 'Trusted prompt:\n'
nl -ba "$scratch/trusted/prompt.py"
printf 'Trusted canonical:\n'
nl -ba "$scratch/trusted/canonical.py"
printf 'Submitted solution:\n'
nl -ba "$scratch/solution.py"

python3 "$scratch/trusted/py2mpy.py" "$scratch/solution.py" \
  > "$scratch/reviewer-regenerated-solution.mpy"
translate_status=$?
printf 'trusted translator exit=%s\n' "$translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

if cmp -s "$scratch/reviewer-regenerated-solution.mpy" "$scratch/solution.mpy"; then
  printf 'OK trusted regeneration is byte-identical to submitted solution.mpy\n'
else
  printf 'FAIL trusted regeneration differs from submitted solution.mpy\n'
  diff -u "$scratch/solution.mpy" "$scratch/reviewer-regenerated-solution.mpy" || true
  failures=$((failures + 1))
fi
sha256sum \
  "$scratch/solution.py" \
  "$scratch/solution.mpy" \
  "$scratch/reviewer-regenerated-solution.mpy"

python3 -m doctest "$scratch/solution.py"
doctest_status=$?
printf 'solution doctest exit=%s\n' "$doctest_status"
if [[ "$doctest_status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

/audit-output/evidence/differential.py
differential_status=$?
printf 'independent differential exit=%s\n' "$differential_status"
if [[ "$differential_status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

printf 'FIDELITY_FAILURE_COUNT=%s\n' "$failures"
exit "$failures"
