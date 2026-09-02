#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/rolling-max-20260729
log=/audit-output/evidence/stage3-concrete-preparation.log
: > "$log"

printf '%s\n' \
  "COMMAND: python3 -c <AST function identity check>" >> "$log"
python3 - "$scratch/solution.py" /audit-output/evidence/concrete_audit.py \
  >> "$log" 2>&1 <<'PY'
import ast
import pathlib
import sys

def function_ast(path):
    module = ast.parse(pathlib.Path(path).read_text(), filename=path)
    functions = [
        node for node in module.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    assert len(functions) == 1
    return ast.dump(functions[0], include_attributes=False)

left = function_ast(sys.argv[1])
right = function_ast(sys.argv[2])
print(f"function_ast_identical={left == right}")
raise SystemExit(0 if left == right else 1)
PY
ast_status=$?
printf 'EXIT_STATUS: %s\n' "$ast_status" >> "$log"

printf 'COMMAND: python3 /reference/py2mpy.py /audit-output/evidence/concrete_audit.py > %s/concrete-audit.mpy\n' \
  "$scratch" >> "$log"
python3 /reference/py2mpy.py /audit-output/evidence/concrete_audit.py \
  > "$scratch/concrete-audit.mpy" 2>> "$log"
translation_status=$?
printf 'EXIT_STATUS: %s\n' "$translation_status" >> "$log"

if (( ast_status == 0 && translation_status == 0 )); then
  exit 0
fi
exit 1
