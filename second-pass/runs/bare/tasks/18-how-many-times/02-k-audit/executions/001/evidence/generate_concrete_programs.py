#!/usr/bin/env python3
"""Generate concrete MPY invocation programs from the submitted MPY module."""

from __future__ import annotations

import json
from pathlib import Path


CASES = {
    "documented-overlap": ("aaaa", "aa"),
    "empty-haystack": ("", "a"),
    "both-empty": ("", ""),
    "empty-needle": ("abc", ""),
    "needle-longer": ("ab", "abc"),
    "prefix-miss": ("baba", "ab"),
    "unicode-overlap": ("🙂🙂🙂", "🙂🙂"),
    "recursion-depth-stress": ("a" * 1_100, "z"),
}

def main() -> None:
    source_path = Path("/tmp/audit-work/how-many-times/solution.mpy")
    output_directory = Path("/tmp/audit-work/how-many-times/concrete-programs")
    output_directory.mkdir(exist_ok=True)

    source = source_path.read_text(encoding="utf-8").rstrip()
    if not source.endswith(")"):
        raise RuntimeError(
            "submitted solution.mpy does not end in Module's closing ')' "
        )
    module_without_close = source[:-1]

    for case_name, (string, substring) in CASES.items():
        string_literal = json.dumps(string, ensure_ascii=False)
        substring_literal = json.dumps(substring, ensure_ascii=False)
        invocation = (
            "\n  Expr(Call(Name(\"how_many_times\"), "
            f"Str({string_literal}), Str({substring_literal}))))"
        )
        output_path = output_directory / f"{case_name}.mpy"
        output_path.write_text(
            module_without_close + invocation + "\n", encoding="utf-8"
        )
        print(
            f"WROTE {output_path} "
            f"string_length={len(string)} substring_length={len(substring)}"
        )


if __name__ == "__main__":
    main()
