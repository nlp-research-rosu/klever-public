#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit records."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-v3 tree digest, independently reimplemented."""
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            mode = child.stat(follow_symlinks=False).st_mode
            path = Path(child.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_file(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    print(f"OK regular file {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    print(f"OK real directory {path}")


def compare_hash(path: Path, expected: str) -> None:
    actual = sha256_file(path)
    assert actual == expected, f"hash mismatch {path}: {actual} != {expected}"
    print(f"OK sha256 {path} {actual}")


def main() -> int:
    require_file(AUDIT)
    require_file(LOCK)
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    compare_hash(LOCK, audit["hashes"]["audit_campaign_lock_sha256"])
    print("OK campaign lock exactly equals audit campaign block")

    required_files = [
        AUDIT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    if Path("/generation-evidence/usage.json").exists():
        required_files.append(Path("/generation-evidence/usage.json"))
    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_file(path)
    for path in required_directories:
        require_directory(path)

    assert not Path("/reference/reference-semantics").exists()
    print("OK generated-semantics boundary: no reference-semantics mount")

    hashes = audit["hashes"]
    direct = {
        Path("/reference/canonical.py"): hashes["canonical_sha256"],
        Path("/reference/prompt.py"): hashes["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): hashes["trusted_translator_sha256"],
        Path("/candidate/prompt.py"): hashes["candidate_prompt_sha256"],
        Path("/candidate/py2mpy.py"): hashes["candidate_translator_sha256"],
        Path("/run.json"): hashes["run_manifest_sha256"],
        Path("/task.json"): hashes["task_manifest_sha256"],
        Path("/generation-result.json"): hashes["stage1_result_sha256"],
        Path("/generation-evidence/invocation.json"): hashes[
            "stage1_invocation_sha256"
        ],
        Path("/generation-evidence/metrics.json"): hashes[
            "generation_metrics_sha256"
        ],
        Path("/generation-evidence/codex-last.txt"): hashes[
            "generation_codex_last_sha256"
        ],
        Path("/generation-evidence/codex-output.log"): hashes[
            "generation_codex_output_sha256"
        ],
        Path("/generation-evidence/prompt.txt"): hashes[
            "generation_prompt_sha256"
        ],
        Path("/generation-evidence/usage.json"): hashes[
            "generation_usage_sha256"
        ],
    }
    for path, expected in direct.items():
        compare_hash(path, expected)

    task_hash = sha256_file(Path("/task.json"))
    assert task_hash == hashes["manifest_sha256"]
    assert task_hash == hashes["task_manifest_sha256"]
    print("OK manifest hash aliases identify task.json")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    candidate_tree = sha256_tree(Path("/candidate"))
    trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    assert candidate_tree == invocation["retained_workspace_sha256"]
    assert trace_tree == usage["source_trace_sha256"]
    print(f"OK candidate pipeline tree sha256 {candidate_tree}")
    print(f"OK trace pipeline tree sha256 {trace_tree}")

    for relative, expected in result["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        compare_hash(path, expected)

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("OK candidate prompt and translator are byte-identical to trusted mounts")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, KeyError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
