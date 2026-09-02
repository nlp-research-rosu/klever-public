from pathlib import Path


def compact(path):
    return "".join(Path(path).read_text(encoding="utf-8").split())


def first_constructor(term, name):
    start = term.index(name + "(")
    depth = 0
    for index in range(start + len(name), len(term)):
        char = term[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return term[start : index + 1]
    raise ValueError(f"unterminated {name} constructor")


translated = compact("solution.mpy")
formal_claim = compact("spec.k")
concrete_tests = compact("concrete-tests.mpy")

assert translated in formal_claim, "spec.k does not load the exact solution.mpy term"
function_term = first_constructor(translated, "FuncDef")
assert function_term in concrete_tests, (
    "concrete-tests.mpy does not use the exact translated function"
)

print("Artifact identity: solution.mpy == spec program; concrete body matches")
