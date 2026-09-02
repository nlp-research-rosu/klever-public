#!/usr/bin/env python3
"""Create a fresh, satisfiable, false result mutation from the audited spec."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/h59/spec.k")
OUTPUT = Path("/audit-output/evidence/spec-vacuity.k")


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one occurrence, got {count}: {old!r}")
    return text.replace(old, new, 1)


def main() -> int:
    text = SOURCE.read_text()
    text = replace_once(text, "module SPEC\n", "module SPEC-VACUITY\n")
    text = replace_once(
        text,
        "requires N0 >=Int 2\n    ensures ?RESULT ==Int lpfFrom(N0, 2)",
        "requires N0 ==Int 15\n"
        "    ensures ?RESULT ==Int lpfFrom(N0, 2) +Int 1",
    )
    OUTPUT.write_text(text)
    print("mutation=entry result changed from lpfFrom(N0,2) to lpfFrom(N0,2)+1")
    print("satisfying_witness=N0=15")
    print("actual_result=5")
    print("mutated_required_result=6")
    print(f"output={OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
