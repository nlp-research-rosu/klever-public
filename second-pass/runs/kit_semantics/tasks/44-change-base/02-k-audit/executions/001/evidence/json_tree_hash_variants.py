#!/usr/bin/env python3
"""Check common canonical-JSON tree manifests against launcher tree hashes."""

import hashlib
import json
from pathlib import Path


TREES = {
    Path("/candidate/reference-semantics"):
        "1de6d5f51876cf9d0f4449a78f077f8b127a14add0504d5060da680fc5a443de",
    Path("/generation-evidence/codex-trace"):
        "d15b81103bd0e998b73c5655d8314b18c994dbca43706008eb33965388c1071a",
}


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(root, include_dirs, shape):
    result = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_dir() and not include_dirs:
            continue
        kind = "directory" if path.is_dir() else "file"
        digest = None if path.is_dir() else file_sha(path)
        size = None if path.is_dir() else path.stat().st_size
        values = {
            "path": rel,
            "relative": rel,
            "name": rel,
            "kind": kind,
            "type": kind,
            "sha256": digest,
            "digest": digest,
            "size": size,
        }
        if shape == "triple":
            row = [rel, kind, digest or ""]
        elif shape == "pair":
            row = [rel, digest or kind]
        else:
            keys = shape.split(",")
            row = {key: values[key] for key in keys}
        result.append(row)
    return result


shapes = [
    "triple",
    "pair",
    "path,kind,sha256",
    "relative,type,digest",
    "path,sha256",
    "relative,sha256",
    "name,sha256",
    "path,kind,sha256,size",
]
wrappers = [
    lambda rows: rows,
    lambda rows: {"entries": rows},
    lambda rows: {"files": rows},
]
dump_options = [
    {"sort_keys": True, "separators": (",", ":")},
    {"sort_keys": False, "separators": (",", ":")},
    {"sort_keys": True},
    {"sort_keys": False},
    {"sort_keys": True, "indent": 2},
    {"sort_keys": False, "indent": 2},
]

tested = 0
matches = []
for include_dirs in (False, True):
    for shape in shapes:
        for wrapper_index, wrapper in enumerate(wrappers):
            for options in dump_options:
                for newline in (False, True):
                    tested += 1
                    good = True
                    for root, expected in TREES.items():
                        document = wrapper(records(root, include_dirs, shape))
                        encoded = json.dumps(document, **options)
                        if newline:
                            encoded += "\n"
                        if hashlib.sha256(encoded.encode()).hexdigest() != expected:
                            good = False
                            break
                    if good:
                        matches.append(
                            (include_dirs, shape, wrapper_index, options, newline)
                        )

print(f"tested={tested}")
print(f"matches={len(matches)}")
for match in matches:
    print(match)
