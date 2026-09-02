#!/usr/bin/env python3
"""Compare original and auditor-labeled K claims after removing attributes."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def claims(path: Path) -> Counter[str]:
    document = json.loads(path.read_text(encoding="utf-8"))
    modules = document["term"]["term"]
    records = []
    for module in modules:
        for sentence in module.get("localSentences", []):
            if sentence.get("node") != "KClaim":
                continue
            semantic = {
                "body": sentence["body"],
                "requires": sentence["requires"],
                "ensures": sentence["ensures"],
            }
            records.append(json.dumps(semantic, sort_keys=True, separators=(",", ":")))
    return Counter(records)


def main() -> int:
    original = claims(Path("/tmp/audit-work/reconstruction/spec-original.json"))
    labeled = claims(Path("/tmp/audit-work/reconstruction/spec-labeled.json"))
    print(f"original_claim_count={sum(original.values())}")
    print(f"labeled_claim_count={sum(labeled.values())}")
    print(f"semantic_claim_multisets_equal={original == labeled}")
    if original != labeled:
        print(f"only_original_count={sum((original - labeled).values())}")
        print(f"only_labeled_count={sum((labeled - original).values())}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
