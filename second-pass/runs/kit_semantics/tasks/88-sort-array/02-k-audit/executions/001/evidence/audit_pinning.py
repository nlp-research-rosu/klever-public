#!/usr/bin/env python3
"""Constructor-level comparison of solution.mpy with both entry claims."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterator


ROOT = Path("/tmp/audit-work/reconstruction")


def walk(term: Any) -> Iterator[dict[str, Any]]:
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def label(term: dict[str, Any]) -> str:
    value = term.get("label")
    if not isinstance(value, dict):
        return ""
    return value.get("name", "")


def stable_digest(term: Any) -> str:
    return hashlib.sha256(
        json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def token(term: dict[str, Any]) -> str:
    assert term["node"] == "KToken"
    return term["token"]


def main() -> None:
    solution = json.loads((ROOT / "solution-kast.json").read_text())
    funcs = [
        term
        for term in walk(solution["term"])
        if term.get("node") == "KApply" and label(term).startswith("FuncDef(")
    ]
    assert len(funcs) == 1
    function = funcs[0]
    assert token(function["args"][0]) == '"sort_array"'
    params_wrapper = function["args"][1]
    assert label(params_wrapper).startswith("Params(")
    source_params = params_wrapper["args"][0]
    source_body = function["args"][2]

    spec = json.loads((ROOT / "spec-all.json").read_text())
    claims = [
        term for term in walk(spec["term"]) if term.get("node") == "KClaim"
    ]
    assert len(claims) == 2

    checked = 0
    for claim in claims:
        attributes = claim.get("att", {}).get("att", {})
        claim_label = attributes.get("label", f"claim-{checked}")
        closures = [
            term
            for term in walk(claim["body"])
            if term.get("node") == "KApply"
            and label(term).startswith("closureVal(")
        ]
        assert len(closures) == 1
        closure = closures[0]
        assert closure["args"][0] == source_params
        assert closure["args"][1] == source_body
        assert token(closure["args"][2]) == "0"

        top_rewrites = [
            term
            for term in walk(claim["body"])
            if term.get("node") == "KRewrite"
            and term["lhs"].get("node") == "KApply"
            and label(term["lhs"]).startswith("Call(")
        ]
        assert len(top_rewrites) == 1
        call = top_rewrites[0]["lhs"]
        call_names = [
            term
            for term in walk(call)
            if term.get("node") == "KToken"
            and term.get("sort", {}).get("name") == "String"
        ]
        assert token(call_names[0]) == '"sort_array"'
        refs = [
            term
            for term in walk(call)
            if term.get("node") == "KApply" and label(term).startswith("ref(")
        ]
        assert len(refs) == 1 and token(refs[0]["args"][0]) == "0"
        rhs = top_rewrites[0]["rhs"]
        assert label(rhs).startswith("ref(")
        assert token(rhs["args"][0]) == "1"

        print(
            f"CLAIM_PINNING_OK label={claim_label} "
            f"body_sha256={stable_digest(source_body)}"
        )
        checked += 1

    print(
        "PINNING_RESULT PASS "
        f"claims={checked} source_body_sha256={stable_digest(source_body)}"
    )


if __name__ == "__main__":
    main()
