import ast
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def function_ast(path, name):
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.dump(node, include_attributes=False)
    raise AssertionError(f"{name} is missing from {path}")


solution_function = function_ast(ROOT / "solution.py", "remove_vowels")
test_function = function_ast(ROOT / "concrete-tests.py", "remove_vowels")
assert solution_function == test_function

for source_name, translated_name in [
    ("solution.py", "solution.mpy"),
    ("concrete-tests.py", "concrete-tests.mpy"),
]:
    translated = subprocess.run(
        [sys.executable, "py2mpy.py", source_name],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    recorded = (ROOT / translated_name).read_text(encoding="utf-8")
    assert translated == recorded, f"{translated_name} is stale"

print("artifact checks: function bodies match; translations are current")
