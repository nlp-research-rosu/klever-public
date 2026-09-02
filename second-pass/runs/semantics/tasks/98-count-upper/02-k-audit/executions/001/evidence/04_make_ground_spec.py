#!/usr/bin/env python3
"""Create ground instances of the exact candidate entry claim with exact Int results."""

from __future__ import annotations

from pathlib import Path


SPEC = Path("/tmp/audit-work/reconstruction/spec.k")


def int_seq(codes: list[int]) -> str:
    result = ".IntSeq"
    for code in reversed(codes):
        result = f"iCons({code}, {result})"
    return result


def main() -> None:
    text = SPEC.read_text()
    start = text.index("  claim\n", text.index("// End-to-end claim"))
    stop = text.rindex("endmodule")
    entry = text[start:stop].rstrip()
    cases = [
        ("empty", [], 0),
        ("documented_aBCdEf", [97, 66, 67, 100, 69, 102], 1),
        ("all_upper_vowels", [65, 69, 73, 79, 85], 3),
        ("unicode_boundary", [197, 69, 120120, 73, 128578, 79], 0),
    ]

    print('requires "verification.k"')
    print()
    print("module COUNT-UPPER-GROUND-SPEC")
    print("  imports COUNT-UPPER-VERIFICATION")
    for label, codes, expected in cases:
        sequence = int_seq(codes)
        ground = entry.replace("str(S:IntSeq)", f"str({sequence})")
        expected_summary = "countUpperFrom(S, true)"
        if expected_summary not in ground:
            raise RuntimeError(f"summary occurrence not found for {label}")
        ground = ground.replace(expected_summary, str(expected), 1)
        print()
        print(f"  // {label}: codes={codes!r}, exact expected result={expected}")
        print(ground)
    print("endmodule")


if __name__ == "__main__":
    main()
