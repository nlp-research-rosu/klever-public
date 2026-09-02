#!/usr/bin/env bash
set -euo pipefail

# Regenerate the translator artifact and the concrete smoke-test program.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Ensure the function exercised by krun is AST-identical to the deliverable.
python3 - <<'PY'
import ast
from pathlib import Path


def function_ast(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    return ast.dump(function, include_attributes=False)


assert function_ast("solution.py") == function_ast("concrete_tests.py")
print("concrete test function AST matches solution.py")
PY

# Concrete execution uses the required MPY-KRUN/MPY-SYNTAX LLVM definition.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Symbolic verification imports MPY, excluding the concrete-only extensions.
kompile verification.k \
  --backend haskell \
  --main-module STRING-XOR-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module STRING-XOR-SPEC \
  --claims STRING-XOR-SPEC.loop-invariant,STRING-XOR-SPEC.solution-correct
