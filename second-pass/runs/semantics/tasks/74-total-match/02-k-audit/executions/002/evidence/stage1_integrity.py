#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-style tree digest, rejecting links and special entries."""
    root_mode = root.lstat().st_mode
    if not stat.S_ISDIR(root_mode):
        raise ValueError(f"not a real directory: {root}")
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
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


def require(path: Path, kind: str) -> None:
    mode = path.lstat().st_mode
    ok = stat.S_ISREG(mode) if kind == "file" else stat.S_ISDIR(mode)
    print(f"REQUIRED {kind:4s} {'OK' if ok else 'BAD'} {path}")
    if not ok:
        raise AssertionError(f"wrong type for required {kind}: {path}")


def compare_trees(left: Path, right: Path) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            elif stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            else:
                result[relative] = ("special", None)
        return result

    a = entries(left)
    b = entries(right)
    print(f"SEMANTICS_ENTRY_COUNT trusted={len(a)} candidate={len(b)}")
    differences: list[str] = []
    for name in sorted(set(a) | set(b)):
        if a.get(name) != b.get(name):
            differences.append(f"{name}: trusted={a.get(name)} candidate={b.get(name)}")
    if differences:
        print("SEMANTICS_DIFFERENCES")
        print("\n".join(differences))
        raise AssertionError("supplied semantics trees differ")
    print("SEMANTICS_RECURSIVE_COMPARE OK")


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    status = "OK" if actual == expected else "MISMATCH"
    print(f"HASH {label:34s} {status} actual={actual} expected={expected}")
    if actual != expected:
        raise AssertionError(f"hash mismatch: {label}")


def main() -> None:
    require(AUDIT, "file")
    data = json.loads(AUDIT.read_text())
    print(f"RECORD_LAYOUT {data['record_layout']}")
    print(f"SEMANTICS_MODE {data['semantics_mode']}")
    assert data["record_layout"] == "legacy-selected-stage1"
    assert data["semantics_mode"] == "SUPPLIED_SEMANTICS"

    required_files = [
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    for path in required_files:
        require(path, "file")
    # usage.json is optional for this legacy layout, but present and therefore checked.
    require(Path("/generation-evidence/usage.json"), "file")
    for path in [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
        Path("/generation-evidence/codex-trace"),
    ]:
        require(path, "dir")
    for path in [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
    ]:
        require(path, "file")

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    print(f"CAMPAIGN_BLOCK_EQUAL {lock == data['audit_campaign']}")
    assert lock == data["audit_campaign"]

    h = data["hashes"]
    file_checks = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    for label, path in file_checks.items():
        check_hash(label, path, h[label])

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    for relative, expected in result["outputs"]["evidence"].items():
        check_hash(f"result.outputs[{relative}]", Path("/generation-evidence") / relative, expected)
    print(f"INVOCATION_OUTPUTS_EQUAL_RESULT {invocation['outputs'] == result['outputs']}")
    assert invocation["outputs"] == result["outputs"]

    prompt_equal = Path("/reference/prompt.py").read_bytes() == Path("/candidate/prompt.py").read_bytes()
    translator_equal = (
        Path("/reference/py2mpy.py").read_bytes() == Path("/candidate/py2mpy.py").read_bytes()
    )
    print(f"PROMPT_BYTE_IDENTITY {prompt_equal}")
    print(f"TRANSLATOR_BYTE_IDENTITY {translator_equal}")
    assert prompt_equal and translator_equal
    compare_trees(Path("/reference/reference-semantics"), Path("/candidate/reference-semantics"))

    for root in [
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
        Path("/candidate"),
        Path("/generation-evidence/codex-trace"),
    ]:
        print(f"TREE_SHA256 {root} {sha256_tree(root)}")
    trusted_tree = sha256_tree(Path("/reference/reference-semantics"))
    candidate_semantics_tree = sha256_tree(Path("/candidate/reference-semantics"))
    assert trusted_tree == candidate_semantics_tree
    assert trusted_tree == h["trusted_reference_semantics_manifest_sha256"]
    assert result["outputs"]["workspace_sha256"] == sha256_tree(Path("/candidate"))
    assert invocation["retained_workspace_sha256"] == sha256_tree(Path("/candidate"))
    assert json.loads(Path("/generation-evidence/usage.json").read_text())["source_trace_sha256"] == sha256_tree(
        Path("/generation-evidence/codex-trace")
    )

    task = json.loads(Path("/task.json").read_text())
    run = json.loads(Path("/run.json").read_text())
    embedded_manifest = dict(data["manifest"])
    embedded_config = embedded_manifest.pop("config")
    print(f"TASK_MATCHES_EMBEDDED_MANIFEST_COMMON_FIELDS {task == embedded_manifest}")
    print(f"EMBEDDED_MANIFEST_CONFIG_MATCH {embedded_config == data['config']}")
    print(f"PROBLEM_ID_MATCH {task['problem_id'] == data['problem_id']}")
    print(f"RUN_CONFIG_MATCH {run['config'] == data['config']}")
    assert task == embedded_manifest
    assert embedded_config == data["config"]
    assert task["problem_id"] == data["problem_id"]
    assert run["config"] == data["config"]
    print("STAGE1_INTEGRITY_RESULT OK")


if __name__ == "__main__":
    main()
