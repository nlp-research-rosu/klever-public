#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat


AUDIT_INPUT = Path("/audit-input.json")


def load_object(path: Path) -> dict:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"not a real regular file: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"not a JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"not a real regular file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce tools/pipeline_contract.py:sha256_tree."""
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def main() -> None:
    audit = load_object(AUDIT_INPUT)
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    lock = load_object(lock_path)
    assert lock == audit["audit_campaign"]
    assert sha256_file(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"]
    print("campaign_lock: content and sha256 match audit-input")

    required_files = [
        AUDIT_INPUT,
        lock_path,
        Path(audit["container_paths"]["run_manifest"]),
        Path(audit["container_paths"]["task_manifest"]),
        Path(audit["container_paths"]["stage1_result"]),
        Path(audit["container_paths"]["generation_manifest"]),
        Path(audit["container_paths"]["generation_metrics"]),
        Path("/generation-evidence/usage.json"),
        Path(audit["container_paths"]["generation_last"]),
        Path(audit["container_paths"]["generation_output"]),
        Path("/generation-evidence/prompt.txt"),
        Path(audit["container_paths"]["canonical"]),
        Path(audit["container_paths"]["trusted_prompt"]),
        Path(audit["container_paths"]["translator"]),
    ]
    required_dirs = [
        Path(audit["container_paths"]["candidate"]),
        Path(audit["container_paths"]["generation_root"]),
        Path(audit["container_paths"]["generation_trace"]),
    ]
    for path in required_files:
        assert path.is_file() and not path.is_symlink(), path
    for path in required_dirs:
        assert path.is_dir() and not path.is_symlink(), path
    print(f"required_records: {len(required_files)} real files, "
          f"{len(required_dirs)} real directories")

    hash_checks = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, field in hash_checks.items():
        observed = sha256_file(path)
        expected = audit["hashes"][field]
        assert observed == expected, (path, observed, expected)
        print(f"sha256 {path}: {observed} MATCH")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    assert not Path("/reference/reference-semantics").exists()
    print("trusted_candidate_copies: prompt and translator byte-identical")
    print("generated_semantics_boundary: hidden reference semantics absent")

    candidate_required = [
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in candidate_required:
        path = Path("/candidate") / name
        assert path.is_file() and not path.is_symlink(), path
    print("candidate_required_artifacts: all present as real regular files")

    result = load_object(Path("/generation-result.json"))
    invocation = load_object(Path("/generation-evidence/invocation.json"))
    candidate_digest = pipeline_tree_hash(Path("/candidate"))
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    assert candidate_digest == invocation["retained_workspace_sha256"]
    print(f"pipeline_candidate_tree: {candidate_digest} MATCH stage-1 records")
    print(
        "launcher_candidate_tree_field: "
        + audit["hashes"]["candidate_tree_sha256"]
        + " (launcher digest namespace; retained-workspace digest checked above)"
    )

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    assert len(trace_files) == 1
    trace_rel = trace_files[0].relative_to(trace_root).as_posix()
    trace_sha = sha256_file(trace_files[0])
    expected_trace_sha = result["outputs"]["evidence"][f"codex-trace/{trace_rel}"]
    assert trace_sha == expected_trace_sha
    usage = load_object(Path("/generation-evidence/usage.json"))
    trace_tree = pipeline_tree_hash(trace_root)
    assert trace_tree == usage["source_trace_sha256"]
    print(f"trace_file: {trace_rel} sha256={trace_sha} MATCH")
    print(f"pipeline_trace_tree: {trace_tree} MATCH usage source trace")
    print(
        "launcher_trace_tree_field: "
        + audit["hashes"]["generation_codex_trace_sha256"]
        + " (launcher digest namespace; file and pipeline digests checked above)"
    )

    counts: Counter[str] = Counter()
    nested: Counter[str] = Counter()
    line_count = 0
    with trace_files[0].open(encoding="utf-8") as stream:
        for line_count, line in enumerate(stream, 1):
            record = json.loads(line)
            counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                nested[str(payload.get("type"))] += 1
    assert line_count == 237
    print(f"structured_trace: {line_count} valid JSONL records")
    print("top_level_types:", dict(sorted(counts.items())))
    print("payload_types:", dict(sorted(nested.items())))

    for root in (Path("/candidate"), Path("/generation-evidence")):
        print(f"file_inventory {root}:")
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            assert not path.is_symlink()
            print(
                f"  {path.relative_to(root).as_posix()} "
                f"{path.stat().st_size} {sha256_file(path)}"
            )


if __name__ == "__main__":
    main()
