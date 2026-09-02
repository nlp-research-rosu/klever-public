#!/usr/bin/env python3
"""Compute common deterministic tree-hash encodings for audit comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


targets = [
    (Path("/reference/reference-semantics"), "1de6d5f51876cf9d0f4449a78f077f8b127a14add0504d5060da680fc5a443de"),
    (Path("/candidate"), "5131d3a077016586f5c59b77675dbf36a7f769f723092b41ef7d1572981bf11f"),
    (Path("/generation-evidence/codex-trace"), "c13f73492f97fcd99a06dc20af8ac5ac6965e0be523a97052f627a5aeeb5003c"),
]


def files(root: Path) -> list[Path]:
    return sorted((path for path in root.rglob("*") if path.is_file()), key=lambda p: p.relative_to(root).as_posix())


def digest_chunks(chunks: list[bytes]) -> str:
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk)
    return digest.hexdigest()


def typed_tree_digest(root: Path) -> str:
    """Independently implement the launcher's typed path/size/content digest."""
    chunks: list[bytes] = []
    entries = sorted(
        (path.relative_to(root).as_posix(), path)
        for path in root.rglob("*")
    )
    for relative, path in entries:
        encoded = relative.encode()
        chunks.extend(
            [
                len(encoded).to_bytes(4, "big"),
                encoded,
                (b"directory\0" if path.is_dir() else b"file\0"),
            ]
        )
        if path.is_file():
            data = path.read_bytes()
            chunks.extend([len(data).to_bytes(8, "big"), data])
    return digest_chunks(chunks)


for root, expected in targets:
    paths = files(root)
    variants: dict[str, list[bytes]] = {}
    for prefix in ["", "./"]:
        for separator in [b"", b"\0", b"\n", b"  "]:
            for post in [b"", b"\0", b"\n"]:
                name = f"path_content prefix={prefix!r} sep={separator!r} post={post!r}"
                chunks: list[bytes] = []
                for path in paths:
                    relative = prefix + path.relative_to(root).as_posix()
                    chunks.extend([relative.encode(), separator, path.read_bytes(), post])
                variants[name] = chunks
    for prefix in ["", "./"]:
        for separator in [b"", b"\0", b"\n", b"  "]:
            for post in [b"", b"\0", b"\n"]:
                name = f"path_sha prefix={prefix!r} sep={separator!r} post={post!r}"
                chunks = []
                for path in paths:
                    relative = prefix + path.relative_to(root).as_posix()
                    file_hash = hashlib.sha256(path.read_bytes()).hexdigest().encode()
                    chunks.extend([relative.encode(), separator, file_hash, post])
                variants[name] = chunks
    print(f"ROOT={root} expected={expected} files={len(paths)}")
    typed_actual = typed_tree_digest(root)
    print(
        f"TYPED_TREE_DIGEST={typed_actual} "
        f"match={typed_actual == expected}"
    )
    file_map = {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }
    json_variants = {
        "json_map_compact": json.dumps(file_map, sort_keys=True, separators=(",", ":")).encode(),
        "json_map_default": json.dumps(file_map, sort_keys=True).encode(),
        "json_map_indent": json.dumps(file_map, sort_keys=True, indent=2).encode(),
        "json_list_compact": json.dumps(
            [{"path": key, "sha256": value} for key, value in file_map.items()],
            sort_keys=True,
            separators=(",", ":"),
        ).encode(),
        "json_list_indent": json.dumps(
            [{"path": key, "sha256": value} for key, value in file_map.items()],
            sort_keys=True,
            indent=2,
        ).encode(),
    }
    for name, data in json_variants.items():
        for suffix_name, suffix in [("none", b""), ("newline", b"\n")]:
            actual = hashlib.sha256(data + suffix).hexdigest()
            if actual == expected:
                print(f"MATCH {name}+{suffix_name}: {actual}")
    matched = False
    for name, chunks in variants.items():
        actual = digest_chunks(chunks)
        if actual == expected:
            print(f"MATCH {name}: {actual}")
            matched = True
    if not matched:
        print("NO_COMMON_VARIANT_MATCH")
