#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the submitted implementation with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# The concrete harness has its own docstring and assertions, but its function
# signature and executable statements must remain identical to solution.py.
python3 - <<'PY'
import ast
from pathlib import Path


def function(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"), filename=path)
    return next(node for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name == "multiply")


def executable(function_def):
    body = function_def.body
    if (body and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)):
        body = body[1:]
    return ast.dump(function_def.args), ast.dump(ast.Module(body=body, type_ignores=[]))


assert executable(function("solution.py")) == executable(function("concrete-tests.py"))
PY

# Concrete execution, using the required LLVM main and syntax modules.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Symbolic definition and the universal reachability proof.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled
