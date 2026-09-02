#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit
no_bridge="$scratch/no-bridge-audit-kompiled"
opposite="$scratch/opposite-audit-kompiled"

echo '$ test ! -e no-bridge-audit-kompiled'
test ! -e "$no_bridge"
clean_no_bridge=$?
echo "no-bridge clean-start exit=$clean_no_bridge"

echo '$ kompile --backend haskell verification-no-bridge.k --main-module VERIFICATION-NO-BRIDGE --syntax-module MPY-SYNTAX --output-definition no-bridge-audit-kompiled'
kompile \
  --backend haskell \
  "$scratch/verification-no-bridge.k" \
  --main-module VERIFICATION-NO-BRIDGE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$no_bridge"
build_no_bridge=$?
echo "no-bridge kompile exit=$build_no_bridge"

echo '$ kprove spec-no-bridge.k --definition no-bridge-audit-kompiled --spec-module SPEC-NO-BRIDGE'
no_bridge_output=$(
  kprove "$scratch/spec-no-bridge.k" \
    --definition "$no_bridge" \
    --spec-module SPEC-NO-BRIDGE 2>&1
)
prove_no_bridge=$?
printf '%s\n' "$no_bridge_output"
echo "no-bridge kprove exit=$prove_no_bridge"
[[ "$no_bridge_output" == *"minEvenArray"* ]]
no_bridge_residual=$?
echo "no-bridge residual minEvenArray check exit=$no_bridge_residual"
if (( prove_no_bridge == 0 )); then
  echo 'UNEXPECTED: proof closed after removing minEvenArray bridge'
  no_bridge_expected=1
else
  echo 'EXPECTED: proof is stuck after removing minEvenArray bridge'
  no_bridge_expected=0
fi

echo '$ test ! -e opposite-audit-kompiled'
test ! -e "$opposite"
clean_opposite=$?
echo "opposite clean-start exit=$clean_opposite"

echo '$ kompile --backend llvm opposite-interpretation.k --main-module OPPOSITE-INTERPRETATION --syntax-module MPY-SYNTAX --output-definition opposite-audit-kompiled'
kompile \
  --backend llvm \
  "$scratch/opposite-interpretation.k" \
  --main-module OPPOSITE-INTERPRETATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$opposite"
build_opposite=$?
echo "opposite kompile exit=$build_opposite"

echo '$ krun solution.mpy --definition opposite-audit-kompiled -cARGS=VArray(69,0,1)'
opposite_output=$(
  krun "$scratch/solution.mpy" \
    --definition "$opposite" \
    -cARGS='VArray(69,0,1)' 2>&1
)
run_opposite=$?
printf '%s\n' "$opposite_output"
echo "opposite krun exit=$run_opposite"
grep -Fq '    VList ( .Ints )' <<<"$opposite_output"
opposite_empty=$?
echo "opposite interpretation result [] check exit=$opposite_empty"

echo '$ trusted canonical and submitted Python on [2]'
python3 - "$scratch/trusted-canonical.py" "$scratch/solution.py" <<'PY'
import importlib.util
import sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck

canonical = load(sys.argv[1], "canonical_opposite")
submitted = load(sys.argv[2], "submitted_opposite")
arr = [2]
print(f"input={arr}")
print(f"canonical={canonical(arr)}")
print(f"submitted={submitted(arr)}")
raise SystemExit(0 if canonical(arr) == submitted(arr) == [2, 0] else 1)
PY
python_status=$?
echo "Python [2] comparison exit=$python_status"

overall=$((clean_no_bridge || build_no_bridge || no_bridge_residual || no_bridge_expected || clean_opposite || build_opposite || run_opposite || opposite_empty || python_status))
echo "bridge audit aggregate exit=$overall"
exit "$overall"
