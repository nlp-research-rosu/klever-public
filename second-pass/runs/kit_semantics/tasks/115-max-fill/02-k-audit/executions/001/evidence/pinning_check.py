#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and spec.k."""

from pathlib import Path
import re


def balanced_term(text, marker):
    start = text.index(marker)
    open_paren = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced term beginning {marker!r}")


def normalize(text):
    return re.sub(r"\s+", "", text)


mpy = Path("/tmp/audit-work/regenerated-solution.mpy").read_text()
spec = Path("/tmp/audit-work/spec.k").read_text()
submitted = Path("/candidate/solution.mpy").read_text()

func = balanced_term(mpy, 'FuncDef("max_fill"')
params = balanced_term(func, 'Params("grid", "capacity")')
body_start = func.index(params) + len(params)
body_start = func.index(",", body_start) + 1
body = func[body_start:-1].strip()

expected_closure = (
    'closureVal(("grid", "capacity"),' + body + ",0)"
)

augassign = balanced_term(body, "AugAssign(")

submitted_identity = submitted == mpy
closure_occurrences = normalize(spec).count(normalize(expected_closure))
body_occurrences = normalize(spec).count(normalize(body))
augassign_occurrences = normalize(spec).count(normalize(augassign))

print(f"TRANSLATED_BYTE_IDENTITY={submitted_identity}")
print(f"EXPECTED_CLOSURE_OCCURRENCES_IN_SPEC={closure_occurrences}")
print(f"EXACT_BODY_OCCURRENCES_IN_SPEC={body_occurrences}")
print(f"EXACT_AUGASSIGN_OCCURRENCES_IN_SPEC={augassign_occurrences}")
print("EXPECTED_CLOSURE_NORMALIZED=" + normalize(expected_closure))

ok = (
    submitted_identity
    and closure_occurrences == 1
    and body_occurrences == 1
    and augassign_occurrences >= 2
)
raise SystemExit(0 if ok else 1)
