#!/usr/bin/env python3
"""Generate constructor-level pinning claims from the trusted translator AST."""

from __future__ import annotations

import ast
import argparse
import importlib.util
import symtable
from pathlib import Path


ROOT = Path("/tmp/audit-work/119-match-parens")
TRANSLATOR = ROOT / "py2mpy.py"

parser = argparse.ArgumentParser()
parser.add_argument("--source", type=Path, default=ROOT / "solution.py")
parser.add_argument("--requires", default="verification.k")
parser.add_argument("--output", type=Path, default=ROOT / "pinning-spec.k")
parser.add_argument("--module", default="PROGRAM-PINNING-SPEC")
parser.add_argument("--imports", default="MATCH-PARENS-VERIFICATION")
args = parser.parse_args()
SOURCE = args.source
OUTPUT = args.output


def load_translator():
    spec = importlib.util.spec_from_file_location("trusted_py2mpy_for_pinning", TRANSLATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load trusted translator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


py2mpy = load_translator()
source_text = SOURCE.read_text()
tree = ast.parse(source_text, filename=str(SOURCE))
py2mpy.SCOPES.clear()
py2mpy._walk_symtable(symtable.symtable(source_text, str(SOURCE), "exec"))
translated = py2mpy.emit_module(tree)

functions = {}
for item in translated.args[0].items:
    if isinstance(item, py2mpy.Ctor) and item.name == "FuncDef":
        name = ast.literal_eval(item.args[0])
        functions[name] = item

if set(functions) != {"is_good", "match_parens"}:
    raise RuntimeError(f"unexpected function set: {set(functions)!r}")

is_good = functions["is_good"]
match_parens = functions["match_parens"]
is_good_body = is_good.args[-1]
match_body = match_parens.args[-1]
loop_body = None
for statement in is_good_body.items:
    if isinstance(statement, py2mpy.Ctor) and statement.name == "For":
        loop_body = statement.args[2]
        break


def rendered(term) -> str:
    """Render the translator term with explicit .Stmts list units.

    The translator's empty-list surface spelling is valid in a .mpy program,
    but proof-claim parsing is less permissive in nested trailing arguments.
    Explicit units preserve exactly the same constructor/list term.
    """
    if isinstance(term, str):
        return term
    if isinstance(term, py2mpy.Seq):
        prefix = " ".join(rendered(item) for item in term.items)
        return f"{prefix} .Stmts" if prefix else ".Stmts"
    if isinstance(term, py2mpy.Ctor):
        return f"{term.name}(" + ", ".join(rendered(arg) for arg in term.args) + ")"
    raise TypeError(type(term))


def configuration_claim(label: str, left: str, right: str) -> str:
    return f'''  claim
    <k> {left} => {right} </k>
    <env> ENV:Int </env>
    <scopes> SCOPES:Map </scopes>
    <scopeLoc> SCOPELOC:Int </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> RET:RetState </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EXITCODE:Int </exit-code>
    [label({label})]
'''


claims = []
if loop_body is not None:
    claims.append(configuration_claim("pinIsGoodLoopBody", "isGoodLoopBody", rendered(loop_body)))
claims.extend(
    [
        configuration_claim("pinIsGoodBody", "isGoodBody", rendered(is_good_body)),
        configuration_claim("pinMatchParensBody", "matchParensBody", rendered(match_body)),
        configuration_claim(
            "pinIsGoodClosure",
            "isGoodClosure",
            f'closureVal(("s", .ParamNames), {rendered(is_good_body)}, 0)',
        ),
        configuration_claim(
            "pinMatchParensClosure",
            "matchParensClosure",
            f'closureVal(("lst", .ParamNames), {rendered(match_body)}, 0)',
        ),
    ]
)

spec_text = f'''requires "{args.requires}"

module {args.module}
  imports {args.imports}

  // All right-hand sides below are generated from solution.py by the trusted
  // translator's constructor tree, not copied from verification.k.
{''.join(claims)}
endmodule
'''
OUTPUT.write_text(spec_text)
print(f"generated {OUTPUT}")
print(f"functions={sorted(functions)}")
print(f"source-derived claims={len(claims)}")
