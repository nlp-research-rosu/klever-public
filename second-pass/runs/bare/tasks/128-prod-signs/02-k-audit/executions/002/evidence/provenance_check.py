#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN = Path("/generation-evidence")
TRACE = GEN / "codex-trace"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a directory: {path}"
    assert not path.is_symlink(), f"symlinked directory: {path}"


def check_tree_nodes(root: Path) -> list[tuple[str, str, int, str | None]]:
    result = []
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in sorted(dirnames + filenames):
            path = directory_path / name
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                kind = "directory"
                digest = None
            elif stat.S_ISREG(mode):
                kind = "file"
                digest = sha256(path)
            else:
                raise AssertionError(f"linked or unsupported node: {path}")
            result.append((relative, kind, stat.S_IMODE(mode), digest))
    return sorted(result)


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the recorded generation workspace/tree digest."""
    digest = hashlib.sha256()
    entries = check_tree_nodes(root)
    for relative, kind, _mode, _file_digest in entries:
        path = root / relative
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.lstat().st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/provenance_check.py")
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

    required_files = [
        AUDIT_INPUT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GEN / "invocation.json",
        GEN / "metrics.json",
        GEN / "codex-last.txt",
        GEN / "codex-output.log",
        GEN / "prompt.txt",
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    if (GEN / "usage.json").exists():
        required_files.append(GEN / "usage.json")
    required_directories = [Path("/candidate"), GEN, TRACE, Path("/reference")]
    for path in required_files:
        require_regular(path)
    for path in required_directories:
        require_directory(path)

    # legacy-selected-stage1 does not require never-recorded runtime metrics.
    assert not (GEN / "runtime-metrics.json").exists()
    # The declared generated-semantics mode forbids a mounted reference semantics.
    assert not Path("/reference/reference-semantics").exists()

    assert lock == audit["audit_campaign"]
    expected_hashes = {
        LOCK: audit["hashes"]["audit_campaign_lock_sha256"],
        Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
        Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
        Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
        GEN / "invocation.json": audit["hashes"]["stage1_invocation_sha256"],
        GEN / "metrics.json": audit["hashes"]["generation_metrics_sha256"],
        GEN / "codex-last.txt": audit["hashes"]["generation_codex_last_sha256"],
        GEN / "codex-output.log": audit["hashes"]["generation_codex_output_sha256"],
        GEN / "prompt.txt": audit["hashes"]["generation_prompt_sha256"],
        GEN / "usage.json": audit["hashes"]["generation_usage_sha256"],
        Path("/reference/canonical.py"): audit["hashes"]["canonical_sha256"],
        Path("/reference/prompt.py"): audit["hashes"]["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): audit["hashes"]["trusted_translator_sha256"],
        Path("/candidate/prompt.py"): audit["hashes"]["candidate_prompt_sha256"],
        Path("/candidate/py2mpy.py"): audit["hashes"]["candidate_translator_sha256"],
    }
    for path, expected in expected_hashes.items():
        actual = sha256(path)
        assert actual == expected, f"hash mismatch: {path}: {actual} != {expected}"

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()

    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    invocation = json.loads((GEN / "invocation.json").read_text(encoding="utf-8"))
    for relative, expected in result["outputs"]["evidence"].items():
        path = GEN / relative
        require_regular(path)
        assert sha256(path) == expected, f"generation-result hash mismatch: {relative}"
        assert invocation["outputs"]["evidence"][relative] == expected

    candidate_manifest = check_tree_nodes(Path("/candidate"))
    generation_manifest = check_tree_nodes(GEN)
    reference_manifest = check_tree_nodes(Path("/reference"))
    candidate_pipeline_hash = pipeline_tree_sha256(Path("/candidate"))
    assert candidate_pipeline_hash == result["outputs"]["workspace_sha256"]
    assert candidate_pipeline_hash == invocation["outputs"]["workspace_sha256"]

    trace_files = [
        path
        for path in TRACE.rglob("*")
        if stat.S_ISREG(path.lstat().st_mode)
    ]
    assert trace_files, "structured trace is empty"
    trace_type_counts: Counter[str] = Counter()
    trace_payload_type_counts: Counter[str] = Counter()
    trace_lines = 0
    for path in sorted(trace_files):
        require_regular(path)
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            record = json.loads(line)
            trace_lines += 1
            trace_type_counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                trace_payload_type_counts[str(payload.get("type"))] += 1
    trace_pipeline_hash = pipeline_tree_sha256(TRACE)
    usage = json.loads((GEN / "usage.json").read_text(encoding="utf-8"))
    assert trace_pipeline_hash == usage["source_trace_sha256"]

    output = (GEN / "codex-output.log").read_text(encoding="utf-8")
    last = (GEN / "codex-last.txt").read_text(encoding="utf-8")
    assert "RESULT: KPROVE_PASSED" in output
    assert "RESULT: KPROVE_PASSED" in last
    assert "kprove spec.k" in output
    assert "#Top" in output

    print("record_layout=legacy-selected-stage1")
    print("campaign_lock_content_match=true")
    print("all_declared_regular_file_hashes_match=true")
    print("candidate_prompt_byte_match=true")
    print("candidate_translator_byte_match=true")
    print("generated_semantics_boundary_reference_semantics_absent=true")
    print("runtime_metrics_absent_but_not_required_for_legacy_selected_stage1=true")
    print(f"candidate_nodes={len(candidate_manifest)}")
    for relative, kind, mode, digest in candidate_manifest:
        print(f"candidate {kind} mode={mode:o} sha256={digest} path={relative}")
    print(f"generation_nodes={len(generation_manifest)}")
    print(f"reference_nodes={len(reference_manifest)}")
    print(
        f"candidate_pipeline_tree_sha256={candidate_pipeline_hash} "
        "matches_generation_workspace=true"
    )
    print(f"trace_files={len(trace_files)} trace_json_records={trace_lines}")
    print(
        f"trace_pipeline_tree_sha256={trace_pipeline_hash} "
        "matches_usage_source_trace=true"
    )
    print(f"trace_record_types={dict(sorted(trace_type_counts.items()))}")
    print(
        "trace_payload_types="
        f"{dict(sorted(trace_payload_type_counts.items()))}"
    )
    print("generation_claim_only=KPROVE_PASSED")
    print("STATUS: PASS")


if __name__ == "__main__":
    main()
