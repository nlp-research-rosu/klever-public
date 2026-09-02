#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

spec_path = Path("/tmp/audit-work/src/spec.k")
solution_path = Path("/tmp/audit-work/src/solution.mpy")
derived_path = Path("/tmp/audit-work/pinning/claim-body.mpy")
definition = "/tmp/audit-work/build/semantic-kompiled"

text = spec_path.read_text()
binding_marker = '"how_many_times" |->'
binding_at = text.index(binding_marker)
start = text.index("function(", binding_at)

depth = 0
quoted = False
escaped = False
end = None
for index in range(start, len(text)):
    char = text[index]
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
            end = index + 1
            break

assert end is not None
function_term = text[start:end]
assert function_term.startswith("function(") and function_term.endswith(")")
function_arguments = function_term[len("function(") : -1]
unit_count = function_arguments.count(".Stmts")
# `.Stmts` is the explicit K unit used in the claim. The concrete list grammar
# represents that same constructor by an empty token sequence.
concrete_arguments = function_arguments.replace(".Stmts", "")
print(f"EXPLICIT_STMTS_UNITS_NORMALIZED: {unit_count}")
derived_text = f'Module(FuncDef("how_many_times", {concrete_arguments}))\n'
derived_path.parent.mkdir(parents=True, exist_ok=True)
derived_path.write_text(derived_text)


def parse(path: Path):
    command = [
        "kast",
        str(path),
        "--definition",
        definition,
        "--sort",
        "Program",
        "--output",
        "json",
    ]
    print("COMMAND:", " ".join(command))
    result = subprocess.run(command, text=True, capture_output=True)
    print(f"KAST_EXIT_STATUS {path.name}: {result.returncode}")
    if result.stderr:
        print(result.stderr, end="")
    assert result.returncode == 0
    return json.loads(result.stdout)


submitted_ast = parse(solution_path)
claim_ast = parse(derived_path)
equal = submitted_ast == claim_ast
submitted_bytes = json.dumps(submitted_ast, sort_keys=True).encode()
claim_bytes = json.dumps(claim_ast, sort_keys=True).encode()
print(f"SUBMITTED_SHA256_TERM_JSON: {hashlib.sha256(submitted_bytes).hexdigest()}")
print(f"CLAIM_SHA256_TERM_JSON: {hashlib.sha256(claim_bytes).hexdigest()}")
print(f"CONSTRUCTOR_AST_EQUAL: {equal}")
assert equal
