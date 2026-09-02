#!/usr/bin/env python3
"""Generate the auditor's independent false empty-list result claim."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path("/tmp/audit-work/126-is-sorted/spec.k")
TARGET = Path("/tmp/audit-work/126-is-sorted/auditor-nonvacuity.k")


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one occurrence of {old!r}, got {count}")
    return text.replace(old, new, 1)


def main() -> int:
    source = SOURCE.read_text()
    start = source.index("  claim [entry]:")
    end = source.rindex("endmodule")
    entry = source[start:end]

    entry = replace_once(
        entry,
        'list(VS:ValSeq))\n      => sortedWithAtMostTwo(VS)',
        "list(.ValSeq))\n      => false",
    )
    entry = replace_once(
        entry,
        ".Map => 0 |-> list(sortVS(VS))",
        ".Map => 0 |-> list(.ValSeq)",
    )
    entry = replace_once(
        entry,
        "    requires nonNegativeVals(VS)\n",
        "",
    )
    entry = replace_once(
        entry,
        "  claim [entry]:",
        "  claim [false-empty-result]:",
    )

    target = (
        'requires "verification.k"\n\n'
        "module AUDITOR-NONVACUITY\n"
        "  imports VERIFICATION\n\n"
        + entry
        + "endmodule\n"
    )
    TARGET.write_text(target)
    print(f"source={SOURCE}")
    print(f"target={TARGET}")
    print("satisfying_input=list(.ValSeq)")
    print("source_result=true")
    print("mutated_required_result=false")
    print("closure_body=unchanged submitted constructor body")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
