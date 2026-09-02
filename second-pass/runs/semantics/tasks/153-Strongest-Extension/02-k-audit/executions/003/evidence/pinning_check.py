#!/usr/bin/env python3
"""Mechanical constructor-level source-to-proof pinning checks."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
mpy = (ROOT / "solution.mpy").read_text()
verification = (ROOT / "verification.k").read_text()
spec = (ROOT / "spec.k").read_text()


def matching_paren(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(opening, len(text)):
        character = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"unclosed parenthesis at {opening}")


def top_level_segments(term: str) -> list[str]:
    opening = term.index("(")
    closing = matching_paren(term, opening)
    body = term[opening + 1 : closing]
    segments = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, character in enumerate(body):
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character in "([":
            depth += 1
        elif character in ")]":
            depth -= 1
        elif character == "," and depth == 0:
            segments.append(body[start:index])
            start = index + 1
    segments.append(body[start:])
    return segments


def function_parts(name: str):
    marker = f'FuncDef("{name}"'
    start = mpy.index(marker)
    opening = mpy.index("(", start)
    closing = matching_paren(mpy, opening)
    term = mpy[start : closing + 1]
    parts = top_level_segments(term)
    if len(parts) < 3:
        raise AssertionError(f"malformed FuncDef for {name}")
    return parts[1], "".join(parts[2:])


def alias_rhs(name: str) -> str:
    match = re.search(rf"\brule\s+{re.escape(name)}\s*=>", verification)
    if not match:
        raise AssertionError(f"missing alias rule {name}")
    tail = verification[match.end() :]
    end = re.search(r"\n\s*\n  (?=(?:rule|syntax|endmodule)\b)", tail)
    if not end:
        raise AssertionError(f"cannot find end of alias rule {name}")
    return tail[: end.start()]


def normalized(term: str) -> str:
    result = re.sub(r"\s+", "", term)
    # The translator pretty-printer leaves empty variadic tails blank, while K
    # source spells the corresponding constructor identities explicitly.
    result = result.replace(",.Exprs)", ",)")
    result = result.replace(",.Stmts)", ",)")
    return result


def expanded_alias(name: str) -> str:
    result = normalized(alias_rhs(name))
    nested_aliases = {
        "extensionStrengthBody": ["characterStrengthBody"],
        "strongestExtensionBody": ["selectionLoopBody"],
    }
    for nested in nested_aliases.get(name, []):
        result = result.replace(nested, normalized(alias_rhs(nested)))
    return result


checks = [
    ("_extension_strength", "extensionStrengthBody", 'Params("extension")'),
    (
        "Strongest_Extension",
        "strongestExtensionBody",
        'Params("class_name","extensions")',
    ),
]

for function_name, alias, expected_params in checks:
    params, source_body = function_parts(function_name)
    proof_body = expanded_alias(alias)
    params_match = normalized(params) == expected_params
    body_match = normalized(source_body) == proof_body
    print(
        f"function={function_name} alias={alias} "
        f"params_match={params_match} body_match={body_match}"
    )
    if not (params_match and body_match):
        print(f"source_body={normalized(source_body)}")
        print(f"proof_body={normalized(proof_body)}")
        raise SystemExit(1)

binding_fragments = [
    '["_extension_strength"<-closureVal(("extension",.ParamNames),extensionStrengthBody,0)]',
    '["Strongest_Extension"<-closureVal(("class_name","extensions",.ParamNames),strongestExtensionBody,0)]',
]
normalized_verification = normalized(verification)
for fragment in binding_fragments:
    present = fragment in normalized_verification
    print(f"solution_scope_binding={fragment} present={present}")
    if not present:
        raise SystemExit(1)

entry_call = normalized(
    """Call(
      Name("Strongest_Extension"),
      str(CLASS:IntSeq),
      list(vCons(
        str(E1:IntSeq),
        vCons(str(E2:IntSeq),
        vCons(str(E3:IntSeq), .ValSeq)))))"""
)
entry_binding = normalized(
    """<env> 0 </env>
    <scopes>
      (0 |-> solutionScope)
      (-1 |-> builtinsScope)
    </scopes>"""
)
print(f"entry_call_exactly_three_present={entry_call in normalized(spec)}")
print(f"entry_solution_scope_present={entry_binding in normalized(spec)}")
if entry_call not in normalized(spec) or entry_binding not in normalized(spec):
    raise SystemExit(1)


def load_function(module_name: str, path: Path):
    module_spec = importlib.util.spec_from_file_location(module_name, path)
    assert module_spec and module_spec.loader
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.Strongest_Extension


canonical = load_function("canonical_for_pinning", Path("/reference/canonical.py"))
candidate = load_function("candidate_for_pinning", ROOT / "solution.py")


def proof_strength(text: str) -> int:
    # The proof's isUpperC/isLowerC primitives operate over ASCII codes.
    return sum(
        (1 if "A" <= character <= "Z" else 0)
        - (1 if "a" <= character <= "z" else 0)
        for character in text
    )


def claimed_result(class_name: str, extensions: list[str]) -> str:
    best = extensions[0]
    best_strength = proof_strength(best)
    for extension in extensions:
        strength = proof_strength(extension)
        if strength > best_strength:
            best = extension
            best_strength = strength
    return class_name + "." + best


witness_class = "my_class"
witness_extensions = ["AA", "Be", "CC"]
summary = claimed_result(witness_class, witness_extensions)
trusted = canonical(witness_class, witness_extensions)
actual = candidate(witness_class, witness_extensions)
print(
    "entry_witness="
    f"{(witness_class, witness_extensions)!r} "
    f"claimed={summary!r} canonical={trusted!r} candidate={actual!r}"
)
if not (summary == trusted == actual == "my_class.AA"):
    raise SystemExit(1)

print(
    "character_claim_witness="
    "CURRENT=65 REST=.IntSeq ALL=iCons(65,.IntSeq) ACC=0 PREV=.IntSeq"
)
print(
    "helper_claim_witness="
    'CS=iCons(65,.IntSeq) LOCALS=.Map and "_extension_strength" not in LOCALS'
)
print(
    "selection_claim_witness="
    'E1="a" E2="A" E3="" BEST="a" BESTS=-1 LAST="a" SCORE=-1'
)
print(
    "entry_claim_witness="
    'CLASS="my_class" E1="AA" E2="Be" E3="CC" with fixed initial cells'
)
