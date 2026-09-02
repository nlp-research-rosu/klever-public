import ast
import subprocess
from pathlib import Path


workspace = Path(__file__).resolve().parent

generated = subprocess.run(
    ["python3", "py2mpy.py", "solution.py"],
    cwd=workspace,
    check=True,
    capture_output=True,
    text=True,
).stdout
recorded = (workspace / "solution.mpy").read_text(encoding="utf-8")
if generated != recorded:
    raise SystemExit("solution.mpy is stale")

solution_tree = ast.parse(
    (workspace / "solution.py").read_text(encoding="utf-8")
)
smoke_tree = ast.parse(
    (workspace / "smoke.py").read_text(encoding="utf-8")
)
solution_function = solution_tree.body[0]
smoke_function = smoke_tree.body[0]
if ast.dump(solution_function) != ast.dump(smoke_function):
    raise SystemExit("smoke.py does not contain the exact solution function")

print("artifact checks: PASS")
