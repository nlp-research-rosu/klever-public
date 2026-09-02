#!/usr/bin/env python3
"""Reviewer-defined deterministic whole-tree hashes and top-level type checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def digest_tree(root: Path) -> tuple[str, int, int, list[str]]:
    digest = hashlib.sha256()
    files = 0
    byte_count = 0
    symlinks: list[str] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix().encode()
        if path.is_symlink():
            symlinks.append(path.relative_to(root).as_posix())
            continue
        if not path.is_file():
            continue
        body = path.read_bytes()
        digest.update(len(rel).to_bytes(8, "big"))
        digest.update(rel)
        digest.update(len(body).to_bytes(8, "big"))
        digest.update(body)
        files += 1
        byte_count += len(body)
    return digest.hexdigest(), files, byte_count, symlinks


def main() -> None:
    audit = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
    for root in [
        Path("/candidate"),
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence/codex-trace"),
    ]:
        digest, files, byte_count, symlinks = digest_tree(root)
        print(
            root,
            "reviewer_tree_sha256=" + digest,
            "files=" + str(files),
            "bytes=" + str(byte_count),
            "symlinks=" + json.dumps(symlinks),
        )
    print(
        "launcher_recorded_tree_hashes:",
        json.dumps(
            {
                key: value
                for key, value in audit["hashes"].items()
                if "tree" in key or "reference_semantics_sha256" in key
                or key == "generation_codex_trace_sha256"
            },
            sort_keys=True,
        ),
    )
    for name in [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]:
        path = Path("/candidate") / name
        print(name, "type=file" if path.is_file() and not path.is_symlink() else "BAD_TYPE")


if __name__ == "__main__":
    main()
