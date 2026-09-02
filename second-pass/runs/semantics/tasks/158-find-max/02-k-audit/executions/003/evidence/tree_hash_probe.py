#!/usr/bin/env python3
"""Compute independent deterministic tree digests and probe common manifest forms."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def digest(path: Path) -> bytes:
    return hashlib.sha256(path.read_bytes()).digest()


def entries(root: Path):
    return [
        (path.relative_to(root).as_posix(), digest(path))
        for path in sorted(root.rglob("*"))
        if path.is_file()
    ]


def variants(root: Path):
    items = entries(root)
    for path_prefix in ("", "./"):
        for path_sep in (b"", b"\0", b"\n", b" ", b":"):
            for entry_sep in (b"", b"\0", b"\n"):
                for value_kind in ("raw", "hex", "content"):
                    payload = b""
                    for relative, raw_hash in items:
                        value = {
                            "raw": raw_hash,
                            "hex": raw_hash.hex().encode(),
                            "content": (root / relative).read_bytes(),
                        }[value_kind]
                        payload += (
                            (path_prefix + relative).encode()
                            + path_sep
                            + value
                            + entry_sep
                        )
                    name = (
                        f"concat(prefix={path_prefix!r},path_sep={path_sep!r},"
                        f"entry_sep={entry_sep!r},value={value_kind})"
                    )
                    yield name, hashlib.sha256(payload).hexdigest()
    hex_map = {relative: raw_hash.hex() for relative, raw_hash in items}
    for compact in (False, True):
        kwargs = {"sort_keys": True}
        if compact:
            kwargs["separators"] = (",", ":")
        payload = json.dumps(hex_map, **kwargs).encode()
        yield f"json-map(compact={compact})", hashlib.sha256(payload).hexdigest()


def main() -> None:
    targets = {
        Path("/reference/reference-semantics"): {
            "1de6d5f51876cf9d0f4449a78f077f8b127a14add0504d5060da680fc5a443de",
            "4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f",
            "36288fc0a5134e284ff4fa9af3eaa619c0c5c1b8ab2c700389418a9725b58e26",
        },
        Path("/candidate"): {
            "a51ef4bd84c05f015cf33850051557e84e452f109c0a851bf1d56ba269fcdce0"
        },
    }
    print("COMMAND: python3 /audit-output/evidence/tree_hash_probe.py")
    for root, expected in targets.items():
        matched = []
        all_variants = list(variants(root))
        for name, actual in all_variants:
            if actual in expected:
                matched.append((name, actual))
        canonical_name, canonical_digest = all_variants[0]
        print(
            f"{root}: files={len(entries(root))} "
            f"independent_digest={canonical_digest} form={canonical_name}"
        )
        print(f"{root}: recorded_targets={sorted(expected)}")
        print(f"{root}: common_form_matches={matched}")


if __name__ == "__main__":
    main()
