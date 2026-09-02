#!/usr/bin/env python3
"""Inspect the candidate's untrusted serialized spec for provenance consistency."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


JSON_PATH = Path("/candidate/spec.json")
SOURCE_PATH = Path("/candidate/spec.k")


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main() -> int:
    raw = JSON_PATH.read_bytes()
    parsed = json.loads(raw)
    labels = collections.Counter()
    claim_labels = []
    source_locations = []
    for node in walk(parsed):
        if node.get("node") == "KLabel":
            labels[node.get("name", "")] += 1
        attributes = node.get("att")
        if isinstance(attributes, dict):
            data = attributes.get("att")
            if isinstance(data, dict):
                if "label" in data:
                    claim_labels.append(data["label"])
                if "org.kframework.attributes.Source" in data:
                    source_locations.append(data["org.kframework.attributes.Source"])

    source_text = SOURCE_PATH.read_text(encoding="utf-8")
    interesting = {
        name: count
        for name, count in sorted(labels.items())
        if any(token in name for token in ("While", "For", "AugAssign", "#while", "#loop"))
    }
    print(f"spec_json_sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"serialized_main_module={parsed['term']['mainModule']}")
    print(f"serialized_claim_labels={sorted(set(claim_labels))}")
    print(f"serialized_source_locations={sorted(set(source_locations))}")
    print(f"serialized_control_labels={interesting}")
    print(f"current_spec_has_While={('While(' in source_text)}")
    print(f"current_spec_has_AugAssign={('AugAssign(' in source_text)}")
    print(f"current_spec_has_For={('For(' in source_text)}")
    print(
        "stale_or_mismatched="
        + str(
            any("While" in key or "#while" in key or "AugAssign" in key for key in interesting)
            and "While(" not in source_text
            and "AugAssign(" not in source_text
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
