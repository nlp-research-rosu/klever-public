import ast
from pathlib import Path


def compact_k(text):
    output = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    # The translator prints an empty statement sequence as the empty field
    # between a comma and ")", while K pretty syntax also accepts `.Stmts`.
    return "".join(output).replace(",.Stmts)", ",)")


translated = Path("solution.mpy").read_text(encoding="utf-8").strip()
specification = Path("spec.k").read_text(encoding="utf-8")
marker = "#loadAll("
start = specification.index(marker) + len(marker)

depth = 1
quoted = False
escaped = False
end = None
for offset, char in enumerate(specification[start:], start=start):
    if quoted:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            quoted = False
        continue
    if char == '"':
        quoted = True
    elif char == "(":
        depth += 1
    elif char == ")":
        depth -= 1
        if depth == 0:
            end = offset
            break

if end is None:
    raise SystemExit("program identity: unmatched #loadAll parenthesis")

embedded = specification[start:end]
if compact_k(translated) != compact_k(embedded):
    raise SystemExit("program identity: solution.mpy differs from spec.k")

solution_ast = ast.parse(Path("solution.py").read_text(encoding="utf-8"))
tests_ast = ast.parse(Path("concrete_tests.py").read_text(encoding="utf-8"))
solution_function = next(
    node for node in solution_ast.body if isinstance(node, ast.FunctionDef)
)
tests_function = next(
    node for node in tests_ast.body if isinstance(node, ast.FunctionDef)
)
if ast.dump(solution_function) != ast.dump(tests_function):
    raise SystemExit(
        "program identity: concrete_tests.py has a different search body"
    )

print("program identity: PASS")
