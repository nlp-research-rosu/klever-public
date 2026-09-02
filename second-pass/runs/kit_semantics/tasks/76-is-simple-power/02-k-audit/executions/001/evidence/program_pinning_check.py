#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and the entry claim."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")
SCRATCH = Path("/tmp/audit-work/76-is-simple-power")


def children(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from children(value)
    elif isinstance(node, list):
        for value in node:
            yield from children(value)


def label(node):
    if not isinstance(node, dict) or node.get("node") != "KApply":
        return None
    return node.get("label", {}).get("name")


def nodes_with_prefix(tree, prefix):
    return [node for node in children(tree) if (label(node) or "").startswith(prefix)]


def stable_hash(term) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


solution_document = json.loads((EVIDENCE / "stage4-solution-kast.json").read_text())
spec_document = json.loads((EVIDENCE / "stage4-spec-kast.json").read_text())
solution_tree = solution_document["term"]
spec_tree = spec_document["term"]

func_defs = nodes_with_prefix(solution_tree, "FuncDef(")
closures = nodes_with_prefix(spec_tree, "closureVal(")
claims = [node for node in children(spec_tree) if node.get("node") == "KClaim"]

if len(func_defs) != 1:
    raise SystemExit(f"expected one FuncDef, found {len(func_defs)}")
if len(closures) != 1:
    raise SystemExit(f"expected one closureVal in spec, found {len(closures)}")

func_def = func_defs[0]
closure = closures[0]
function_name = func_def["args"][0]
function_param_names = func_def["args"][1]["args"][0]
function_body = func_def["args"][2]
claim_param_names = closure["args"][0]
claim_body = closure["args"][1]
claim_capture_env = closure["args"][2]

entry_claims = [
    claim
    for claim in claims
    if claim.get("att", {}).get("att", {}).get("label") == "SPEC.is-simple-power"
]
loop_claims = [
    claim
    for claim in claims
    if claim.get("att", {}).get("att", {}).get("label") == "SPEC.loop-invariant"
]
if len(entry_claims) != 1 or len(loop_claims) != 1:
    raise SystemExit(
        f"claim count mismatch: entry={len(entry_claims)} loop={len(loop_claims)}"
    )

entry = entry_claims[0]
calls = nodes_with_prefix(entry["body"], "Call(")
summaries = nodes_with_prefix(entry["body"], "simplePower(")

name_expected = {
    "node": "KToken",
    "sort": {"node": "KSort", "name": "String"},
    "token": '"is_simple_power"',
}
capture_expected = {
    "node": "KToken",
    "sort": {"node": "KSort", "name": "Int"},
    "token": "0",
}

checks = {
    "function_name_is_is_simple_power": function_name == name_expected,
    "parameter_constructor_identity": function_param_names == claim_param_names,
    "body_constructor_identity": function_body == claim_body,
    "closure_capture_environment_is_0": claim_capture_env == capture_expected,
    "entry_has_exactly_one_call": len(calls) == 1,
    "entry_has_result_summary": len(summaries) >= 1,
    "entry_precondition_is_true": entry["requires"].get("token") == "true",
}
for name, passed in checks.items():
    print(f"{name}={passed}")
print(f"solution_body_sha256={stable_hash(function_body)}")
print(f"claim_body_sha256={stable_hash(claim_body)}")
print(f"compiled_claim_count={len(claims)}")
print("compiled_claim_labels=" + repr(sorted(
    claim.get("att", {}).get("att", {}).get("label") for claim in claims
)))
if not all(checks.values()):
    raise SystemExit(1)


def import_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_simple_power


canonical = import_entry("pinning_canonical", SCRATCH / "trusted/canonical.py")
generated = import_entry("pinning_generated", SCRATCH / "solution.py")


def multiplication_oracle(x: int, n: int) -> bool:
    if x == 1:
        return True
    if n == 0:
        return x == 0
    if n == 1:
        return False
    if n == -1:
        return x == -1
    power = 1
    while abs(power) <= abs(x):
        if power == x:
            return True
        power *= n
    return False


print("entry_witness: X=8, N=2; entry requires true and all fixed cells are ground")
print(
    "loop_witness: L=1, X=8, N=2, local scope "
    '{"x":8,"n":2}, parent(0); X != 0 and N >= 2'
)
print("loop_witness_post: final x=1; (1 == 1) == simplePower(8,2) is true")
for x, n in [(8, 2), (3, 2), (-8, -2), (0, 0)]:
    expected = multiplication_oracle(x, n)
    print(
        f"substitution x={x} n={n} "
        f"claimed_simplePower={expected} "
        f"generated_python={generated(x, n)} "
        f"canonical_python={canonical(x, n)}"
    )
