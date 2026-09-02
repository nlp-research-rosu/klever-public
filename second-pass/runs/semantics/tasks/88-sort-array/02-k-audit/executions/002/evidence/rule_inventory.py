#!/usr/bin/env python3
"""Generate a source-located inventory of local K declarations and rules."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
EXTRA = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
OUTPUT = Path("/audit-output/evidence/rule_inventory.md")

START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
BOUNDARY = re.compile(r"^\s*(syntax|rule|context|configuration|claim|module|endmodule)\b")


def compact(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines)
    text = re.sub(r"\s+", " ", text)
    return text.replace("|", r"\|")


def entries(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    out: list[dict[str, object]] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        end = index + 1
        while end < len(lines) and not BOUNDARY.match(lines[end]):
            end += 1
        body = lines[index:end]
        text = compact(body)
        tags: list[str] = []
        if kind == "syntax":
            for attr in [
                "function",
                "total",
                "functional",
                "macro",
                "macro-rec",
                "strict",
                "seqstrict",
                "symbol",
                "no-evaluators",
            ]:
                if re.search(rf"\b{re.escape(attr)}\b", text):
                    tags.append(attr)
            category = "syntax"
        elif kind == "rule":
            category = "operational" if "<k>" in text else "equation"
            for attr in ["priority", "simplification", "concrete", "owise", "macro-rec"]:
                if re.search(rf"\b{re.escape(attr)}\b", text):
                    tags.append(attr)
        else:
            category = kind
        out.append(
            {
                "kind": kind,
                "category": category,
                "line": index + 1,
                "end": end,
                "tags": ",".join(tags) or "-",
                "text": text,
            }
        )
        index = end
    return out


def main() -> None:
    files = sorted(ROOT.rglob("*.k"), key=lambda path: path.relative_to(ROOT).as_posix())
    files += EXTRA
    counts: Counter[str] = Counter()
    inventories: list[tuple[Path, list[dict[str, object]]]] = []
    for path in files:
        found = entries(path)
        inventories.append((path, found))
        for item in found:
            counts[f"kind:{item['kind']}"] += 1
            counts[f"category:{item['category']}"] += 1
            for tag in str(item["tags"]).split(","):
                if tag != "-":
                    counts[f"tag:{tag}"] += 1

    with OUTPUT.open("w") as stream:
        stream.write("# Exhaustive K source inventory\n\n")
        stream.write(
            "Generated from the trusted supplied-semantics mount plus the candidate "
            "`verification.k` and `spec.k`. Imported K builtin modules are outside "
            "this local-source inventory.\n\n"
        )
        stream.write("## Counts\n\n")
        for key, value in sorted(counts.items()):
            stream.write(f"- `{key}`: {value}\n")
        stream.write("\n")

        for path, found in inventories:
            display = (
                path.relative_to(ROOT).as_posix()
                if path.is_relative_to(ROOT)
                else str(path)
            )
            stream.write(f"## `{display}`\n\n")
            stream.write("| Location | Kind | Category | Attributes | Source declaration/rule |\n")
            stream.write("|---|---|---|---|---|\n")
            if not found:
                stream.write("| — | — | — | — | No local declaration, rule, context, configuration, or claim |\n")
            for item in found:
                location = (
                    f"{item['line']}"
                    if item["line"] == item["end"]
                    else f"{item['line']}-{item['end']}"
                )
                stream.write(
                    f"| {location} | {item['kind']} | {item['category']} | "
                    f"{item['tags']} | `{item['text']}` |\n"
                )
            stream.write("\n")

    print(f"files={len(files)}")
    print(f"output={OUTPUT}")
    for key, value in sorted(counts.items()):
        print(f"{key}={value}")
    print("RULE_INVENTORY=PASS")


if __name__ == "__main__":
    main()
