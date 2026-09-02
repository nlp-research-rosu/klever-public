#!/usr/bin/env python3
"""Mechanically split the candidate SPEC module into one spec per claim."""

from __future__ import annotations

import shutil
from pathlib import Path


SOURCE = Path("/tmp/audit-work/25-factorize/spec.k")
DESTINATION = Path("/audit-output/evidence/positive-claims")


def main() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    claims: list[list[str]] = []
    current: list[str] | None = None
    for line in lines:
        if line.startswith("  claim "):
            if current is not None:
                claims.append(current)
            current = [line]
        elif current is not None:
            if line == "endmodule":
                claims.append(current)
                current = None
            elif line.startswith("  //") or not line.strip():
                continue
            else:
                current.append(line)
    if current is not None:
        claims.append(current)
    if len(claims) != 26:
        raise AssertionError(f"expected 26 claims, found {len(claims)}")

    if DESTINATION.exists():
        for path in DESTINATION.iterdir():
            if path.is_file() and not path.is_symlink():
                path.unlink()
            else:
                raise RuntimeError(f"unexpected existing split-claim entry: {path}")
    else:
        DESTINATION.mkdir()

    for index, claim in enumerate(claims, 1):
        module = f"SPEC-CLAIM-{index:03d}"
        destination = DESTINATION / f"claim-{index:03d}.k"
        document = [
            'requires "verification.k"',
            "",
            f"module {module}",
            "  imports VERIFICATION",
            "",
            *claim,
            "endmodule",
            "",
        ]
        destination.write_text("\n".join(document), encoding="utf-8")
        print(
            f"generated {destination} module={module} "
            f"source_first_line={claim[0].strip()}"
        )
    print(f"SPLIT_CLAIM_COUNT={len(claims)}")


if __name__ == "__main__":
    main()
