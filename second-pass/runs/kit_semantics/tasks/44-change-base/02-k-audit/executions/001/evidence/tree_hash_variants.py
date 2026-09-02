#!/usr/bin/env python3
"""Identify the launcher's declared tree-hash serialization independently."""

import hashlib
import itertools
import os
from pathlib import Path


TREES = {
    Path("/candidate/reference-semantics"):
        "1de6d5f51876cf9d0f4449a78f077f8b127a14add0504d5060da680fc5a443de",
    Path("/generation-evidence/codex-trace"):
        "d15b81103bd0e998b73c5655d8314b18c994dbca43706008eb33965388c1071a",
}


def entries(root: Path, include_dirs: bool, include_root: bool):
    result = []
    if include_root:
        result.append((Path("."), root))
    for path in root.rglob("*"):
        if include_dirs or path.is_file() or path.is_symlink():
            result.append((path.relative_to(root), path))
    return sorted(result, key=lambda item: item[0].as_posix())


def kind(path: Path, style: str) -> bytes:
    if style == "none":
        return b""
    if path.is_symlink():
        value = {"word": "symlink", "short": "L", "stat": "l"}[style]
    elif path.is_dir():
        value = {"word": "directory", "short": "D", "stat": "d"}[style]
    else:
        value = {"word": "file", "short": "F", "stat": "f"}[style]
    return value.encode()


def payload(path: Path, style: str) -> bytes:
    if path.is_symlink():
        content = os.readlink(path).encode()
    elif path.is_file():
        content = path.read_bytes()
    else:
        content = b""
    if style == "content":
        return content
    if style == "sha256":
        return hashlib.sha256(content).hexdigest().encode()
    if style == "sha256raw":
        return hashlib.sha256(content).digest()
    return b""


def digest(
    root: Path,
    *,
    include_dirs: bool,
    include_root: bool,
    path_prefix: bytes,
    path_suffix: bytes,
    kind_style: str,
    kind_prefix: bytes,
    kind_suffix: bytes,
    payload_style: str,
    payload_suffix: bytes,
) -> str:
    h = hashlib.sha256()
    for rel, path in entries(root, include_dirs, include_root):
        rel_bytes = rel.as_posix().encode()
        h.update(path_prefix + rel_bytes + path_suffix)
        h.update(kind_prefix + kind(path, kind_style) + kind_suffix)
        h.update(payload(path, payload_style) + payload_suffix)
    return h.hexdigest()


values = {
    "include_dirs": [False, True],
    "include_root": [False, True],
    "path_prefix": [b"", b"./"],
    "path_suffix": [b"", b"\0", b"\n", b" "],
    "kind_style": ["word", "short", "stat", "none"],
    "kind_prefix": [b"", b"\0", b" "],
    "kind_suffix": [b"", b"\0", b"\n", b" "],
    "payload_style": ["content", "sha256", "sha256raw", "none"],
    "payload_suffix": [b"", b"\0", b"\n"],
}

matches = []
keys = list(values)
for choices in itertools.product(*(values[key] for key in keys)):
    options = dict(zip(keys, choices))
    if all(digest(root, **options) == expected for root, expected in TREES.items()):
        matches.append(options)

print(f"variants_tested={len(list(itertools.product(*(values[key] for key in keys))))}")
print(f"matches={len(matches)}")
for match in matches:
    print(match)


# Search common record layouts where component order, size/mode inclusion, and
# whether directories are records vary. This covers sha256sum-style manifests,
# Merkle-leaf manifests, and simple Go/Python WalkDir serializations.
record_matches = []
root_values = [False, True]
directory_values = [False, True]
path_styles = ["plain", "dot", "slashdir"]
kind_styles = ["none", "word", "short", "stat"]
payload_styles = ["content", "sha256", "sha256raw", "none"]
size_styles = ["none", "ascii", "big8"]
mode_styles = ["none", "ascii"]
separators = [b"", b"\0", b"\n", b" "]
orders = [
    ("path", "kind", "mode", "size", "payload"),
    ("kind", "path", "mode", "size", "payload"),
    ("payload", "path", "kind", "mode", "size"),
    ("path", "payload", "kind", "mode", "size"),
]


def record_digest(
    root: Path,
    *,
    include_root: bool,
    include_dirs: bool,
    path_style: str,
    kind_style: str,
    payload_style: str,
    size_style: str,
    mode_style: str,
    separator: bytes,
    suffix: bytes,
    order,
) -> str:
    h = hashlib.sha256()
    for rel, path in entries(root, include_dirs, include_root):
        rel_text = rel.as_posix()
        if path_style == "dot":
            rel_text = "./" + rel_text
        elif path_style == "slashdir" and path.is_dir():
            rel_text += "/"
        file_payload = b""
        if path.is_file() or path.is_symlink():
            file_payload = payload(path, payload_style)
        file_size = path.stat(follow_symlinks=False).st_size
        parts = {
            "path": rel_text.encode(),
            "kind": kind(path, kind_style),
            "payload": file_payload,
            "size": (
                b""
                if size_style == "none"
                else str(file_size).encode()
                if size_style == "ascii"
                else file_size.to_bytes(8, "big")
            ),
            "mode": (
                b""
                if mode_style == "none"
                else oct(path.stat(follow_symlinks=False).st_mode & 0o7777).encode()
            ),
        }
        present = [parts[name] for name in order if parts[name]]
        h.update(separator.join(present) + suffix)
    return h.hexdigest()


record_tested = 0
for choices in itertools.product(
    root_values,
    directory_values,
    path_styles,
    kind_styles,
    payload_styles,
    size_styles,
    mode_styles,
    separators,
    separators,
    orders,
):
    options = dict(
        zip(
            (
                "include_root",
                "include_dirs",
                "path_style",
                "kind_style",
                "payload_style",
                "size_style",
                "mode_style",
                "separator",
                "suffix",
                "order",
            ),
            choices,
        )
    )
    record_tested += 1
    if all(
        record_digest(root, **options) == expected
        for root, expected in TREES.items()
    ):
        record_matches.append(options)

print(f"record_variants_tested={record_tested}")
print(f"record_matches={len(record_matches)}")
for match in record_matches:
    print(match)
