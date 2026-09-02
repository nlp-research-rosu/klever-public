#!/usr/bin/env bash
set +e
work=/tmp/audit-work/candidate-src
llvm_def=/tmp/audit-work/semantic-kompiled
haskell_def=/tmp/audit-work/verification-kompiled

cd "$work" || exit 1

echo '$ kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm --output-definition /tmp/audit-work/semantic-kompiled'
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition "$llvm_def"
llvm_status=$?
echo "LLVM_KOMPILE_EXIT_STATUS=$llvm_status"

echo '$ python3 /audit-output/evidence/concrete_python_oracle.py'
python3 /audit-output/evidence/concrete_python_oracle.py
python_status=$?
echo "PYTHON_ORACLE_EXIT_STATUS=$python_status"

run_case() {
  case_name=$1
  input_term=$2
  expected=$3
  echo "$ krun solution.mpy --definition $llvm_def -cINPUT='$input_term'"
  case_output=$(krun solution.mpy --definition "$llvm_def" -cINPUT="$input_term" 2>&1)
  case_status=$?
  echo "$case_output"
  normalized=$(printf '%s' "$case_output" | tr -d '[:space:]')
  if [[ "$normalized" == *"$expected"* ]]; then
    compare_status=0
  else
    compare_status=1
  fi
  echo "KRUN_CASE=$case_name EXIT_STATUS=$case_status EXPECTED=$expected MATCH=$((1 - compare_status))"
  if (( case_status || compare_status )); then
    return 1
  fi
  return 0
}

concrete_status=0
if (( llvm_status == 0 )); then
  run_case \
    prompt_one \
    'VList(VString("a"), VFloat("3.14"), VInt(5))' \
    'result(VList(VInt(5),.PyVals))' || concrete_status=1
  run_case \
    empty \
    'VList()' \
    'result(VList(.PyVals))' || concrete_status=1
  run_case \
    bool_boundary \
    'VList(VBool(true), VBool(false), VInt(0), VInt(-4), VFloat("2.0"))' \
    'result(VList(VBool(true),VBool(false),VInt(0),VInt(-4),.PyVals))' || concrete_status=1
  run_case \
    constructors \
    'VList(VString("x"), VFloat("2.0"), VInt(7), VBool(true), VList(VInt(9)), VDict, VNone, VOpaque("object"), VInt(-1))' \
    'result(VList(VInt(7),VBool(true),VInt(-1),.PyVals))' || concrete_status=1
  run_case \
    large_duplicate \
    'VList(VInt(100000000000000000000000000000000000000000000000000000000000000000000000000000000), VString("skip"), VInt(100000000000000000000000000000000000000000000000000000000000000000000000000000000), VInt(-100000000000000000000000000000000000000000000000000000000000000000000000000000000))' \
    'result(VList(VInt(100000000000000000000000000000000000000000000000000000000000000000000000000000000),VInt(100000000000000000000000000000000000000000000000000000000000000000000000000000000),VInt(-100000000000000000000000000000000000000000000000000000000000000000000000000000000),.PyVals))' || concrete_status=1
else
  concrete_status=1
  echo 'KRUN_CASES_SKIPPED=LLVM_BUILD_FAILED'
fi
echo "CONCRETE_SUITE_EXIT_STATUS=$concrete_status"

echo '$ kompile verification.k --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition /tmp/audit-work/verification-kompiled'
kompile verification.k \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition "$haskell_def"
haskell_status=$?
echo "HASKELL_KOMPILE_EXIT_STATUS=$haskell_status"

proof_status=1
if (( haskell_status == 0 )); then
  echo '$ kprove spec.k --definition /tmp/audit-work/verification-kompiled --spec-module SPEC'
  kprove spec.k \
    --definition "$haskell_def" \
    --spec-module SPEC
  proof_status=$?
  echo "KPROVE_ALL_17_CLAIMS_EXIT_STATUS=$proof_status"
else
  echo 'KPROVE_SKIPPED=HASKELL_BUILD_FAILED'
fi

if (( llvm_status || python_status || concrete_status || haskell_status || proof_status )); then
  exit 1
fi
exit 0
