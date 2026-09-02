#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """The pipeline-v2 content-manifest digest, independently reimplemented."""
    mode = root.lstat().st_mode
    assert stat.S_ISDIR(mode) and not root.is_symlink(), root
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
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
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    assert not path.is_symlink(), f"symlinked directory: {path}"


def compare_trees(left: Path, right: Path) -> None:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            else:
                result[relative] = ("linked-or-other", None)
        return result

    left_inventory = inventory(left)
    right_inventory = inventory(right)
    assert left_inventory == right_inventory, "candidate/trusted semantics trees differ"
    assert all(kind != "linked-or-other" for kind, _ in left_inventory.values())
    print(f"semantics_recursive_entries={len(left_inventory)} exact_match=true")


def check_recorded_file(
    label: str, path: Path, expected: str, *, required: bool = True
) -> None:
    if not path.exists() and not required:
        print(f"{label}: absent (optional)")
        return
    require_regular(path)
    actual = sha256_file(path)
    print(f"{label}: actual={actual} expected={expected}")
    assert actual == expected, label


def main() -> None:
    require_regular(AUDIT)
    require_regular(LOCK)
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True
    assert audit["audit_campaign"] == lock
    task_manifest = json.loads(Path("/task.json").read_text())
    assert all(audit["manifest"].get(key) == value for key, value in task_manifest.items())
    assert audit["manifest"].get("config") == audit["config"]
    print("campaign_lock_matches_audit_block=true")

    hashes = audit["hashes"]
    direct = [
        ("audit_campaign_lock", LOCK, "audit_campaign_lock_sha256"),
        ("run_manifest", Path("/run.json"), "run_manifest_sha256"),
        ("task_manifest", Path("/task.json"), "task_manifest_sha256"),
        ("stage1_result", Path("/generation-result.json"), "stage1_result_sha256"),
        (
            "stage1_invocation",
            GENERATION / "invocation.json",
            "stage1_invocation_sha256",
        ),
        ("generation_metrics", GENERATION / "metrics.json", "generation_metrics_sha256"),
        ("generation_usage", GENERATION / "usage.json", "generation_usage_sha256"),
        (
            "generation_codex_last",
            GENERATION / "codex-last.txt",
            "generation_codex_last_sha256",
        ),
        (
            "generation_codex_output",
            GENERATION / "codex-output.log",
            "generation_codex_output_sha256",
        ),
        ("generation_prompt", GENERATION / "prompt.txt", "generation_prompt_sha256"),
        ("canonical", REFERENCE / "canonical.py", "canonical_sha256"),
        ("trusted_prompt", REFERENCE / "prompt.py", "trusted_prompt_sha256"),
        ("trusted_translator", REFERENCE / "py2mpy.py", "trusted_translator_sha256"),
        ("candidate_prompt", CANDIDATE / "prompt.py", "candidate_prompt_sha256"),
        ("candidate_translator", CANDIDATE / "py2mpy.py", "candidate_translator_sha256"),
    ]
    for label, path, hash_key in direct:
        check_recorded_file(label, path, hashes[hash_key])

    # Runtime metrics were never recorded in this legacy-selected-stage1 layout.
    assert not (GENERATION / "runtime-metrics.json").exists()
    print("runtime_metrics_absent_and_not_required=true")

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in required_candidate:
        require_regular(CANDIDATE / name)
    for root in [CANDIDATE, REFERENCE, GENERATION, GENERATION / "codex-trace"]:
        require_directory(root)

    assert (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()
    compare_trees(
        CANDIDATE / "reference-semantics", REFERENCE / "reference-semantics"
    )

    candidate_semantics_manifest = sha256_tree(CANDIDATE / "reference-semantics")
    trusted_semantics_manifest = sha256_tree(REFERENCE / "reference-semantics")
    print(f"candidate_semantics_manifest={candidate_semantics_manifest}")
    print(f"trusted_semantics_manifest={trusted_semantics_manifest}")
    assert candidate_semantics_manifest == hashes[
        "trusted_reference_semantics_manifest_sha256"
    ]
    assert trusted_semantics_manifest == hashes[
        "trusted_reference_semantics_manifest_sha256"
    ]

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((GENERATION / "invocation.json").read_text())
    candidate_manifest = sha256_tree(CANDIDATE)
    print(f"candidate_pipeline_manifest={candidate_manifest}")
    assert candidate_manifest == result["outputs"]["workspace_sha256"]
    assert candidate_manifest == invocation["retained_workspace_sha256"]

    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = GENERATION / relative
        check_recorded_file(f"result_evidence/{relative}", path, expected)

    trace_manifest = sha256_tree(GENERATION / "codex-trace")
    usage = json.loads((GENERATION / "usage.json").read_text())
    print(f"trace_pipeline_manifest={trace_manifest}")
    assert trace_manifest == usage["source_trace_sha256"]
    jsonl_files = sorted((GENERATION / "codex-trace").rglob("*.jsonl"))
    assert jsonl_files
    event_types: Counter[str] = Counter()
    lines = 0
    for path in jsonl_files:
        require_regular(path)
        with path.open() as stream:
            for raw in stream:
                record = json.loads(raw)
                assert isinstance(record, dict)
                event_types[str(record.get("type"))] += 1
                lines += 1
    print(f"structured_trace_json_lines={lines}")
    print("structured_trace_event_types=" + json.dumps(event_types, sort_keys=True))
    assert lines == 259

    for path in [Path("/run.json"), Path("/task.json"), Path("/generation-result.json")]:
        document = json.loads(path.read_text())
        assert isinstance(document, dict)
    print("required_json_records_parse=true")
    print("INTEGRITY_STATUS=PASS")


if __name__ == "__main__":
    main()
