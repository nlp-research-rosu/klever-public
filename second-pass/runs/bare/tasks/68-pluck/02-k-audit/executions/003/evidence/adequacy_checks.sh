#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit
proof_definition="$scratch/proof-audit-kompiled"
concrete_definition="$scratch/concrete-audit-kompiled"
witness_definition="$scratch/witness-audit2-kompiled"

echo '$ kprove pinning-spec.k --definition proof-audit-kompiled --spec-module PINNING-SPEC'
pinning_output=$(
  kprove "$scratch/pinning-spec.k" \
    --definition "$proof_definition" \
    --spec-module PINNING-SPEC 2>&1
)
pinning_status=$?
printf '%s\n' "$pinning_output"
echo "constructor pinning kprove exit=$pinning_status"
[[ "$pinning_output" == *"#Top"* ]]
pinning_top=$?
echo "constructor pinning #Top check exit=$pinning_top"

echo '$ krun solution.mpy --definition concrete-audit-kompiled -cARGS=VArray(68,0,3)'
baseline_output=$(
  krun "$scratch/solution.mpy" \
    --definition "$concrete_definition" \
    -cARGS='VArray(68,0,3)' 2>&1
)
baseline_status=$?
printf '%s\n' "$baseline_output"
echo "fixed semantic.k symbolic-array krun exit=$baseline_status"
[[ "$baseline_output" == *"minEvenArray ( 68 , 0 , 3 )"* ]]
baseline_residual=$?
echo "fixed semantic.k residual minEvenArray check exit=$baseline_residual"

echo '$ test ! -e witness-audit2-kompiled'
test ! -e "$witness_definition"
witness_clean=$?
echo "witness clean-start exit=$witness_clean"

echo '$ kompile --backend llvm witness.k --main-module WITNESS --syntax-module MPY-SYNTAX --output-definition witness-audit2-kompiled'
kompile \
  --backend llvm \
  "$scratch/witness.k" \
  --main-module WITNESS \
  --syntax-module MPY-SYNTAX \
  --output-definition "$witness_definition"
witness_build=$?
echo "witness kompile exit=$witness_build"

echo '$ krun solution.mpy --definition witness-audit2-kompiled -cARGS=VArray(68,0,3)'
witness_output=$(
  krun "$scratch/solution.mpy" \
    --definition "$witness_definition" \
    -cARGS='VArray(68,0,3)' 2>&1
)
witness_run=$?
printf '%s\n' "$witness_output"
echo "witness krun exit=$witness_run"
grep -Fq '    VList ( 2 , 1 , .Ints )' <<<"$witness_output"
witness_result=$?
echo "witness expected result [2,1] check exit=$witness_result"

echo '$ trusted canonical and submitted Python on [4,2,3]'
python3 - "$scratch/trusted-canonical.py" "$scratch/solution.py" <<'PY'
import importlib.util
import sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck

canonical = load(sys.argv[1], "canonical_witness")
submitted = load(sys.argv[2], "submitted_witness")
arr = [4, 2, 3]
print(f"input={arr}")
print(f"canonical={canonical(arr)}")
print(f"submitted={submitted(arr)}")
raise SystemExit(0 if canonical(arr) == submitted(arr) == [2, 1] else 1)
PY
python_witness=$?
echo "Python witness comparison exit=$python_witness"

overall=$((pinning_status || pinning_top || baseline_residual || witness_clean || witness_build || witness_run || witness_result || python_witness))
echo "adequacy mechanical checks aggregate exit=$overall"
exit "$overall"
