#!/usr/bin/env python3
"""Generate an exhaustive source-positioned inventory of K declarations/rules."""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import NamedTuple


START_RE = re.compile(
    r"^\s*(module|imports|configuration|syntax|context|rule|claim|alias|endmodule)\b"
)
ATTR_RE = re.compile(r"\[([^\]]+)\]")


class Entry(NamedTuple):
    path: Path
    line_start: int
    line_end: int
    kind: str
    text: str
    attrs: tuple[str, ...]
    flags: tuple[str, ...]


def source_paths() -> list[Path]:
    root = Path("/reference/reference-semantics")
    paths = [root / "semantics.k", *sorted((root / "semantics").glob("*.k"))]
    paths.extend([Path("/candidate/verification.k"), Path("/candidate/spec.k")])
    return paths


def classify(kind: str, text: str, attrs: tuple[str, ...]) -> tuple[str, ...]:
    joined_attrs = ",".join(attrs)
    flags: list[str] = []
    if kind == "syntax":
        if "function" in joined_attrs:
            flags.append("function-declaration")
        if "total" in joined_attrs:
            flags.append("total-declaration")
        if "functional" in joined_attrs:
            flags.append("functional-declaration")
        if "macro" in joined_attrs:
            flags.append("macro-declaration")
        if "symbol(" in joined_attrs:
            flags.append("named-symbol")
        if "no-evaluators" in joined_attrs:
            flags.append("opaque-symbol")
    if kind == "rule":
        flags.append("operational-rule" if "<k>" in text else "equational-rule")
        if "priority(" in text:
            flags.append("priority-rule")
        if "simplification" in text:
            flags.append("simplification-rule")
        if "concrete" in text:
            flags.append("concrete-only-rule")
        if "owise" in text:
            flags.append("owise-rule")
    if kind == "claim":
        flags.append("reachability-claim")
    return tuple(flags)


def parse_file(path: Path) -> list[Entry]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if re.match(r'^\s*requires\s+"', line):
            starts.append((index, "requires"))
        else:
            match = START_RE.match(line)
            if match:
                starts.append((index, match.group(1)))
    entries: list[Entry] = []
    for position, (index, kind) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        raw_lines = lines[index:next_index]
        # Exclude trailing blank/comment prelude that belongs to the next conceptual
        # section while retaining every executable/declarative line.
        while raw_lines and not raw_lines[-1].strip():
            raw_lines.pop()
        text = " ".join(line.strip() for line in raw_lines if line.strip())
        attrs = tuple(
            attr.strip()
            for attr_group in ATTR_RE.findall(text)
            for attr in attr_group.split(",")
        )
        entries.append(
            Entry(
                path=path,
                line_start=index + 1,
                line_end=index + len(raw_lines),
                kind=kind,
                text=text,
                attrs=attrs,
                flags=classify(kind, text, attrs),
            )
        )
    return entries


def rel(path: Path) -> str:
    for root, prefix in (
        (Path("/reference/reference-semantics"), "trusted-reference-semantics"),
        (Path("/candidate"), "candidate"),
    ):
        try:
            return f"{prefix}/{path.relative_to(root).as_posix()}"
        except ValueError:
            pass
    return str(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = source_paths()
    entries_by_file = {path: parse_file(path) for path in paths}
    all_entries = [entry for path in paths for entry in entries_by_file[path]]
    kind_counts = Counter(entry.kind for entry in all_entries)
    flag_counts = Counter(flag for entry in all_entries for flag in entry.flags)

    output: list[str] = [
        "# Exhaustive K source inventory",
        "",
        "Generated from the recursively byte-identical trusted/candidate supplied "
        "semantics plus the candidate proof-local files. Every declaration, "
        "configuration, context, rule, and claim is source-positioned below.",
        "",
        "## Totals",
        "",
        f"- Source files: {len(paths)}",
        f"- Inventory entries: {len(all_entries)}",
    ]
    for kind, count in sorted(kind_counts.items()):
        output.append(f"- `{kind}` entries: {count}")
    for flag, count in sorted(flag_counts.items()):
        output.append(f"- `{flag}`: {count}")

    output.extend(["", "## Per-file counts", ""])
    for path in paths:
        counts = Counter(entry.kind for entry in entries_by_file[path])
        formatted = ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items()))
        output.append(f"- `{rel(path)}`: {formatted}")

    output.extend(["", "## Entries", ""])
    number = 0
    for path in paths:
        output.extend(["", f"### `{rel(path)}`", ""])
        for entry in entries_by_file[path]:
            number += 1
            flags = ", ".join(entry.flags) if entry.flags else "none"
            attrs = ", ".join(entry.attrs) if entry.attrs else "none"
            output.append(
                f"{number}. **{entry.kind}** `{rel(entry.path)}:"
                f"{entry.line_start}-{entry.line_end}`  "
            )
            output.append(f"   Flags: {flags}; attributes: {attrs}")
            output.append(f"   Source: `{entry.text.replace('`', chr(39))}`")

    rendered = "\n".join(output) + "\n"
    args.output.write_text(rendered, encoding="utf-8")
    digest = hashlib.sha256(rendered.encode()).hexdigest()
    print(f"output={args.output}")
    print(f"bytes={len(rendered.encode())}")
    print(f"sha256={digest}")
    print(f"source_files={len(paths)}")
    print(f"inventory_entries={len(all_entries)}")
    print("kind_counts=" + repr(dict(sorted(kind_counts.items()))))
    print("flag_counts=" + repr(dict(sorted(flag_counts.items()))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
