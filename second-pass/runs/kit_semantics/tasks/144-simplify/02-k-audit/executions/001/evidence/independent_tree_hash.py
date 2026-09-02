#!/usr/bin/env python3
"""Deterministic reviewer-defined type/path/content tree digest."""

from __future__ import annotations

import hashlib
import os
import stat
import sys


def tree_hash(root: str) -> tuple[str, dict[str, int]]:
    digest = hashlib.sha256()
    counts = {"directory": 0, "file": 0, "symlink": 0, "other": 0}
    for current, directories, files in os.walk(
        root, topdown=True, followlinks=False
    ):
        directories.sort()
        files.sort()
        entries = directories + files
        for name in entries:
            path = os.path.join(current, name)
            relative = os.path.relpath(path, root).replace(os.sep, "/")
            metadata = os.lstat(path)
            if stat.S_ISDIR(metadata.st_mode):
                kind = "directory"
                payload = b""
            elif stat.S_ISREG(metadata.st_mode):
                kind = "file"
                value = hashlib.sha256()
                with open(path, "rb") as stream:
                    for chunk in iter(
                        lambda: stream.read(1024 * 1024), b""
                    ):
                        value.update(chunk)
                payload = value.digest()
            elif stat.S_ISLNK(metadata.st_mode):
                kind = "symlink"
                payload = os.readlink(path).encode()
            else:
                kind = "other"
                payload = b""
            counts[kind] += 1
            digest.update(kind.encode() + b"\0")
            digest.update(relative.encode() + b"\0")
            digest.update(str(metadata.st_mode & 0o7777).encode() + b"\0")
            digest.update(str(metadata.st_size).encode() + b"\0")
            digest.update(payload + b"\0")
    return digest.hexdigest(), counts


status = 0
for root in sys.argv[1:]:
    value, counts = tree_hash(root)
    print(f"path={root} reviewer_tree_sha256={value} counts={counts}")
    status |= bool(counts["symlink"] or counts["other"])
print(f"EXIT_STATUS: {status}")
raise SystemExit(status)
