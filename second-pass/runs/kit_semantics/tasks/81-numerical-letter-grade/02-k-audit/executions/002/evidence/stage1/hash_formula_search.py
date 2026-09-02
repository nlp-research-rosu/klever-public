#!/usr/bin/env python3
"""Search a bounded family of conventional tree-hash serializations."""

from __future__ import annotations

import hashlib
import itertools
import os
import stat
import sys
from pathlib import Path


def tree_entries(root: Path) -> list[tuple[str, str, bytes]]:
    entries: list[tuple[str, str, bytes]] = []
    for current, directories, files in os.walk(root):
        directories.sort()
        files.sort()
        base = Path(current)
        for name in directories:
            path = base / name
            mode = path.stat(follow_symlinks=False).st_mode
            if not stat.S_ISDIR(mode):
                raise RuntimeError(path)
            entries.append((path.relative_to(root).as_posix(), "directory", b""))
        for name in files:
            path = base / name
            mode = path.stat(follow_symlinks=False).st_mode
            if not stat.S_ISREG(mode):
                raise RuntimeError(path)
            entries.append((path.relative_to(root).as_posix(), "file", path.read_bytes()))
    return sorted(entries)


def field_bytes(kind: str, content: bytes, mode: str) -> bytes:
    if kind == "directory":
        return b""
    if mode == "raw":
        return content
    binary = hashlib.sha256(content).digest()
    if mode == "sha-bin":
        return binary
    if mode == "sha-hex":
        return binary.hex().encode()
    raise AssertionError(mode)


def main() -> None:
    root = Path(sys.argv[1])
    target = sys.argv[2]
    entries = tree_entries(root)
    separators = [b"", b"\0", b"\n", b" ", b":", b"\t"]
    prefixes = ["", "./"]
    kinds = {
        "none": {"file": b"", "directory": b""},
        "word": {"file": b"file", "directory": b"directory"},
        "letter": {"file": b"F", "directory": b"D"},
    }
    found = 0
    for include_dirs, prefix, kind_name, content_mode, sep1, sep2, sep3 in itertools.product(
        [False, True],
        prefixes,
        kinds,
        ["raw", "sha-bin", "sha-hex"],
        separators,
        separators,
        separators,
    ):
        digest = hashlib.sha256()
        for rel, kind, content in entries:
            if kind == "directory" and not include_dirs:
                continue
            digest.update((prefix + rel).encode())
            digest.update(sep1)
            digest.update(kinds[kind_name][kind])
            digest.update(sep2)
            digest.update(field_bytes(kind, content, content_mode))
            digest.update(sep3)
        if digest.hexdigest() == target:
            found += 1
            print(
                "MATCH",
                f"include_dirs={include_dirs}",
                f"prefix={prefix!r}",
                f"kind={kind_name}",
                f"content={content_mode}",
                f"sep1={sep1!r}",
                f"sep2={sep2!r}",
                f"sep3={sep3!r}",
            )
    print(f"SEARCHED root={root} target={target} matches={found}")


if __name__ == "__main__":
    main()
