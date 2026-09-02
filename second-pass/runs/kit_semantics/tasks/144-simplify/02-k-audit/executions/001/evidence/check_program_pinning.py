#!/usr/bin/env python3
"""Independent constructor-level source/claim pinning check."""

from __future__ import annotations

import ast
import importlib.util
import re
import symtable
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/144-simplify")


def load_translator(path: Path):
    spec = importlib.util.spec_from_file_location("trusted_py2mpy", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def token_form(text: str) -> tuple[str, ...]:
    """Discard whitespace but preserve every constructor token and literal."""
    token = re.compile(
        r'"(?:\\.|[^"\\])*"'
        r"|[A-Za-z_#][A-Za-z0-9_#-]*"
        r"|\.[A-Za-z][A-Za-z0-9]*"
        r"|-?[0-9]+"
        r"|=>|==K|[(),]"
    )
    result = tuple(token.findall(text))
    residue = token.sub("", text)
    if not residue.isspace() and residue:
        raise AssertionError(f"unrecognized term text: {residue!r}")
    return result


translator = load_translator(SCRATCH / "py2mpy.py")
source = (SCRATCH / "solution.py").read_text(encoding="utf-8")
tree = ast.parse(source, filename="solution.py")
assert len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef)
function = tree.body[0]
assert function.name == "simplify"
assert [arg.arg for arg in function.args.args] == ["x", "n"]

translator.SCOPES.clear()
translator._walk_symtable(
    symtable.symtable(source, "solution.py", "exec")
)
function_term = translator.emit_stmt(function)
trusted_body_text = translator.render(function_term.args[-1])
trusted_module_text = translator.render(translator.emit_module(tree)) + "\n"
stored_module_text = (SCRATCH / "solution.mpy").read_text(encoding="utf-8")

verification = (SCRATCH / "verification.k").read_text(encoding="utf-8")
loop_match = re.search(
    r"\n  rule simplifyLoopBody =>\n(.*?)"
    r"\n\n  rule simplifyReturn =>",
    verification,
    flags=re.DOTALL,
)
return_match = re.search(
    r"\n  rule simplifyReturn =>\n(.*?)"
    r"\n\n  rule simplifyBody =>",
    verification,
    flags=re.DOTALL,
)
body_match = re.search(
    r"\n  rule simplifyBody =>\n(.*?)"
    r"\n\n  rule simplifyScope",
    verification,
    flags=re.DOTALL,
)
assert loop_match and return_match and body_match
proof_body_text = body_match.group(1)
proof_body_text = proof_body_text.replace(
    "simplifyLoopBody", loop_match.group(1)
)
proof_body_text = proof_body_text.replace(
    "simplifyReturn", return_match.group(1)
)

# The translator omits the explicit associative-list units accepted by K.
def remove_list_units(tokens: tuple[str, ...]) -> tuple[str, ...]:
    result: list[str] = []
    for value in tokens:
        if value == ".Exprs":
            # `Call(F, X, .Exprs)` and `Call(F, X)` are the same
            # right-associated argument sequence.
            assert result and result[-1] == ","
            result.pop()
            continue
        if value == ".Stmts":
            continue
        result.append(value)
    return tuple(result)


stored_identity = trusted_module_text == stored_module_text
body_identity = remove_list_units(token_form(trusted_body_text)) == (
    remove_list_units(token_form(proof_body_text))
)
claim_has_exact_closure = bool(
    re.search(
        r'toCall\(closureVal\(\("x",\s*"n"\),\s*'
        r"simplifyBody,\s*0\)\)",
        (SCRATCH / "spec.k").read_text(encoding="utf-8"),
    )
)

print(f"stored_module_byte_identity={stored_identity}")
print(f"proof_body_constructor_identity={body_identity}")
print(f"entry_claim_exact_params_body_scope={claim_has_exact_closure}")
status = 0 if all(
    (stored_identity, body_identity, claim_has_exact_closure)
) else 1
print(f"EXIT_STATUS: {status}")
raise SystemExit(status)
