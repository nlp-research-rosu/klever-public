#!/usr/bin/env python3
"""Emit a complete, line-addressed inventory of the audited K sources."""

from collections import Counter
from pathlib import Path
import re


ROOT = Path("/reference/reference-semantics")
FILES = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k"))]
FILES += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
START = re.compile(r"^  (syntax|rule|claim|context|configuration)\b")


def normalized(lines):
    kept = []
    for line in lines:
        text = line.strip()
        if text and not text.startswith("//"):
            kept.append(text)
    return " ".join(kept)


records = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [(idx, START.match(line).group(1)) for idx, line in enumerate(lines) if START.match(line)]
    for pos, (start, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        while end > start and lines[end - 1].strip() in {"endmodule", ""}:
            end -= 1
        text = normalized(lines[start:end])
        tags = []
        if kind == "syntax":
            tags.append("declaration")
            for attr in (
                "function",
                "total",
                "functional",
                "symbol",
                "no-evaluators",
                "macro",
                "macro-rec",
                "strict",
                "seqstrict",
            ):
                if re.search(rf"\b{re.escape(attr)}\b", text):
                    tags.append(attr)
        elif kind == "rule":
            tags.append("operational" if "<k>" in text else "equational")
            for attr in ("priority", "simplification", "concrete", "owise"):
                if re.search(rf"\b{attr}\b", text):
                    tags.append(attr)
        elif kind == "context":
            tags.append("evaluation-context")
        elif kind == "claim":
            tags.append("reachability-claim")
        else:
            tags.append("configuration")
        records.append(
            (
                str(path),
                start + 1,
                max(start + 1, end),
                kind,
                ",".join(tags),
                text,
            )
        )

counts = Counter()
for _, _, _, kind, tags, _ in records:
    counts[kind] += 1
    for tag in tags.split(","):
        counts[f"tag:{tag}"] += 1

print("K SOURCE INVENTORY")
print("Files:")
for path in FILES:
    print(f"  {path}")
print(f"Total records: {len(records)}")
for key in sorted(counts):
    print(f"  {key}: {counts[key]}")
print("Records:")
for number, (path, start, end, kind, tags, text) in enumerate(records, 1):
    print(
        f"{number:04d}\t{path}:{start}-{end}\t{kind}\t{tags}\t{text}"
    )
