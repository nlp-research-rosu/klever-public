#!/usr/bin/env python3
"""Hash every mounted file with a reviewer-defined, documented tree aggregate."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


OUT = Path("/audit-output/evidence")
ROOTS = {
    "candidate": Path("/candidate"),
    "reference": Path("/reference"),
    "generation-evidence": Path("/generation-evidence"),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    summary: dict[str, object] = {
        "aggregate_definition": (
            "SHA256 of UTF-8 rows TYPE<TAB>RELATIVE_PATH<TAB>"
            "FILE_SHA256_OR_LINK_TARGET<LF>, sorted by relative path"
        ),
        "roots": {},
    }
    for name, root in ROOTS.items():
        rows: list[tuple[str, str, str]] = []
        for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                rows.append(("symlink", rel, os.readlink(path)))
            elif path.is_dir():
                rows.append(("dir", rel, ""))
            elif path.is_file():
                rows.append(("file", rel, sha256_file(path)))
            else:
                rows.append(("other", rel, ""))
        encoded = "".join("\t".join(row) + "\n" for row in rows).encode()
        manifest = OUT / f"{name}-tree-manifest.tsv"
        manifest.write_text("".join("\t".join(row) + "\n" for row in rows))
        summary["roots"][name] = {
            "path": str(root),
            "entry_count": len(rows),
            "symlink_count": sum(row[0] == "symlink" for row in rows),
            "reviewer_aggregate_sha256": hashlib.sha256(encoded).hexdigest(),
            "manifest": str(manifest),
            "manifest_sha256": sha256_file(manifest),
        }
    print(json.dumps(summary, indent=2, sort_keys=True))
    (OUT / "mounted-tree-hash-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
