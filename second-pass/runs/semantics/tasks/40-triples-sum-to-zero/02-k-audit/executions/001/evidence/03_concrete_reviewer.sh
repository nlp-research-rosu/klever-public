#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/forty-triples-audit
harness=/audit-output/evidence/actual_program_tests.py
translated="$scratch/actual-program-tests.mpy"

candidate_lines=$(wc -l < "$scratch/candidate-src/solution.py")
if ! cmp -s \
  "$scratch/candidate-src/solution.py" \
  <(sed -n "1,${candidate_lines}p" "$harness"); then
  echo "REVIEWER_HARNESS_PROGRAM_PREFIX_IDENTITY FAIL"
  diff -u "$scratch/candidate-src/solution.py" \
    <(sed -n "1,${candidate_lines}p" "$harness") || true
  exit 1
fi
echo "REVIEWER_HARNESS_PROGRAM_PREFIX_IDENTITY OK"

python3 "$scratch/trusted/py2mpy.py" "$harness" > "$translated"
translate_status=$?
echo "REVIEWER_TRANSLATOR_EXIT_STATUS $translate_status"
if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi
sha256sum "$harness" "$translated"

krun "$translated" --definition "$scratch/runtime-kompiled"
