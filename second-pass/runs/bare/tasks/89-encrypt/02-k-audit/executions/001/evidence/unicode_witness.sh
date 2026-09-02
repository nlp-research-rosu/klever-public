#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/source || exit 99

echo "Actual Python and canonical outcomes:"
run python3 - <<'PY'
from canonical import encrypt as canonical
from solution import encrypt as generated

value = "🙂"
print("input", repr(value))
print("generated", repr(generated(value)))
print("canonical", repr(canonical(value)))
PY
python_status=$?

echo "Fresh LLVM semantics outcome:"
run krun solution.mpy \
  -cINPUT='"🙂"' \
  --definition /tmp/audit-work/build/concrete-kompiled
llvm_status=$?

echo "Fresh Haskell/proof semantics outcome:"
run krun solution.mpy \
  -cINPUT='"🙂"' \
  --definition /tmp/audit-work/build/proof-kompiled
haskell_status=$?

printf 'summary python=%d llvm=%d haskell=%d\n' \
  "$python_status" "$llvm_status" "$haskell_status"
if (( python_status || llvm_status || haskell_status )); then
  exit 1
fi
