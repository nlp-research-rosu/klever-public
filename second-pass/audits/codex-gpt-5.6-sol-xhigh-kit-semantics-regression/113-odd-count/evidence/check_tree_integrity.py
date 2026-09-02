#!/usr/bin/env python3
"""Compare two trees by entry type and regular-file bytes without following links."""

from __future__ import annotations

import argparse
import hashlib
import os
import stat
from pathlib import Path


def inventory(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as entries:
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
                    result[rel] = ("regular", digest)
                else:
                    result[rel] = ("other", oct(mode))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trusted")
    parser.add_argument("candidate")
    args = parser.parse_args()
    trusted = inventory(Path(args.trusted))
    candidate = inventory(Path(args.candidate))
    problems: list[str] = []
    for rel in sorted(trusted.keys() - candidate.keys()):
        problems.append(f"MISSING {rel}: trusted={trusted[rel]}")
    for rel in sorted(candidate.keys() - trusted.keys()):
        problems.append(f"ADDITIONAL {rel}: candidate={candidate[rel]}")
    for rel in sorted(trusted.keys() & candidate.keys()):
        if trusted[rel] != candidate[rel]:
            problems.append(
                f"CHANGED_OR_MISTYPED {rel}: "
                f"trusted={trusted[rel]} candidate={candidate[rel]}"
            )
    symlinks = [
        rel for rel, value in candidate.items() if value[0] == "symlink"
    ]
    print(f"trusted_entries={len(trusted)}")
    print(f"candidate_entries={len(candidate)}")
    print(f"candidate_symlinks={len(symlinks)}")
    print(f"integrity_problems={len(problems)}")
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
