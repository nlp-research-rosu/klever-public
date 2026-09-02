#!/usr/bin/env python3
"""Check exact source containment for the proved loop claim reused as a rule."""

from pathlib import Path


SCRATCH = Path("/tmp/audit-work/150-x-or-y-review")


def slice_lines(path: Path, first: int, last: int) -> list[str]:
    return path.read_text().splitlines()[first - 1 : last]


def normalized(lines: list[str], leading: str, trailing_prefix: str) -> list[str]:
    result = list(lines)
    assert result[0].strip() == leading
    result[0] = "<BRIDGE>"
    assert result[-1].strip().startswith(trailing_prefix)
    result = result[:-1]
    return [line.rstrip() for line in result]


def main() -> int:
    claim = normalized(
        slice_lines(SCRATCH / "spec.k", 9, 36),
        "claim",
        "[label(loop_correct)]",
    )
    rule = normalized(
        slice_lines(SCRATCH / "verification.k", 73, 100),
        "rule",
        "[priority(40)]",
    )
    same = claim == rule
    print(f"claim_lines_without_attribute={len(claim)}")
    print(f"rule_lines_without_attribute={len(rule)}")
    print(f"normalized_exact_match={same}")
    if not same:
        for index, (left, right) in enumerate(zip(claim, rule), start=1):
            if left != right:
                print(f"first_difference_line={index} claim={left!r} rule={right!r}")
                break
    print(
        "The compiled-definition check below uses the source location attached "
        "to the summary rule."
    )
    needle = "Location(Location(74,5,99,24))"
    base_definition = (SCRATCH / "verification-kompiled" / "definition.kore").read_text()
    summary_definition = (SCRATCH / "summary-kompiled" / "definition.kore").read_text()
    base_count = base_definition.count(needle)
    summary_count = summary_definition.count(needle)
    print(f"base_main_module={(SCRATCH / 'verification-kompiled' / 'mainModule.txt').read_text().strip()}")
    print(f"summary_main_module={(SCRATCH / 'summary-kompiled' / 'mainModule.txt').read_text().strip()}")
    print(f"bridge_location_occurrences_in_base_definition={base_count}")
    print(f"bridge_location_occurrences_in_summary_definition={summary_count}")
    separated = base_count == 0 and summary_count == 1
    print(f"proof_then_import_separation={separated}")
    return 0 if same and separated else 1


if __name__ == "__main__":
    raise SystemExit(main())
