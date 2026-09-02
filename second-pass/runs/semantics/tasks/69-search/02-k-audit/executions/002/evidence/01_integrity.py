#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def tree_manifest(root: Path) -> list[dict[str, object]]:
    assert root.is_dir() and not root.is_symlink(), f"bad tree root: {root}"
    rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        assert not stat.S_ISLNK(mode), f"symlink in tree: {path}"
        if stat.S_ISDIR(mode):
            kind = "directory"
            size = None
            sha256 = None
        elif stat.S_ISREG(mode):
            kind = "file"
            size = path.stat().st_size
            sha256 = digest(path)
        else:
            raise AssertionError(f"unsupported entry type: {path}")
        rows.append({"path": rel, "kind": kind, "size": size, "sha256": sha256})
    return rows


def manifest_digest(rows: list[dict[str, object]]) -> str:
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    require_regular(AUDIT)
    require_regular(LOCK)
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    actual_lock_hash = digest(LOCK)
    assert actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"audit_input_sha256={digest(AUDIT)}")
    print(f"campaign_lock_sha256={actual_lock_hash}")
    print("campaign_block_matches_lock=true")

    required = [
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
    for path in required:
        require_regular(path)
        print(f"regular {path} sha256={digest(path)} size={path.stat().st_size}")

    recorded_file_hashes = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    }
    for path, key in recorded_file_hashes.items():
        assert digest(path) == audit["hashes"][key], f"recorded hash mismatch: {path}"
    print("all_launcher_recorded_file_hashes_match=true")

    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        require_regular(usage)
        assert digest(usage) == audit["hashes"]["generation_usage_sha256"]
        print(f"usage_present sha256={digest(usage)}")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_rows = tree_manifest(trace_root)
    trace_files = [row for row in trace_rows if row["kind"] == "file"]
    assert trace_files, "structured trace is empty"
    expected_trace_file_hashes = json.loads(Path("/generation-result.json").read_text())[
        "outputs"
    ]["evidence"]
    for row in trace_files:
        key = f"codex-trace/{row['path']}"
        assert row["sha256"] == expected_trace_file_hashes[key]
    print(f"trace_file_count={len(trace_files)}")
    print(f"independent_trace_manifest_sha256={manifest_digest(trace_rows)}")

    candidate_prompt = Path("/candidate/prompt.py")
    candidate_translator = Path("/candidate/py2mpy.py")
    require_regular(candidate_prompt)
    require_regular(candidate_translator)
    assert candidate_prompt.read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert candidate_translator.read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("candidate_prompt_byte_identical=true")
    print("candidate_translator_byte_identical=true")

    trusted_root = Path("/reference/reference-semantics")
    candidate_root = Path("/candidate/reference-semantics")
    trusted_rows = tree_manifest(trusted_root)
    candidate_rows = tree_manifest(candidate_root)
    assert trusted_rows == candidate_rows, "candidate supplied-semantics tree differs"
    print(f"semantics_entry_count={len(trusted_rows)}")
    print(f"independent_semantics_manifest_sha256={manifest_digest(trusted_rows)}")
    print("candidate_reference_semantics_recursively_identical=true")

    candidate_rows_all = tree_manifest(Path("/candidate"))
    print(f"candidate_entry_count={len(candidate_rows_all)}")
    print(f"independent_candidate_manifest_sha256={manifest_digest(candidate_rows_all)}")
    for name in ["solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"]:
        require_regular(Path("/candidate") / name)
        print(f"candidate_required_artifact_regular={name}")

    print("INTEGRITY_CHECK=PASS")


if __name__ == "__main__":
    main()
