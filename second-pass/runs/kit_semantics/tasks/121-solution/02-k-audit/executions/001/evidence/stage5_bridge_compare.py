#!/usr/bin/env python3
"""Mechanical context checks for the sole operational bridge."""

from __future__ import annotations

import hashlib
import pathlib
import re


WORK = pathlib.Path("/tmp/audit-work/reconstruction")


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


def balanced_call(text: str, marker: str) -> str:
    start = text.index(marker)
    open_index = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
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
    raise RuntimeError(f"unbalanced {marker}")


def split_args(call: str) -> list[str]:
    inside = call[call.index("(") + 1 : -1]
    parts: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(inside):
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
        elif char == "," and depth == 0:
            parts.append(inside[start:index])
            start = index + 1
    parts.append(inside[start:])
    return parts


verification = (WORK / "verification.k").read_text()
connection = (WORK / "connection-spec.k").read_text()
spec = (WORK / "spec.k").read_text()

guard = "requires allInts(REST) andBool POSITION >=Int 0"


def bridge_contract(text: str) -> str:
    start = text.index("<k>")
    end = text.index(guard, start) + len(guard)
    return normalized(text[start:end])


rule_contract = bridge_contract(verification)
claim_contract = bridge_contract(connection)
print("bridge_contract_sha256", hashlib.sha256(rule_contract.encode()).hexdigest())
print("connection_contract_sha256", hashlib.sha256(claim_contract.encode()).hexdigest())
print("exact_match_domain_and_rewrite", rule_contract == claim_contract)

spec_for = balanced_call(spec, "For")
bridge_loop = balanced_call(verification, "#loop")
spec_body = split_args(spec_for)[2].replace(".Stmts", "")
bridge_body = split_args(bridge_loop)[2].replace(".Stmts", "")
spec_body_norm = normalized(spec_body)
bridge_body_norm = normalized(bridge_body)
print("spec_for_body_sha256", hashlib.sha256(spec_body_norm.encode()).hexdigest())
print("bridge_loop_body_sha256", hashlib.sha256(bridge_body_norm.encode()).hexdigest())
print("exact_real_loop_body", spec_body_norm == bridge_body_norm)

print(
    "connection_imports_bridge",
    'requires "verification.k"' in connection
    or "imports VERIFICATION\n" in connection,
)
if (
    rule_contract != claim_contract
    or spec_body_norm != bridge_body_norm
    or 'requires "verification.k"' in connection
    or "imports VERIFICATION\n" in connection
):
    raise SystemExit(1)
