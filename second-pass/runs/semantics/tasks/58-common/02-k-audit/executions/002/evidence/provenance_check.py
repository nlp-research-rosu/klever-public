#!/usr/bin/env python3
"""Independent integrity checks for the mounted 58-common audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode):
        raise AssertionError(f"symlink forbidden: {path}")
    if not stat.S_ISREG(info.st_mode):
        raise AssertionError(f"not a regular file: {path}")
    if not os.access(path, os.R_OK):
        raise AssertionError(f"not readable: {path}")


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            result[rel] = ("symlink", os.readlink(path))
        elif stat.S_ISDIR(info.st_mode):
            result[rel] = ("directory", None)
        elif stat.S_ISREG(info.st_mode):
            result[rel] = ("file", sha256(path))
        else:
            result[rel] = ("other", None)
    return result


def manifest_sha(entries: dict[str, tuple[str, str | None]]) -> str:
    digest = hashlib.sha256()
    for rel, (kind, content_hash) in sorted(entries.items()):
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(kind.encode())
        digest.update(b"\0")
        digest.update((content_hash or "").encode())
        digest.update(b"\n")
    return digest.hexdigest()


def pipeline_tree_sha(root: Path) -> str:
    """Independently implement the recorded pipeline-v2 tree-hash format."""
    entries = tree_entries(root)
    digest = hashlib.sha256()
    for rel, (kind, _) in sorted(entries.items()):
        encoded = rel.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            path = root / rel
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def main() -> None:
    require_regular(AUDIT)
    require_regular(LOCK)
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True
    assert lock == audit["audit_campaign"]
    assert sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
    print("campaign_lock: exact structural and recorded-hash match")

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "usage.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
        REFERENCE / "canonical.py",
        REFERENCE / "prompt.py",
        REFERENCE / "py2mpy.py",
    ]
    trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert trace_files, "structured trace is empty"
    required.extend(trace_files)
    for path in required:
        require_regular(path)
    print(f"required_regular_files: {len(required)} readable, regular, non-symlink")

    recorded = {
        LOCK: "audit_campaign_lock_sha256",
        REFERENCE / "canonical.py": "canonical_sha256",
        REFERENCE / "prompt.py": "trusted_prompt_sha256",
        REFERENCE / "py2mpy.py": "trusted_translator_sha256",
        CANDIDATE / "prompt.py": "candidate_prompt_sha256",
        CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
        GENERATION / "invocation.json": "stage1_invocation_sha256",
        GENERATION / "metrics.json": "generation_metrics_sha256",
        GENERATION / "usage.json": "generation_usage_sha256",
        GENERATION / "codex-last.txt": "generation_codex_last_sha256",
        GENERATION / "codex-output.log": "generation_codex_output_sha256",
        GENERATION / "prompt.txt": "generation_prompt_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
    }
    for path, key in recorded.items():
        actual = sha256(path)
        expected = audit["hashes"][key]
        assert actual == expected, (path, actual, expected)
        print(f"sha256_match {key} {actual} {path}")

    assert (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()
    print("candidate_prompt_and_translator: byte-identical to trusted mounts")

    trusted_entries = tree_entries(REFERENCE / "reference-semantics")
    candidate_entries = tree_entries(CANDIDATE / "reference-semantics")
    assert trusted_entries == candidate_entries
    assert all(kind != "symlink" for kind, _ in trusted_entries.values())
    print(f"reference_semantics: exact recursive match across {len(trusted_entries)} entries")
    print(f"reference_semantics_independent_manifest_sha256: {manifest_sha(trusted_entries)}")
    trusted_pipeline_hash = pipeline_tree_sha(REFERENCE / "reference-semantics")
    assert (
        trusted_pipeline_hash
        == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    )
    print(f"reference_semantics_pipeline_tree_sha256_match: {trusted_pipeline_hash}")

    for name in ("solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"):
        require_regular(CANDIDATE / name)
    candidate_entries_all = tree_entries(CANDIDATE)
    assert all(kind != "symlink" for kind, _ in candidate_entries_all.values())
    print(f"candidate_tree_entries: {len(candidate_entries_all)}; no symlinks or special entries")
    print(f"candidate_independent_manifest_sha256: {manifest_sha(candidate_entries_all)}")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((GENERATION / "invocation.json").read_text())
    metrics = json.loads((GENERATION / "metrics.json").read_text())
    usage = json.loads((GENERATION / "usage.json").read_text())
    run = json.loads(Path("/run.json").read_text())
    task = json.loads(Path("/task.json").read_text())
    assert result["session_id"] == invocation["session_id"]
    assert result["status"] == invocation["status"] == metrics["status"] == "SUCCEEDED"
    assert task["problem_id"] == audit["problem_id"] == "58-common"
    assert task["condition"]["name"] == run["condition"]["name"] == audit["condition"]
    assert usage["status"] == "COMPLETE"
    candidate_pipeline_hash = pipeline_tree_sha(CANDIDATE)
    assert candidate_pipeline_hash == result["outputs"]["workspace_sha256"]
    assert candidate_pipeline_hash == invocation["retained_workspace_sha256"]
    print(f"candidate_pipeline_tree_sha256_match: {candidate_pipeline_hash}")
    trace_pipeline_hash = pipeline_tree_sha(GENERATION / "codex-trace")
    assert trace_pipeline_hash == usage["source_trace_sha256"]
    print(f"trace_pipeline_tree_sha256_match: {trace_pipeline_hash}")

    output_hashes = result["outputs"]["evidence"]
    for rel, expected in output_hashes.items():
        path = GENERATION / rel
        require_regular(path)
        actual = sha256(path)
        assert actual == expected, (path, actual, expected)
        print(f"generation_result_hash_match {actual} {rel}")

    trace_line_count = 0
    trace_type_counts: dict[str, int] = {}
    for path in trace_files:
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                event = json.loads(line)
                event_type = event.get("type", "<missing>")
                trace_type_counts[event_type] = trace_type_counts.get(event_type, 0) + 1
                trace_line_count += 1
    print(f"trace_json_lines: {trace_line_count}; top-level-types={trace_type_counts}")

    output_text = (GENERATION / "codex-output.log").read_text(errors="strict")
    print(
        "generation_log_markers:",
        {
            "#Top": output_text.count("#Top"),
            "KPROVE_PASSED": output_text.count("KPROVE_PASSED"),
            "WarnStuckClaimState": output_text.count("WarnStuckClaimState"),
        },
    )
    print("PROVENANCE_CHECK_OK")


if __name__ == "__main__":
    main()
