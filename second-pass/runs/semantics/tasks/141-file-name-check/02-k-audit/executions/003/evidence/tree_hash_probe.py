#!/usr/bin/env python3
"""Probe common deterministic tree-hash encodings against launcher records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


TARGETS = {
    Path("/reference/reference-semantics"): {
        "1de6d5f51876cf9d0f4449a78f077f8b127a14add0504d5060da680fc5a443de",
        "36288fc0a5134e284ff4fa9af3eaa619c0c5c1b8ab2c700389418a9725b58e26",
        "4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f",
    },
    Path("/candidate"): {
        "01cb68a2973cdee96461087511a1080f531f53c9ed5e23e3d9d79dba347f3298",
        "fc3987be5629ea9557ec8ddd582b49850de4ea2c998e6f9fa723ce32b86f26d9",
    },
}


def digest(chunks) -> str:
    state = hashlib.sha256()
    for chunk in chunks:
        state.update(chunk)
    return state.hexdigest()


def main() -> None:
    for root, targets in TARGETS.items():
        files = sorted(path for path in root.rglob("*") if path.is_file())
        records = [
            (
                path.relative_to(root).as_posix(),
                path.read_bytes(),
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            for path in files
        ]
        variants: dict[str, str] = {}
        variants["rel0content"] = digest(
            piece
            for rel, content, _sha in records
            for piece in (rel.encode(), b"\0", content)
        )
        variants["rel_nl_content"] = digest(
            piece
            for rel, content, _sha in records
            for piece in (rel.encode(), b"\n", content)
        )
        variants["rel_content"] = digest(
            piece
            for rel, content, _sha in records
            for piece in (rel.encode(), content)
        )
        variants["rel0shahex"] = digest(
            piece
            for rel, _content, sha in records
            for piece in (rel.encode(), b"\0", sha.encode())
        )
        variants["rel0shabin"] = digest(
            piece
            for rel, _content, sha in records
            for piece in (rel.encode(), b"\0", bytes.fromhex(sha))
        )
        variants["sha2spacesrel"] = digest(
            f"{sha}  {rel}\n".encode() for rel, _content, sha in records
        )
        variants["sha1spacerel"] = digest(
            f"{sha} {rel}\n".encode() for rel, _content, sha in records
        )
        mapping = {rel: sha for rel, _content, sha in records}
        variants["json_default"] = hashlib.sha256(
            json.dumps(mapping, sort_keys=True).encode()
        ).hexdigest()
        variants["json_compact"] = hashlib.sha256(
            json.dumps(mapping, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        print(f"root={root} files={len(files)}")
        for name, value in variants.items():
            print(f"  {name}={value} launcher_match={value in targets}")


if __name__ == "__main__":
    main()
