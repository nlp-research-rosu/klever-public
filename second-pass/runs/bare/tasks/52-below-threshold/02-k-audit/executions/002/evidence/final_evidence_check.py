#!/usr/bin/env python3
"""Check REVIEW.md publication invariants and recorded command statuses."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/audit-output")
EVIDENCE = ROOT / "evidence"
EXPECTED_NONZERO = {
    "03-kprove-entry-alone-diagnostic": 130,
    "04-body-mutation-kprove": 1,
    "06-vacuity-kprove": 1,
    "06-vacuity-loop-kprove": 1,
}


def main() -> int:
    review = (ROOT / "REVIEW.md").read_text()
    assert review.endswith("VERDICT: PASS\nLEGITIMACY: LEGIT\n")
    assert review.count("\nVERDICT:") == 1
    assert review.count("\nLEGITIMACY:") == 1

    links = re.findall(r"\]\((/audit-output/[^)]+)\)", review)
    missing = [link for link in links if not Path(link).is_file()]
    print("review evidence links:", len(links))
    print("missing linked files:", len(missing))
    for link in missing:
        print(link)
    assert not missing

    exits: dict[str, int] = {}
    for path in sorted(EVIDENCE.glob("*.exit")):
        exits[path.stem] = int(path.read_text().strip())
    print("recorded exits:")
    for name, status in exits.items():
        print(f"{name}: {status}")
        expected = EXPECTED_NONZERO.get(name, 0)
        assert status == expected, (name, status, expected)

    for name in exits:
        assert (EVIDENCE / f"{name}.command").is_file()
        assert (EVIDENCE / f"{name}.log").is_file()

    for name, expected in EXPECTED_NONZERO.items():
        assert exits.get(name) == expected
    print("FINAL_EVIDENCE_CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
