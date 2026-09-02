#!/usr/bin/env python3
"""Read the complete generation console log and preserve bounded audit signals."""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


EVENT = re.compile(
    r"^(user|codex|exec|apply_patch|warning:|tokens used|"
    r"\s*(?:succeeded|failed|exited)\b)"
)
SIGNAL = re.compile(
    r"(?:#Top|WarnStuckClaimState|kprove|kompile|krun|mutation|vacuity|"
    r"differential cases|mismatches:|RESULT:|ERROR|exit:)"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    event_lines = []
    signal_lines = []
    counters = collections.Counter()
    with args.source.open(errors="replace") as stream:
        for line_number, line in enumerate(stream, 1):
            stripped = line.rstrip("\n")
            if EVENT.search(stripped):
                event_lines.append((line_number, stripped))
            if SIGNAL.search(stripped):
                signal_lines.append((line_number, stripped))
                for key in (
                    "#Top",
                    "WarnStuckClaimState",
                    "kprove",
                    "kompile",
                    "krun",
                    "mutation",
                    "differential cases",
                    "mismatches:",
                    "RESULT:",
                    "ERROR",
                ):
                    if key in stripped:
                        counters[key] += 1
    total_lines = line_number

    lines = [
        "# Generation console-log review",
        "",
        f"- Complete lines read: {total_lines}",
        f"- Event-marker lines: {len(event_lines)}",
        f"- Proof/build/test signal lines: {len(signal_lines)}",
        f"- Signal counts: `{dict(sorted(counters.items()))}`",
        "",
        "## Event markers",
        "",
    ]
    lines.extend(f"- {number}: `{text}`" for number, text in event_lines)
    lines.extend(["", "## Proof/build/test signals", ""])
    lines.extend(f"- {number}: `{text}`" for number, text in signal_lines)
    args.output.write_text("\n".join(lines) + "\n")
    print(f"complete_lines_read={total_lines}")
    print(f"event_lines={len(event_lines)}")
    print(f"signal_lines={len(signal_lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
