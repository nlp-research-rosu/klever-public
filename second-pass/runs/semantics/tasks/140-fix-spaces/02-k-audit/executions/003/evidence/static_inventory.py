#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule index for the audited K sources."""

from __future__ import annotations

import hashlib
import pathlib
import re


ROOT = pathlib.Path("/tmp/audit-work/140-fix-spaces/source")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

DECLARATION = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|context|syntax|rule|claim)\b"
)
KIND = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|context|syntax|rule|claim)\b"
)


def main() -> int:
    totals: dict[str, int] = {}
    print("inventory_root=", ROOT)
    print("files=", len(FILES))
    for path in FILES:
        data = path.read_bytes()
        lines = data.decode("utf-8").splitlines()
        declarations: list[tuple[int, str]] = []
        for line_no, line in enumerate(lines, 1):
            match = DECLARATION.match(line)
            if not match:
                continue
            kind = KIND.match(line).group(1)  # type: ignore[union-attr]
            totals[kind] = totals.get(kind, 0) + 1
            declarations.append((line_no, line.strip()))

        relative = path.relative_to(ROOT)
        print(
            f"\nFILE {relative} sha256={hashlib.sha256(data).hexdigest()} "
            f"lines={len(lines)} declarations={len(declarations)}"
        )
        for index, (line_no, text) in enumerate(declarations, 1):
            attrs = []
            for attr in (
                "function",
                "functional",
                "total",
                "simplification",
                "concrete",
                "no-evaluators",
                "priority",
                "owise",
                "macro",
                "macro-rec",
                "strict",
                "seqstrict",
            ):
                if attr in text:
                    attrs.append(attr)
            suffix = f" attrs={','.join(attrs)}" if attrs else ""
            print(f"  {index:03d} line={line_no:04d} {text}{suffix}")

    print("\nTOTALS")
    for kind, count in sorted(totals.items()):
        print(f"{kind}={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
