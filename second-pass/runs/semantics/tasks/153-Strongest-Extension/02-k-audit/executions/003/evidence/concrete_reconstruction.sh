#!/usr/bin/env bash
set -u

cd /tmp/audit-work/concrete || exit 97

echo "BEGIN prepare"
echo "COMMAND python3 /tmp/audit-work/trusted/py2mpy.py concrete-audit.py > concrete-audit.mpy"
python3 /tmp/audit-work/trusted/py2mpy.py concrete-audit.py > concrete-audit.mpy
translate_status=$?
echo "EXIT translate $translate_status"
if [[ $translate_status -ne 0 ]]; then
  exit 1
fi

echo "COMMAND python3 AST-prefix comparison"
python3 - <<'PY'
import ast
from pathlib import Path

solution = ast.parse(Path("/tmp/audit-work/candidate/solution.py").read_text())
test_module = ast.parse(Path("concrete-audit.py").read_text())
assert ast.dump(solution) == ast.dump(
    ast.Module(body=test_module.body[:2], type_ignores=[])
)
print("concrete_program_function_prefix=MATCH")
PY
ast_status=$?
echo "EXIT ast_prefix $ast_status"
if [[ $ast_status -ne 0 ]]; then
  exit 1
fi

echo "BEGIN build_concrete"
echo "COMMAND kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-2-kompiled"
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-2-kompiled
build_status=$?
echo "EXIT build_concrete $build_status"
if [[ $build_status -ne 0 ]]; then
  exit 1
fi

echo "BEGIN run_concrete"
echo "COMMAND krun concrete-audit.mpy --definition audit-runtime-2-kompiled --output pretty"
krun concrete-audit.mpy \
  --definition audit-runtime-2-kompiled \
  --output pretty 2>&1 | tee concrete-audit.out
run_status=${PIPESTATUS[0]}
echo "EXIT run_concrete $run_status"
if [[ $run_status -ne 0 ]]; then
  exit 1
fi
if ! rg -Uq '<k>\s+\.K\s+</k>' concrete-audit.out; then
  echo "FINAL_K_NOT_EMPTY"
  exit 1
fi
if ! rg -Uq '<exc>\s+NoExc\s+</exc>' concrete-audit.out; then
  echo "FINAL_EXCEPTION_NOT_CLEAR"
  exit 1
fi
if ! rg -Uq '<exit-code>\s+0\s+</exit-code>' concrete-audit.out; then
  echo "FINAL_EXIT_NOT_ZERO"
  exit 1
fi
echo "CONCRETE_RECONSTRUCTION_PASS"
