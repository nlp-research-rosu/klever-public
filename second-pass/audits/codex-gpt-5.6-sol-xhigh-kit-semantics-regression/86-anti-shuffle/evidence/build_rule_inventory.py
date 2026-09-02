#!/usr/bin/env python3
"""Build a source-derived inventory of K declarations and rules."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
OUTPUT_JSON = Path("/audit-output/evidence/05-rule-inventory.json")
OUTPUT_MD = Path("/audit-output/evidence/05-rule-inventory.md")
START = re.compile(r"^\s*(syntax|configuration|rule|claim|context|alias)\b")
ATTRIBUTE = re.compile(
    r"\b(function|total|functional|simplification|priority(?:\([^)]*\))?"
    r"|symbol(?:\([^)]*\))?|macro|owise|concrete|no-evaluators|strict(?:\([^)]*\))?"
    r"|seqstrict(?:\([^)]*\))?)\b"
)


def proof_local_disposition(line: int) -> str:
    if 8 <= line <= 15:
        return "valid structural definition: consecutive heap representation"
    if line == 19:
        return "valid derived lemma: next consecutive heap index is absent"
    if 23 <= line <= 94:
        return "valid finite-map membership, lookup, or overwrite equality"
    if 97 <= line <= 129:
        return "exact syntax macro; expands to submitted translated AST"
    if 133 <= line <= 134:
        return "valid definitional summary, conditional on supplied sortVS primitive"
    if 139 <= line <= 169:
        return "valid structurally recursive scan/frame summary"
    if 174 <= line <= 215:
        return "valid structurally recursive heap/counter/freshness summary"
    if 219 <= line <= 243:
        return "valid inductive freshness simplification"
    if 245 <= line <= 258:
        return "valid final result/heap/counter definition"
    return "reviewed proof-local declaration"


source_files = sorted((ROOT / "reference-semantics").rglob("*.k"))
source_files += [ROOT / "verification.k", ROOT / "spec.k"]
inventory: list[dict[str, object]] = []
source_hashes: dict[str, str] = {}

for path in source_files:
    relative = str(path.relative_to(ROOT))
    raw = path.read_bytes()
    source_hashes[relative] = hashlib.sha256(raw).hexdigest()
    lines = raw.decode("utf-8").splitlines()
    starts = [
        (index, START.match(text).group(1))
        for index, text in enumerate(lines)
        if START.match(text)
    ]
    for position, (index, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:stop]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].strip() == "endmodule"
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        attrs = sorted(set(ATTRIBUTE.findall(block)))
        if relative == "verification.k":
            origin = "proof-local"
            disposition = proof_local_disposition(index + 1)
        elif relative == "spec.k":
            origin = "target-claim"
            disposition = "audited reachability claim"
        else:
            origin = "trusted-supplied-semantics"
            disposition = (
                "selected fixed semantics; inspected for submitted-program path "
                "and otherwise inert for this AST"
            )
        inventory.append(
            {
                "id": f"{relative}:{index + 1}",
                "file": relative,
                "line": index + 1,
                "kind": kind,
                "attributes": attrs,
                "origin": origin,
                "disposition": disposition,
                "text": block,
            }
        )

counts = Counter(item["kind"] for item in inventory)
origins = Counter(item["origin"] for item in inventory)
opaque = [
    item["id"]
    for item in inventory
    if "no-evaluators" in item["attributes"]
]
priorities = [
    item["id"]
    for item in inventory
    if any(str(attr).startswith("priority") for attr in item["attributes"])
]
payload = {
    "source_root": str(ROOT),
    "source_hashes": source_hashes,
    "counts_by_kind": dict(sorted(counts.items())),
    "counts_by_origin": dict(sorted(origins.items())),
    "opaque_declarations": opaque,
    "priority_declarations_or_rules": priorities,
    "items": inventory,
}
OUTPUT_JSON.write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

markdown = [
    "# Exhaustive K declaration/rule inventory",
    "",
    f"Items: {len(inventory)}",
    "",
    "Counts by kind: "
    + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())),
    "",
    "Counts by origin: "
    + ", ".join(f"{key}={value}" for key, value in sorted(origins.items())),
    "",
    "| ID | Kind | Attributes | Origin | Disposition | First source line |",
    "|---|---|---|---|---|---|",
]
for item in inventory:
    first_line = str(item["text"]).splitlines()[0].strip().replace("|", "\\|")
    attrs = ", ".join(item["attributes"]) or "—"
    markdown.append(
        f"| `{item['id']}` | {item['kind']} | {attrs} | {item['origin']} | "
        f"{item['disposition']} | `{first_line}` |"
    )
OUTPUT_MD.write_text("\n".join(markdown) + "\n", encoding="utf-8")

print(f"inventory_items={len(inventory)}")
print("counts_by_kind=" + json.dumps(dict(sorted(counts.items())), sort_keys=True))
print("counts_by_origin=" + json.dumps(dict(sorted(origins.items())), sort_keys=True))
print(f"opaque_count={len(opaque)}")
print(f"priority_count={len(priorities)}")
print(f"json_sha256={hashlib.sha256(OUTPUT_JSON.read_bytes()).hexdigest()}")
print(f"markdown_sha256={hashlib.sha256(OUTPUT_MD.read_bytes()).hexdigest()}")
