from pathlib import Path
import re


program_k = Path("program.k").read_text(encoding="utf-8")
solution_mpy = Path("solution.mpy").read_text(encoding="utf-8").strip()

match = re.search(
    r"rule solutionProgram =>\n(?P<term>.*?)\nendmodule\n?\Z",
    program_k,
    flags=re.DOTALL,
)
if match is None:
    raise AssertionError("program.k does not contain the solutionProgram rule")

embedded = "\n".join(
    line[4:] if line.startswith("    ") else line
    for line in match.group("term").splitlines()
).strip()

if embedded != solution_mpy:
    raise AssertionError(
        "solutionProgram differs from solution.mpy\n"
        f"--- embedded ---\n{embedded}\n"
        f"--- generated ---\n{solution_mpy}\n"
    )

print("program identity: solutionProgram == solution.mpy")
