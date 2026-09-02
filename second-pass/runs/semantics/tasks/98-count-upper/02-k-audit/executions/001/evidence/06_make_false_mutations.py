#!/usr/bin/env python3
"""Generate fresh result and body-sensitivity mutations from the copied candidate spec."""

from __future__ import annotations

import argparse
from pathlib import Path


SPEC = Path("/tmp/audit-work/reconstruction/spec.k")


def off_by_one(text: str) -> str:
    old_module = "module COUNT-UPPER-SPEC"
    old_result = "      => countUpperFrom(S, true)\n"
    if text.count(old_module) != 1 or text.count(old_result) != 1:
        raise RuntimeError("unexpected source shape for off-by-one mutation")
    return (
        text.replace(old_module, "module COUNT-UPPER-VACUITY-SPEC", 1)
        .replace(old_result, "      => countUpperFrom(S, true) +Int 1\n", 1)
    )


def body_sensitivity(text: str) -> str:
    start = text.index("  claim\n", text.index("// End-to-end claim"))
    stop = text.rindex("endmodule")
    entry = text[start:stop].rstrip()
    # Exactly two source-body occurrences exist in the entry claim: the executed
    # #loadAll body and the post-state closure body. Mutate both so failure cannot
    # be blamed on closure pinning; leave countUpperFrom's AEIOU equations unchanged.
    if entry.count('"AEIOU"') != 2:
        raise RuntimeError("unexpected source shape for body mutation")
    entry = entry.replace('"AEIOU"', '"A"')
    return (
        'requires "verification.k"\n\n'
        "module COUNT-UPPER-BODY-MUTATION-SPEC\n"
        "  imports COUNT-UPPER-VERIFICATION\n\n"
        "  // Executed program and pinned closure count only 'A'; postcondition still\n"
        "  // uses countUpperFrom, whose proof-local equations count AEIOU.\n"
        f"{entry}\n"
        "endmodule\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("off-by-one", "body"))
    args = parser.parse_args()
    source = SPEC.read_text()
    print(off_by_one(source) if args.kind == "off-by-one" else body_sensitivity(source), end="")


if __name__ == "__main__":
    main()
