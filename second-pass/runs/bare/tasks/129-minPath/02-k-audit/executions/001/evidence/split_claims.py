#!/usr/bin/env python3
"""Split the candidate's unlabeled claims into independently runnable modules."""

from __future__ import annotations

import pathlib
import re


SOURCE = pathlib.Path("/tmp/audit-work/candidate-src/spec.k")
OUTPUT = pathlib.Path("/tmp/audit-work/candidate-src/isolated-claims")


def main() -> int:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if re.fullmatch(r"\s*claim\s*", line)]
    endmodule = next(
        index for index, line in enumerate(lines) if index > starts[-1] and line.strip() == "endmodule"
    )
    starts.append(endmodule)

    OUTPUT.mkdir(exist_ok=True)
    print(f"SOURCE={SOURCE}")
    print(f"CLAIM_COUNT={len(starts) - 1}")
    for claim_number, (start, end) in enumerate(zip(starts, starts[1:]), 1):
        claim_lines = lines[start:end]
        while claim_lines and not claim_lines[-1].strip():
            claim_lines.pop()
        module_name = f"MINPATH-SPEC-{claim_number:02d}"
        target = OUTPUT / f"spec-claim-{claim_number:02d}.k"
        rendered = "\n".join(
            [
                'requires "../verification.k"',
                "",
                f"module {module_name}",
                "  imports MINPATH-VERIFICATION",
                "",
                *claim_lines,
                "endmodule",
                "",
            ]
        )
        target.write_text(rendered, encoding="utf-8")
        print(f"{claim_number:02d}|{module_name}|{target}|claim_source_line={start + 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
