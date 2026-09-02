#!/usr/bin/env python3
"""Independent content/type manifest for mounted candidate and semantics trees."""

import hashlib
import os
from pathlib import Path


def inventory(root: Path):
    manifest = hashlib.sha256()
    entries = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            kind = "symlink"
            value = os.readlink(path)
            digest = hashlib.sha256(value.encode()).hexdigest()
        elif path.is_dir():
            kind = "dir"
            digest = "-"
        elif path.is_file():
            kind = "file"
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            kind = "other"
            digest = "-"
        record = f"{kind}\0{relative}\0{digest}\0".encode()
        manifest.update(record)
        entries.append((kind, relative, digest))
    return manifest.hexdigest(), entries


for root_name in (
    "/candidate",
    "/reference/reference-semantics",
    "/candidate/reference-semantics",
):
    root = Path(root_name)
    digest, entries = inventory(root)
    print(f"TREE root={root} reviewer_manifest_sha256={digest} entries={len(entries)}")
    for kind, relative, file_digest in entries:
        print(f"{kind}\t{file_digest}\t{relative}")
