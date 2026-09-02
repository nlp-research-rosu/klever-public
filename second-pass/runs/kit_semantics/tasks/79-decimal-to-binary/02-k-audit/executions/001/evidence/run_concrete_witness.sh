#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/79-audit/source
cd "$scratch" || exit 1

echo '$ Python AST comparison: runtime-witness function vs submitted solution function'
python3 - <<'PY'
import ast
from pathlib import Path

def function(path):
    tree = ast.parse(Path(path).read_text(), filename=path)
    return next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "decimal_to_binary"
    )

submitted = function("/candidate/solution.py")
witness = function("/audit-output/evidence/runtime-witness.py")
assert ast.dump(submitted, include_attributes=False) == ast.dump(
    witness, include_attributes=False
)
print("RUNTIME_WITNESS_BODY_AST_MATCH=true")
PY
ast_status=$?
echo "AST_COMPARE_EXIT_STATUS=$ast_status"

echo '$ cp /audit-output/evidence/runtime-witness.py runtime-witness.py'
cp /audit-output/evidence/runtime-witness.py "$scratch/runtime-witness.py"
copy_status=$?
echo "COPY_EXIT_STATUS=$copy_status"

echo '$ python3 py2mpy.py runtime-witness.py > runtime-witness.mpy'
python3 py2mpy.py runtime-witness.py > runtime-witness.mpy
translate_status=$?
echo "TRANSLATE_EXIT_STATUS=$translate_status"

echo '$ krun runtime-witness.mpy --definition fresh-runtime-kompiled'
krun runtime-witness.mpy --definition fresh-runtime-kompiled
krun_status=$?
echo "KRUN_EXIT_STATUS=$krun_status"

if (( ast_status || copy_status || translate_status || krun_status )); then
  exit 1
fi
echo 'CONCRETE_WITNESS=PASS'
