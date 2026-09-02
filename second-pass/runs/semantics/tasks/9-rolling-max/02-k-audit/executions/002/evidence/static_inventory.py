#!/usr/bin/env python3
"""Emit an exhaustive source-level K declaration/rule inventory as JSON."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/9-rolling-max")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^(requires|module|endmodule)\b|^ {2}(imports|syntax|configuration|context|rule|claim)\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")


def source_class(path: Path) -> str:
    if path.name == "verification.k":
        return "candidate-proof-extension"
    if path.name == "spec.k":
        return "candidate-specification"
    return "trusted-supplied-semantics"


def attributes(text: str) -> list[str]:
    result = []
    for group in ATTR.findall(text):
        result.extend(item.strip() for item in group.split(","))
    return result


def classify(keyword: str, text: str, attrs: list[str]) -> list[str]:
    classes = []
    if keyword == "rule":
        classes.append("operational-rule" if "<k>" in text else "equational-rule")
    elif keyword == "syntax":
        classes.append("syntax-declaration")
    elif keyword == "context":
        classes.append("evaluation-context")
    elif keyword == "configuration":
        classes.append("configuration")
    elif keyword == "claim":
        classes.append("reachability-claim")
    else:
        classes.append(keyword)

    joined = ",".join(attrs)
    for marker in [
        "function",
        "functional",
        "total",
        "macro",
        "macro-rec",
        "priority",
        "owise",
        "concrete",
        "simplification",
        "anywhere",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
    ]:
        if re.search(rf"(^|[^A-Za-z-]){re.escape(marker)}([^A-Za-z-]|$)", joined):
            classes.append(marker)
    if "symbol" in classes and "no-evaluators" in classes:
        classes.append("opaque-symbol")
    return classes


def main() -> int:
    inventory = []
    for path in FILES:
        lines = path.read_text().splitlines()
        starts = []
        for index, line in enumerate(lines):
            match = START.match(line)
            if match:
                starts.append((index, match.group(1) or match.group(2)))
        for item_index, (start, keyword) in enumerate(starts):
            next_start = starts[item_index + 1][0] if item_index + 1 < len(starts) else len(lines)
            end = next_start
            while end > start + 1 and (
                not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
            ):
                end -= 1
            text = "\n".join(lines[start:end])
            attrs = attributes(text)
            inventory.append(
                {
                    "source_class": source_class(path),
                    "file": str(path),
                    "start_line": start + 1,
                    "end_line": end,
                    "keyword": keyword,
                    "attributes": attrs,
                    "classes": classify(keyword, text, attrs),
                    "text": text,
                }
            )

    keyword_counts = collections.Counter(item["keyword"] for item in inventory)
    class_counts = collections.Counter(
        item_class for item in inventory for item_class in item["classes"]
    )
    per_file = collections.Counter(item["file"] for item in inventory)
    output = {
        "files": [str(path) for path in FILES],
        "file_count": len(FILES),
        "inventory_item_count": len(inventory),
        "keyword_counts": dict(sorted(keyword_counts.items())),
        "class_counts": dict(sorted(class_counts.items())),
        "per_file_item_counts": dict(sorted(per_file.items())),
        "items": inventory,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
