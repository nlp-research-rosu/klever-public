#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        raise AssertionError(f"missing or unreadable required path {path}: {err}") from err
    assert stat.S_ISREG(mode), f"required path is not a regular file: {path}"
    assert not path.is_symlink(), f"required path is a symlink: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def compare_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, (
        f"{label} hash mismatch: expected {expected}, got {actual} for {path}"
    )
    print(f"PASS hash {label}: {actual}  {path}")


def tree_inventory(root: Path) -> str:
    """Print a path/type/content-hash inventory and return its own stable digest."""
    assert root.is_dir() and not root.is_symlink(), f"bad tree root: {root}"
    records: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise AssertionError(f"symlinked tree entry: {path} -> {os.readlink(path)}")
        if stat.S_ISDIR(mode):
            record = f"d\\0{rel}"
        elif stat.S_ISREG(mode):
            record = f"f\\0{rel}\\0{sha256(path)}"
        else:
            raise AssertionError(f"mistyped tree entry: {path}")
        records.append(record)
        print(f"TREE {root}: {record.replace(chr(0), ' ')}")
    result = hashlib.sha256(("\n".join(records) + "\n").encode()).hexdigest()
    print(f"INDEPENDENT_TREE_INVENTORY_SHA256 {root}: {result}")
    return result


def main() -> int:
    require_regular(AUDIT_INPUT)
    audit_input = json.loads(AUDIT_INPUT.read_text())
    assert audit_input["record_layout"] == "legacy-selected-stage1"
    assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
    paths = {key: Path(value) for key, value in audit_input["container_paths"].items()}
    hashes = audit_input["hashes"]

    required_declared = [
        "audit_campaign_lock",
        "candidate",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "generation_root",
        "generation_trace",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    ]
    assert set(required_declared).issubset(paths)
    for key in required_declared:
        path = paths[key]
        mode = path.lstat().st_mode
        assert not stat.S_ISLNK(mode), f"launcher-declared mount is symlinked: {path}"
        assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), (
            f"launcher-declared mount has wrong type: {path}"
        )
        print(f"PASS declared mount {key}: {path}")

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    assert lock == audit_input["audit_campaign"], (
        "campaign lock JSON differs from audit-input audit_campaign block"
    )
    print("PASS campaign lock exactly matches audit_input.audit_campaign")

    direct_hashes = [
        ("audit_campaign_lock_sha256", paths["audit_campaign_lock"]),
        ("canonical_sha256", paths["canonical"]),
        ("trusted_prompt_sha256", paths["trusted_prompt"]),
        ("trusted_translator_sha256", paths["translator"]),
        ("run_manifest_sha256", paths["run_manifest"]),
        ("task_manifest_sha256", paths["task_manifest"]),
        ("manifest_sha256", paths["task_manifest"]),
        ("stage1_result_sha256", paths["stage1_result"]),
        ("stage1_invocation_sha256", paths["generation_manifest"]),
        ("generation_metrics_sha256", paths["generation_metrics"]),
        ("generation_codex_last_sha256", paths["generation_last"]),
        ("generation_codex_output_sha256", paths["generation_output"]),
        ("generation_prompt_sha256", paths["generation_root"] / "prompt.txt"),
        ("generation_usage_sha256", paths["generation_root"] / "usage.json"),
        ("candidate_prompt_sha256", paths["candidate"] / "prompt.py"),
        ("candidate_translator_sha256", paths["candidate"] / "py2mpy.py"),
    ]
    for label, path in direct_hashes:
        compare_hash(label, path, hashes[label])

    assert (paths["candidate"] / "prompt.py").read_bytes() == paths[
        "trusted_prompt"
    ].read_bytes()
    assert (paths["candidate"] / "py2mpy.py").read_bytes() == paths[
        "translator"
    ].read_bytes()
    print("PASS candidate prompt and translator are byte-identical to trusted mounts")

    forbidden = Path("/reference/reference-semantics")
    assert not forbidden.exists() and not forbidden.is_symlink(), (
        "GENERATED_SEMANTICS boundary violated by reference-semantics mount"
    )
    assert hashes["trusted_reference_semantics_sha256"] is None
    assert hashes["candidate_reference_semantics_sha256"] is None
    print("PASS GENERATED_SEMANTICS boundary: no reference semantics is mounted")

    required_legacy_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required_legacy_records:
        require_regular(path)
        print(f"PASS required legacy-selected-stage1 record: {path}")
    if Path("/generation-evidence/usage.json").exists():
        require_regular(Path("/generation-evidence/usage.json"))
        print("PASS optional-present usage record")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    evidence_hashes = result["outputs"]["evidence"]
    assert evidence_hashes == invocation["outputs"]["evidence"]
    print("PASS generation-result and invocation evidence hash maps agree")
    for rel, expected in sorted(evidence_hashes.items()):
        compare_hash(f"result.outputs.evidence[{rel}]", paths["generation_root"] / rel, expected)

    trace_files = sorted(
        path for path in paths["generation_trace"].rglob("*") if path.is_file()
    )
    assert trace_files, "structured trace tree is empty"
    for path in trace_files:
        rel = path.relative_to(paths["generation_root"]).as_posix()
        assert rel in evidence_hashes, f"unrecorded trace file: {rel}"
    print(f"PASS structured trace file set: {len(trace_files)} file(s)")

    tree_inventory(paths["generation_trace"])
    tree_inventory(paths["candidate"])

    trace_events = 0
    for path in trace_files:
        with path.open() as stream:
            for line_no, line in enumerate(stream, 1):
                try:
                    json.loads(line)
                except Exception as err:
                    raise AssertionError(
                        f"malformed structured trace event {path}:{line_no}: {err}"
                    ) from err
                trace_events += 1
    print(f"PASS parsed every structured trace JSON event: {trace_events}")
    print("PROVENANCE_CHECK: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as err:
        print(f"PROVENANCE_CHECK: FAIL: {err}", file=sys.stderr)
        raise
