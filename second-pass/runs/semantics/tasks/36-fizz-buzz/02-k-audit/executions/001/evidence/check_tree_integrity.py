#!/usr/bin/env python3
"""Compare two trees by lstat type and regular-file bytes, never following links."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def inventory(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    pending = [root]
    while pending:
        parent = pending.pop()
        with os.scandir(parent) as entries:
            for entry in entries:
                path = Path(entry.path)
                rel = str(path.relative_to(root))
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISLNK(mode):
                    result[rel] = ("symlink", os.readlink(path))
                elif stat.S_ISDIR(mode):
                    result[rel] = ("directory", "")
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    digest = hashlib.sha256(path.read_bytes()).hexdigest()
                    result[rel] = ("file", digest)
                else:
                    result[rel] = ("other", oct(mode))
    return result


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED CANDIDATE", file=sys.stderr)
        return 2
    trusted_root, candidate_root = map(Path, sys.argv[1:])
    trusted = inventory(trusted_root)
    candidate = inventory(candidate_root)
    failures: list[str] = []
    for rel in sorted(trusted.keys() | candidate.keys()):
        if rel not in candidate:
            failures.append(f"MISSING {rel}: trusted={trusted[rel]}")
        elif rel not in trusted:
            failures.append(f"ADDITIONAL {rel}: candidate={candidate[rel]}")
        elif trusted[rel] != candidate[rel]:
            failures.append(
                f"CHANGED_OR_MISTYPED {rel}: "
                f"trusted={trusted[rel]} candidate={candidate[rel]}"
            )
    symlinks = [rel for rel, (kind, _) in candidate.items() if kind == "symlink"]
    for rel in symlinks:
        failures.append(f"FORBIDDEN_SYMLINK {rel}: target={candidate[rel][1]}")
    print(f"trusted_entries={len(trusted)}")
    print(f"candidate_entries={len(candidate)}")
    print(f"integrity_failures={len(failures)}")
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
