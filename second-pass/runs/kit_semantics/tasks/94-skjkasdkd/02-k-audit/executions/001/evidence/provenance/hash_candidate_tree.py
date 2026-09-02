#!/usr/bin/env python3
"""Reviewer-defined deterministic content hashes for the mounted candidate tree."""

import hashlib
from pathlib import Path


root = Path("/candidate")
manifest = hashlib.sha256()
content_stream = hashlib.sha256()
file_count = 0
dir_count = 0
symlink_count = 0
total_bytes = 0
for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
    rel = path.relative_to(root).as_posix()
    if path.is_symlink():
        symlink_count += 1
        manifest.update(f"L\0{rel}\0{path.readlink()}\n".encode())
    elif path.is_dir():
        dir_count += 1
        manifest.update(f"D\0{rel}\n".encode())
    elif path.is_file():
        file_count += 1
        payload = path.read_bytes()
        total_bytes += len(payload)
        digest = hashlib.sha256(payload).hexdigest()
        manifest.update(f"F\0{rel}\0{len(payload)}\0{digest}\n".encode())
        content_stream.update(rel.encode())
        content_stream.update(b"\0")
        content_stream.update(payload)
print("file_count", file_count)
print("dir_count", dir_count)
print("symlink_count", symlink_count)
print("total_file_bytes", total_bytes)
print("reviewer_manifest_sha256", manifest.hexdigest())
print("reviewer_path_content_stream_sha256", content_stream.hexdigest())
