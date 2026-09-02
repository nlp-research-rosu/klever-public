#!/usr/bin/env python3
import ast
import sys
from pathlib import Path

solution = ast.parse(Path(sys.argv[1]).read_text())
runtime_tests = ast.parse(Path(sys.argv[2]).read_text())
prefix = ast.Module(
    body=runtime_tests.body[: len(solution.body)],
    type_ignores=[],
)
assert ast.dump(solution) == ast.dump(prefix)
print(
    f"AST prefix identity: {len(solution.body)} submitted top-level nodes "
    f"followed by {len(runtime_tests.body) - len(solution.body)} reviewer assertions"
)
