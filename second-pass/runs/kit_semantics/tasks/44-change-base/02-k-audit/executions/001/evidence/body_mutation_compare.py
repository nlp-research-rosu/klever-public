#!/usr/bin/env python3
import json
from pathlib import Path


def walk(term):
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def label_name(term):
    if not isinstance(term, dict) or term.get("node") != "KApply":
        return None
    return term.get("label", {}).get("name")


def one_closure_body(path: Path, claim_label: str):
    data = json.loads(path.read_text())
    module = data["term"]["term"][0]
    claims = [
        claim
        for claim in module["localSentences"]
        if claim["att"]["att"].get("label") == claim_label
    ]
    if len(claims) != 1:
        raise RuntimeError(f"{path}: claims matching {claim_label}: {len(claims)}")
    closures = [
        term
        for term in walk(claims[0]["body"])
        if label_name(term)
        == "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
    ]
    if len(closures) != 1:
        raise RuntimeError(f"{path}: closures: {len(closures)}")
    return closures[0]["args"][1]


def differences(left, right, path="$"):
    if type(left) is not type(right):
        return [(path, left, right)]
    if isinstance(left, dict):
        diffs = []
        for key in sorted(set(left) | set(right)):
            if key not in left or key not in right:
                diffs.append((f"{path}.{key}", left.get(key), right.get(key)))
            else:
                diffs.extend(differences(left[key], right[key], f"{path}.{key}"))
        return diffs
    if isinstance(left, list):
        if len(left) != len(right):
            return [(f"{path}.length", len(left), len(right))]
        diffs = []
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            diffs.extend(
                differences(left_item, right_item, f"{path}[{index}]")
            )
        return diffs
    return [] if left == right else [(path, left, right)]


original = one_closure_body(
    Path("/tmp/audit-work/44-change-base/spec-parsed.json"),
    "SPEC.change-base",
)
mutated = one_closure_body(
    Path("/tmp/audit-work/44-change-base/body-mutation-parsed.json"),
    "FRESH-BODY-MUTATION-SPEC.changed-executed-body",
)
diffs = differences(original, mutated)
print(f"constructor_differences={len(diffs)}")
for path, left, right in diffs:
    print(f"DIFF path={path} original={left!r} mutated={right!r}")
expected = (
    len(diffs) == 1
    and diffs[0][1] == "48"
    and diffs[0][2] == "49"
)
print(f"exactly_digit_offset_48_to_49={expected}")
raise SystemExit(0 if expected else 1)
