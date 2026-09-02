#!/usr/bin/env python3
"""Add inert audit labels so each original positive claim can be selected alone."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    source_path = Path("/tmp/audit-work/138-audit/scratch/spec.k")
    output_path = Path("/tmp/audit-work/138-audit/scratch/spec-audit-labeled.k")
    preserved_path = Path("/audit-output/evidence/spec-audit-labeled.k")
    lines = source_path.read_text().splitlines()
    count = 0
    output = []
    for line in lines:
        if line == "module SPEC":
            output.append("module SPEC-AUDIT-LABELED")
        elif line.strip() == "claim":
            count += 1
            indent = line[: len(line) - len(line.lstrip())]
            output.append(f"{indent}claim [audit-claim-{count}]:")
        else:
            output.append(line)
    assert count == 6, f"expected 6 claims, found {count}"
    rendered = "\n".join(output) + "\n"
    output_path.write_text(rendered)
    preserved_path.write_text(rendered)
    print("source:", source_path)
    print("generated:", output_path)
    print("preserved:", preserved_path)
    print("labeled_claim_count:", count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
