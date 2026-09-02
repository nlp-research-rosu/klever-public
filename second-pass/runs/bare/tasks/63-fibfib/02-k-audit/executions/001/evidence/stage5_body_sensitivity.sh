#!/usr/bin/env bash
set -u

status=0
mutation_dir=/tmp/audit-work/body-mutation
trusted_translator=/tmp/audit-work/reference-src/py2mpy.py
definition=/tmp/audit-work/rebuild/concrete-kompiled

echo '$ python3 trusted py2mpy.py mutated solution-return-b.py > solution-return-b.mpy'
python3 "$trusted_translator" \
  "$mutation_dir/solution-return-b.py" \
  > "$mutation_dir/solution-return-b.mpy"
rc=$?
echo "exit=$rc"
(( rc == 0 )) || status=1

echo '$ krun mutated solution-return-b.mpy --definition fresh concrete-kompiled -cN=5'
output="$(
  krun "$mutation_dir/solution-return-b.mpy" \
    --definition "$definition" \
    -cN=5
)"
rc=$?
printf '%s\n' "$output"
echo "exit=$rc"
(( rc == 0 )) || status=1

actual="$(
  printf '%s\n' "$output" |
    sed -n '/<result>/ { n; s/[[:space:]]//g; p; }'
)"
echo "mutated_k_result=$actual"
echo "original_k_result=4"
if [[ "$actual" == 7 && "$actual" != 4 ]]; then
  echo 'body_sensitivity=PASS'
else
  echo 'body_sensitivity=FAIL'
  status=1
fi

echo '$ kast mutated program and compare to the claim macro KORE'
kast "$mutation_dir/solution-return-b.mpy" \
  --definition /tmp/audit-work/rebuild/proof-kompiled \
  --module FIBFIB \
  --sort Pgm \
  --expand-macros \
  --output kore \
  --output-file "$mutation_dir/solution-return-b.kore"
rc=$?
echo "kast_exit=$rc"
(( rc == 0 )) || status=1

cmp -s \
  "$mutation_dir/solution-return-b.kore" \
  /audit-output/evidence/stage4_claim_program_macro.kore
rc=$?
echo "mutated_vs_claim_macro_cmp_exit=$rc (expected 1)"
if (( rc == 0 )); then
  status=1
fi

echo '$ preserve reviewer mutation below /audit-output/evidence'
cp --no-dereference \
  "$mutation_dir/solution-return-b.py" \
  /audit-output/evidence/stage5_solution_return_b.py
cp --no-dereference \
  "$mutation_dir/solution-return-b.mpy" \
  /audit-output/evidence/stage5_solution_return_b.mpy

echo "overall_exit=$status"
exit "$status"
