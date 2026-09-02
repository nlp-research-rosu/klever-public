#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/reconstruction
semantic_def="$work/audit-semantic-kompiled"
proof_def="$work/audit-verification-kompiled"
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

cd "$work" || exit 98

run_recorded timeout 900 kompile semantic.k \
  --backend llvm \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$semantic_def"

run_recorded timeout 900 kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_def"

cases=(
  'ListExpr(Int(2), Int(4), Int(1), Int(3), Int(5), Int(7))'
  'ListExpr()'
  'ListExpr(Int(0))'
  'ListExpr(Int(-6), Int(-1), Int(-9), Int(4), Int(2))'
  'ListExpr(Int(-2), Int(-1))'
  'ListExpr(Int(2), Int(1))'
)

for input in "${cases[@]}"; do
  echo "CONCRETE_INPUT=$input"
  run_recorded timeout 120 krun solution.mpy \
    --definition "$semantic_def" \
    -cINPUT="$input"
done

echo "COMMAND: python3 canonical.py on matching concrete inputs"
python3 - <<'PY'
from canonical import largest_smallest_integers
cases = [
    [2, 4, 1, 3, 5, 7],
    [],
    [0],
    [-6, -1, -9, 4, 2],
    [-2, -1],
    [2, 1],
]
for case in cases:
    print(f"PYTHON_INPUT={case!r} PYTHON_RESULT={largest_smallest_integers(case)!r}")
PY
python_status=$?
echo "EXIT_STATUS=$python_status"
if (( python_status != 0 )); then
  overall=1
fi

echo 'POSITIVE_CLAIMS=all three claims in spec.k (setup, loop invariant, end-to-end)'
run_recorded timeout 900 kprove spec.k \
  --definition "$proof_def" \
  --spec-module SPEC

echo "OVERALL_STAGE3_STATUS=$overall"
exit "$overall"
