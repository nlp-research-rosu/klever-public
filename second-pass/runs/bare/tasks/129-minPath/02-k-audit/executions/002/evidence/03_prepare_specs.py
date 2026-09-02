#!/usr/bin/env python3
"""Create mechanically labeled copies of the submitted anonymous claims."""

from __future__ import annotations

import re
from pathlib import Path


SOURCE = Path("/tmp/audit-work/candidate-src/spec.k")
LABELED = Path("/tmp/audit-work/candidate-src/spec-labeled.k")


def main() -> None:
    text = SOURCE.read_text()
    text = text.replace(
        "module MINPATH-SPEC\n", "module MINPATH-SPEC-LABELED\n", 1
    )
    counter = 0

    def label(_: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        return f"\n  claim [audit-{counter:02d}]:\n"

    text, replacements = re.subn(r"\n  claim\n", label, text)
    text = text.replace("endmodule\n", "endmodule\n", 1)
    assert replacements == 11
    assert counter == 11
    LABELED.write_text(text)
    print(f"source={SOURCE}")
    print(f"labeled={LABELED}")
    print(f"claims_labeled={counter}")
    print("labels=" + ",".join(f"audit-{index:02d}" for index in range(1, 12)))


if __name__ == "__main__":
    main()
