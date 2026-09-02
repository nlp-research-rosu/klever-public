#!/usr/bin/env python3
"""Probe common deterministic directory-digest encodings.

This is reviewer-authored diagnostic evidence.  It does not trust candidate
hashes or candidate code.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


def entries(root: Path) -> list[tuple[str, str, Path]]:
    result: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for item in os.scandir(directory):
            mode = item.stat(follow_symlinks=False).st_mode
            path = Path(item.path)
            rel = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result.append((rel, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                result.append((rel, "file", path))
            else:
                raise RuntimeError(f"unsupported entry: {path}")
    return sorted(result)


def digest_stream(parts: list[bytes]) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part)
    return digest.hexdigest()


def probe(root: Path) -> None:
    tree = entries(root)
    files = [(rel, path) for rel, kind, path in tree if kind == "file"]
    file_hashes = [(rel, hashlib.sha256(path.read_bytes()).hexdigest()) for rel, path in files]
    outputs: dict[str, str] = {}
    outputs["concat-content"] = digest_stream([path.read_bytes() for _, path in files])
    outputs["rel-nul-content"] = digest_stream(
        [part for rel, path in files for part in (rel.encode(), b"\0", path.read_bytes())]
    )
    outputs["rel-newline-content"] = digest_stream(
        [part for rel, path in files for part in (rel.encode(), b"\n", path.read_bytes())]
    )
    outputs["rel-nul-hex-nul"] = digest_stream(
        [
            part
            for rel, hexdigest in file_hashes
            for part in (rel.encode(), b"\0", hexdigest.encode(), b"\0")
        ]
    )
    outputs["hex-space-rel-newline"] = digest_stream(
        [
            f"{hexdigest}  {rel}\n".encode()
            for rel, hexdigest in file_hashes
        ]
    )
    outputs["json-map-compact"] = hashlib.sha256(
        json.dumps(dict(file_hashes), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    outputs["json-map-default"] = hashlib.sha256(
        json.dumps(dict(file_hashes), sort_keys=True).encode()
    ).hexdigest()

    pipeline_parts: list[bytes] = []
    lean_parts: list[bytes] = []
    for rel, kind, path in tree:
        encoded = rel.encode()
        pipeline_parts.extend(
            [
                len(encoded).to_bytes(4, "big"),
                encoded,
                kind.encode(),
                b"\0",
            ]
        )
        lean_parts.extend([encoded, b"\0", kind.encode(), b"\0"])
        if kind == "file":
            content = path.read_bytes()
            pipeline_parts.extend([len(content).to_bytes(8, "big"), content])
            lean_parts.append(content)
    outputs["pipeline-sha256-tree"] = digest_stream(pipeline_parts)
    outputs["relative-nul-kind-nul-content"] = digest_stream(lean_parts)

    print(f"ROOT {root}")
    print(f"ENTRY_COUNT {len(tree)} FILE_COUNT {len(files)}")
    for name, value in outputs.items():
        print(f"{name} {value}")


def main() -> None:
    for argument in sys.argv[1:]:
        probe(Path(argument))


if __name__ == "__main__":
    main()
