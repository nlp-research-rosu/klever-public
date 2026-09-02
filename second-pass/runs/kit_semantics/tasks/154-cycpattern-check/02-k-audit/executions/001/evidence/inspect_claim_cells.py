#!/usr/bin/env python3
"""Summarize frontend cell completion for the submitted reachability claims."""

from __future__ import annotations

import json
from pathlib import Path


SPEC_JSON = Path(
    "/tmp/audit-work/cycpattern-audit/candidate-src/fresh-spec.json"
)


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def label_name(node: dict) -> str:
    return node.get("label", {}).get("name", "")


def summary(node: dict) -> str:
    rewrites = sum(item.get("node") == "KRewrite" for item in walk(node))
    variables = sorted(
        {
            item.get("name", "")
            for item in walk(node)
            if item.get("node") == "KVariable"
        }
    )
    tokens = [
        item.get("token", "")
        for item in walk(node)
        if item.get("node") == "KToken"
    ]
    return (
        f"rewrites={rewrites} variables={variables} "
        f"tokens={tokens[:12]}{'...' if len(tokens) > 12 else ''}"
    )


def main() -> int:
    document = json.loads(SPEC_JSON.read_text())
    modules = document["term"]["term"]
    claims = [
        sentence
        for module in modules
        for sentence in module.get("localSentences", [])
        if sentence.get("node") == "KClaim"
    ]
    print(f"spec_json={SPEC_JSON}")
    print(f"claims={len(claims)}")
    for claim in claims:
        attributes = claim.get("att", {}).get("att", {})
        claim_label = attributes.get("label")
        body = claim["body"]
        print(f"\nCLAIM {claim_label}")
        print(f"top_label={label_name(body)} arity={body.get('arity')}")
        for cell in body.get("args", []):
            print(f"  CELL {label_name(cell)}: {summary(cell)}")
        print(f"  REQUIRES: {summary(claim['requires'])}")
        print(f"  ENSURES: {summary(claim['ensures'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
