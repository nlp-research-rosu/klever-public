#!/usr/bin/env bash
set -uo pipefail

mutation_dir=/tmp/audit-work/25-factorize-audit/body-mutation
trusted_translator=/tmp/audit-work/25-factorize-audit/trusted/py2mpy.py
original_mpy=/tmp/audit-work/25-factorize-audit/source/solution.mpy
mutated_mpy="$mutation_dir/solution.mpy"
regenerated_mpy="$mutation_dir/solution.regenerated.mpy"
semantic_definition=/tmp/audit-work/25-factorize-audit/semantic-fresh-kompiled
mutated_proof_definition=/tmp/audit-work/25-factorize-audit/body-mut-verification-kompiled

cd "$mutation_dir" || exit 1

echo "$ python3 $trusted_translator $mutation_dir/solution.py > $regenerated_mpy"
python3 "$trusted_translator" "$mutation_dir/solution.py" > "$regenerated_mpy"
status=$?
printf '[exit_status=%d]\n' "$status"
if (( status != 0 )); then
  exit "$status"
fi

echo "$ cmp $mutated_mpy $regenerated_mpy"
cmp "$mutated_mpy" "$regenerated_mpy"
status=$?
printf '[exit_status=%d]\n' "$status"
if (( status != 0 )); then
  exit "$status"
fi

echo "$ cmp $original_mpy $mutated_mpy"
cmp "$original_mpy" "$mutated_mpy"
status=$?
printf '[exit_status=%d expected_nonzero=yes]\n' "$status"

sha256sum "$original_mpy" "$mutated_mpy"

echo "$ krun $mutated_mpy -cINPUT=25 --definition $semantic_definition"
krun "$mutated_mpy" -cINPUT=25 --definition "$semantic_definition"
status=$?
printf '[exit_status=%d]\n' "$status"
if (( status != 0 )); then
  exit "$status"
fi

echo "$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition $mutated_proof_definition"
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$mutated_proof_definition"
status=$?
printf '[exit_status=%d]\n' "$status"
if (( status != 0 )); then
  exit "$status"
fi

echo "$ kprove spec.k --definition $mutated_proof_definition --spec-module SPEC"
kprove spec.k \
  --definition "$mutated_proof_definition" \
  --spec-module SPEC
status=$?
printf '[exit_status=%d]\n' "$status"
exit "$status"
