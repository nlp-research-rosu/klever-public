#!/usr/bin/env python3
"""Emit every local K declaration/rule/claim from the immutable proof sources."""

from __future__ import annotations

from pathlib import Path
import re


SOURCES = (
    Path("/candidate/semantic.k"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
)


def logical_items(lines: list[str], keyword: str) -> list[tuple[int, str]]:
    items: list[tuple[int, str]] = []
    index = 0
    while index < len(lines):
        stripped = lines[index].lstrip()
        if not stripped.startswith(keyword + " "):
            index += 1
            continue
        start = index
        pieces = [stripped.rstrip()]
        index += 1
        if keyword == "syntax":
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                pieces.append(lines[index].strip())
                index += 1
        elif keyword in {"rule", "claim", "configuration"}:
            while index < len(lines):
                next_stripped = lines[index].lstrip()
                if (
                    next_stripped.startswith(
                        (
                            "rule ",
                            "claim ",
                            "syntax ",
                            "configuration ",
                            "module ",
                            "endmodule",
                            "imports ",
                            "requires ",
                        )
                    )
                    or next_stripped.startswith("//")
                    or not next_stripped.strip()
                ):
                    break
                pieces.append(lines[index].strip())
                index += 1
        items.append((start + 1, " ".join(pieces)))
    return items


def main() -> None:
    totals = {key: 0 for key in ("syntax", "rule", "claim", "configuration")}
    all_text = ""
    for path in SOURCES:
        text = path.read_text(encoding="utf-8")
        all_text += text + "\n"
        lines = text.splitlines()
        print(f"SOURCE {path}")
        for keyword in totals:
            for line_number, item in logical_items(lines, keyword):
                totals[keyword] += 1
                print(
                    f"{keyword.upper()} index={totals[keyword]} "
                    f"line={line_number} text={item}"
                )
    function_names = re.findall(
        r"([A-Za-z_][A-Za-z0-9_]*)\([^)\n]*\)\s*\[function\]",
        all_text,
    )
    function_names = sorted(set(function_names))
    print("FUNCTION_SYMBOLS " + ", ".join(function_names))
    print(f"FUNCTION_SYMBOL_COUNT {len(function_names)}")
    for marker in (
        "[total]",
        "[functional]",
        "opaque",
        "priority",
        "simplification",
        "[owise]",
    ):
        print(
            f"MARKER {marker!r} occurrences="
            f"{all_text.lower().count(marker.lower())}"
        )
    for key, value in totals.items():
        print(f"TOTAL_{key.upper()} {value}")


if __name__ == "__main__":
    main()
