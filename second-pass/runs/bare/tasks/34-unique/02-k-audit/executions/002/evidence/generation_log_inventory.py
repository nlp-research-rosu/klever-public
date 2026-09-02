#!/usr/bin/env python3
"""Read every line of the plain generation log and report bounded landmarks."""

from __future__ import annotations

from collections import Counter
from pathlib import Path


def main() -> None:
    path = Path("/generation-evidence/codex-output.log")
    counts: Counter[str] = Counter()
    selected: list[tuple[int, str]] = []
    with path.open(encoding="utf-8", errors="strict") as stream:
        for line_number, line in enumerate(stream, 1):
            stripped = line.rstrip("\n")
            counts["lines"] += 1
            counts["bytes_as_utf8"] += len(line.encode("utf-8"))
            for label, marker in (
                ("exec_markers", "exec"),
                ("codex_markers", "codex"),
                ("top_markers", "#Top"),
                ("trivial_claim_warnings", "WarnTrivialClaim"),
                ("stuck_claim_warnings", "WarnStuckClaimState"),
                ("empty_claim_errors", "Unexpected empty set of claims"),
                ("result_markers", "RESULT: KPROVE_PASSED"),
            ):
                if (marker in stripped if len(marker) > 5 else stripped == marker):
                    counts[label] += 1
                    if label not in {"exec_markers", "codex_markers"}:
                        selected.append((line_number, stripped[:800]))
    print(f"LOG_PATH {path}")
    for key in sorted(counts):
        print(f"{key.upper()} {counts[key]}")
    for line_number, text in selected:
        print(f"LANDMARK line={line_number} text={text}")


if __name__ == "__main__":
    main()
