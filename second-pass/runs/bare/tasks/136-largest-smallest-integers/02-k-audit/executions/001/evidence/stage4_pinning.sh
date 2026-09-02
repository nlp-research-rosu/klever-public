#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
proof_def="$work/audit-verification-kompiled"
semantic_def="$work/audit-semantic-kompiled"
overall=0

run_recorded() {
  echo "COMMAND: $*"
  "$@"
  local status=$?
  echo "EXIT_STATUS=$status"
  if (( status != 0 )); then
    overall=1
  fi
}

run_recorded kast "$work/solution.mpy" \
  --definition "$proof_def" \
  --module VERIFICATION \
  --sort Program \
  --expand-macros \
  --output json \
  --output-file "$evidence/solution-file.kast.json"

run_recorded kast \
  --expression solutionProgram \
  --definition "$proof_def" \
  --module VERIFICATION \
  --sort Program \
  --expand-macros \
  --output json \
  --output-file "$evidence/solution-macro.kast.json"

echo 'COMMAND: cmp -s solution-file.kast.json solution-macro.kast.json'
cmp -s "$evidence/solution-file.kast.json" "$evidence/solution-macro.kast.json"
cmp_status=$?
echo "CONSTRUCTOR_IDENTITY_EXIT_STATUS=$cmp_status"
if (( cmp_status != 0 )); then
  overall=1
fi
sha256sum "$evidence/solution-file.kast.json" "$evidence/solution-macro.kast.json"

for input in \
  'Value(pyIntList(nil))' \
  'Value(pyIntList(icon(-2, icon(3, icon(0, nil)))))'
do
  echo "SPEC_REPRESENTATION_INPUT=$input"
  run_recorded timeout 120 krun "$work/solution.mpy" \
    --definition "$semantic_def" \
    -cINPUT="$input"
done

echo "CONCRETE_CLAIM_WITNESS_1: IS=nil, env=.Map, steps=0"
echo "CONCRETE_CLAIM_WITNESS_2: IS=icon(-2,icon(3,nil)), N=pyNone, P=pyNone, OLD=pyInt(99), REST=.Map, S=0"
echo "CONCRETE_CLAIM_WITNESS_3: IS=icon(-2,icon(3,icon(0,nil))), env=.Map, steps=0"
echo "PYTHON_EXPECTED_1=(None, None)"
echo "PYTHON_EXPECTED_3=(-2, 3)"
echo "OVERALL_STAGE4_STATUS=$overall"
exit "$overall"
