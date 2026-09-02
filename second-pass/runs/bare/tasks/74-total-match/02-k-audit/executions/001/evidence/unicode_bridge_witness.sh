#!/usr/bin/env bash
set -uo pipefail

echo "Python executions for lst1=['🙂'], lst2=['ab']"
python3 - <<'PY'
import importlib.util

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.total_match

canonical = load("/tmp/audit-work/reference/canonical.py", "unicode_canonical")
generated = load("/tmp/audit-work/src/solution.py", "unicode_generated")
left = ["🙂"]
right = ["ab"]
print("lengths:", sum(map(len, left)), sum(map(len, right)))
print("canonical:", canonical(left, right))
print("generated:", generated(left, right))
PY

k_args='args(pyList(pyStr("\U0001f642") :: .StrVals),pyList(pyStr("ab") :: .StrVals))'

echo "Fresh LLVM semantics execution"
krun /tmp/audit-work/src/solution.mpy \
  --definition /tmp/audit-work/build/semantic-kompiled \
  "-cARGS=$k_args"
llvm_status=$?
echo "LLVM_KRUN_EXIT: $llvm_status"

echo "Fresh Haskell proof-definition execution"
krun /tmp/audit-work/src/solution.mpy \
  --definition /tmp/audit-work/build/verification-kompiled \
  "-cARGS=$k_args"
haskell_status=$?
echo "HASKELL_KRUN_EXIT: $haskell_status"

if (( llvm_status != 0 || haskell_status != 0 )); then
  exit 1
fi
