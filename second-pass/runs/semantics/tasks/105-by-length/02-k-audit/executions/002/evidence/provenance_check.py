#!/usr/bin/env python3
"""Independent integrity checks for the 105-by-length audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement /opt/humaneval/tools/pipeline_contract.py:sha256_tree."""
    mode = root.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"tree root is not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            child_mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(child_mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(child_mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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


def require_regular(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise AssertionError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise AssertionError(f"not a real directory: {path}")


def compare_trees(left: Path, right: Path) -> None:
    def manifest(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            else:
                result[relative] = ("linked/unsupported", None)
        return result

    left_manifest = manifest(left)
    right_manifest = manifest(right)
    if left_manifest != right_manifest:
        names = sorted(set(left_manifest) | set(right_manifest))
        differences = [
            (name, left_manifest.get(name), right_manifest.get(name))
            for name in names
            if left_manifest.get(name) != right_manifest.get(name)
        ]
        raise AssertionError(f"tree mismatch: {differences}")


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    if audit["record_layout"] != "legacy-selected-stage1":
        raise AssertionError(f"unexpected layout: {audit['record_layout']}")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise AssertionError(f"unexpected semantics mode: {audit['semantics_mode']}")

    required_files = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/usage.json"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_directories:
        require_directory(path)

    campaign = json.loads(
        Path("/audit-campaign-lock.json").read_text(encoding="utf-8")
    )
    assert campaign == audit["audit_campaign"], "campaign lock mismatch"

    hash_bindings = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "stage1_invocation_sha256": Path(
            "/generation-evidence/invocation.json"
        ),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
        "run_manifest_sha256": Path("/run.json"),
    }
    for key, path in hash_bindings.items():
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        assert actual == expected, f"{key}: expected {expected}, got {actual}"
        print(f"OK hash {key}={actual}")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    compare_trees(
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    )
    print("OK candidate prompt and translator byte-identical to trusted inputs")
    print("OK candidate reference-semantics tree exactly matches trusted tree")

    candidate_digest = pipeline_tree_digest(Path("/candidate"))
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    assert candidate_digest == invocation["retained_workspace_sha256"]
    assert candidate_digest == invocation["outputs"]["workspace_sha256"]
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    print(f"OK retained candidate pipeline tree digest={candidate_digest}")

    semantics_digest = pipeline_tree_digest(
        Path("/reference/reference-semantics")
    )
    assert (
        semantics_digest
        == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    )
    print(f"OK trusted semantics pipeline tree digest={semantics_digest}")

    result_hashes = result["outputs"]["evidence"]
    invocation_hashes = invocation["outputs"]["evidence"]
    for relative, expected in sorted(result_hashes.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected
        assert invocation_hashes[relative] == expected
        print(f"OK generation evidence hash {relative}={actual}")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_digest = pipeline_tree_digest(trace_root)
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    assert trace_digest == usage["source_trace_sha256"]
    outer: Counter[str | None] = Counter()
    payload: Counter[str | None] = Counter()
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    line_count = 0
    for path in trace_files:
        require_regular(path)
        with path.open(encoding="utf-8") as stream:
            for line_count, line in enumerate(stream, line_count + 1):
                record = json.loads(line)
                outer[record.get("type")] += 1
                body = record.get("payload")
                payload[body.get("type") if isinstance(body, dict) else None] += 1
    print(f"OK trace pipeline tree digest={trace_digest}")
    print(f"OK trace JSONL files={len(trace_files)} records={line_count}")
    print(f"TRACE outer types={dict(sorted(outer.items(), key=str))}")
    print(f"TRACE payload types={dict(sorted(payload.items(), key=str))}")

    for name in ("solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"):
        require_regular(Path("/candidate") / name)
    print("OK all required proof artifacts are real regular files")
    print("RESULT: PROVENANCE_INTEGRITY_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
