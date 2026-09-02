#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
adequacy_work=/tmp/audit-work/adequacy
overall=0

mkdir -p "$adequacy_work"
cp "$evidence/concrete_bool_model.py" "$adequacy_work/concrete_bool_model.py"
cp "$evidence/body_sensitivity_solution.py" "$adequacy_work/body_sensitivity_solution.py"

echo '$ python3 /audit-output/evidence/04_witnesses.py'
python3 "$evidence/04_witnesses.py"
witness_status=$?
echo "exit=$witness_status"

echo '$ python3 /reference/py2mpy.py /tmp/audit-work/adequacy/concrete_bool_model.py > /tmp/audit-work/reconstruction/concrete-bool-model.mpy'
python3 /reference/py2mpy.py "$adequacy_work/concrete_bool_model.py" > "$work/concrete-bool-model.mpy"
bool_translate_status=$?
echo "exit=$bool_translate_status"
cp "$work/concrete-bool-model.mpy" "$evidence/concrete_bool_model.mpy"

echo '$ python3 /tmp/audit-work/adequacy/concrete_bool_model.py (expected assertion failure under real Python)'
python3 "$adequacy_work/concrete_bool_model.py"
bool_python_status=$?
echo "exit=$bool_python_status"
if test "$bool_python_status" -eq 0; then
  overall=1
fi

echo '$ krun concrete-bool-model.mpy --definition runtime-kompiled'
(
  cd "$work" &&
  krun concrete-bool-model.mpy --definition runtime-kompiled
)
bool_krun_status=$?
echo "exit=$bool_krun_status"

for item in \
  'spec-bool-model-false.k SPEC-BOOL-MODEL-FALSE expected_success' \
  'spec-bool-real-result.k SPEC-BOOL-REAL-RESULT expected_failure'
do
  set -- $item
  spec_file=$1
  spec_module=$2
  expectation=$3
  cp "$work/$spec_file" "$evidence/claim-specs/$spec_file"
  echo "\$ kprove $spec_file --definition verification-kompiled --spec-module $spec_module ($expectation)"
  (
    cd "$work" &&
    kprove "$spec_file" \
      --definition verification-kompiled \
      --spec-module "$spec_module"
  )
  status=$?
  echo "exit=$status"
  if test "$expectation" = expected_success && test "$status" -ne 0; then
    overall=1
  fi
  if test "$expectation" = expected_failure && test "$status" -eq 0; then
    overall=1
  fi
done

echo '$ trusted translator renders the material body mutation'
python3 /reference/py2mpy.py "$adequacy_work/body_sensitivity_solution.py" > "$work/body-sensitivity-solution.mpy"
mutation_translate_status=$?
echo "exit=$mutation_translate_status"
cp "$work/body-sensitivity-solution.mpy" "$evidence/body_sensitivity_solution.mpy"

echo '$ Python witness for the material body mutation: any_int(5,2,7)'
python3 -c 'import importlib.util; p="/tmp/audit-work/adequacy/body_sensitivity_solution.py"; s=importlib.util.spec_from_file_location("mut",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.any_int(5,2,7)); assert m.any_int(5,2,7) is False'
mutation_python_status=$?
echo "exit=$mutation_python_status"

echo '$ kprove original candidate spec after solution body mutation (proof has no solution.mpy dependency)'
(
  cd "$work" &&
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module ANY-INT-SPEC
)
body_insensitive_status=$?
echo "exit=$body_insensitive_status"

if test "$witness_status" -ne 0 ||
   test "$bool_translate_status" -ne 0 ||
   test "$bool_python_status" -eq 0 ||
   test "$bool_krun_status" -ne 0 ||
   test "$mutation_translate_status" -ne 0 ||
   test "$mutation_python_status" -ne 0 ||
   test "$body_insensitive_status" -ne 0
then
  overall=1
fi

echo "INTERPRETATION: overall=0 means all expected observations occurred, including the expected failure of the real-result Bool claim."
exit "$overall"
