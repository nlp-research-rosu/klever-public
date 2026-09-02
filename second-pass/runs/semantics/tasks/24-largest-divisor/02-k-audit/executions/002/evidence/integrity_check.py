#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Independently reproduce tools.pipeline_contract.sha256_tree."""
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
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
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required regular file is mistyped: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"required directory is mistyped: {path}")
    next(os.scandir(path), None)


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            result[relative] = ("directory", None)
        elif stat.S_ISREG(mode):
            result[relative] = ("file", sha256_file(path))
        else:
            result[relative] = ("unsupported", None)
    return result


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert lock == audit["audit_campaign"]
    lock_hash = sha256_file(LOCK)
    print(f"audit_campaign_lock_sha256={lock_hash}")
    assert lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]

    container_paths = {
        key: Path(value) for key, value in audit["container_paths"].items()
    }
    regular_container_keys = {
        "audit_campaign_lock",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    }
    directory_container_keys = {
        "candidate",
        "generation_root",
        "generation_trace",
    }
    for key in sorted(regular_container_keys):
        require_regular(container_paths[key])
        print(f"container_regular[{key}]={container_paths[key]}")
    for key in sorted(directory_container_keys):
        require_directory(container_paths[key])
        print(f"container_directory[{key}]={container_paths[key]}")

    required_layout_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required_layout_records.append(usage)
    for path in required_layout_records:
        require_regular(path)
        print(f"required_record={path}")

    singleton_expectations = {
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    if usage.exists():
        singleton_expectations[usage] = "generation_usage_sha256"
    for path, hash_key in singleton_expectations.items():
        actual = sha256_file(path)
        expected = audit["hashes"][hash_key]
        print(f"sha256[{path}]={actual} expected={expected}")
        assert actual == expected

    run = json.loads(Path("/run.json").read_text())
    task = json.loads(Path("/task.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    metrics = json.loads(Path("/generation-evidence/metrics.json").read_text())
    if usage.exists():
        json.loads(usage.read_text())
    embedded_manifest = audit["manifest"]
    assert all(
        embedded_manifest.get(key) == value for key, value in task.items()
    )
    assert embedded_manifest["config"] == audit["config"]
    assert task["problem_id"] == audit["problem_id"] == "24-largest-divisor"
    assert run["run_id"] == audit["run_id"]
    assert invocation["stage"] == result["stage"] == "01-k-proof"
    assert metrics["exit_code"] == invocation["exit_code"] == 0
    assert result["outputs"]["evidence"] == invocation["outputs"]["evidence"]

    generation_root = Path("/generation-evidence")
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = generation_root / relative
        require_regular(path)
        actual = sha256_file(path)
        print(f"generation_output_sha256[{relative}]={actual} expected={expected}")
        assert actual == expected

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    require_directory(trusted_semantics)
    require_directory(candidate_semantics)
    trusted_manifest = tree_manifest(trusted_semantics)
    candidate_manifest = tree_manifest(candidate_semantics)
    assert trusted_manifest == candidate_manifest
    assert all(kind != "unsupported" for kind, _ in trusted_manifest.values())
    print(f"reference_semantics_entries={len(trusted_manifest)}")
    print("candidate_reference_semantics_recursive_byte_comparison=MATCH")
    trusted_tree_hash = pipeline_tree_sha256(trusted_semantics)
    candidate_sem_tree_hash = pipeline_tree_sha256(candidate_semantics)
    print(f"trusted_reference_semantics_pipeline_tree_sha256={trusted_tree_hash}")
    print(f"candidate_reference_semantics_pipeline_tree_sha256={candidate_sem_tree_hash}")
    assert trusted_tree_hash == candidate_sem_tree_hash
    assert (
        trusted_tree_hash
        == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    )

    assert Path("/reference/prompt.py").read_bytes() == Path(
        "/candidate/prompt.py"
    ).read_bytes()
    assert Path("/reference/py2mpy.py").read_bytes() == Path(
        "/candidate/py2mpy.py"
    ).read_bytes()
    print("candidate_prompt_recursive_comparison=MATCH")
    print("candidate_translator_recursive_comparison=MATCH")

    candidate_tree_hash = pipeline_tree_sha256(Path("/candidate"))
    trace_tree_hash = pipeline_tree_sha256(
        Path("/generation-evidence/codex-trace")
    )
    print(f"candidate_pipeline_tree_sha256={candidate_tree_hash}")
    print(f"trace_pipeline_tree_sha256={trace_tree_hash}")
    assert candidate_tree_hash == result["outputs"]["workspace_sha256"]
    assert candidate_tree_hash == invocation["retained_workspace_sha256"]
    if usage.exists():
        usage_document = json.loads(usage.read_text())
        assert (
            trace_tree_hash == usage_document["source_trace_sha256"]
        )

    trace_files = sorted(
        Path("/generation-evidence/codex-trace").rglob("*.jsonl")
    )
    assert trace_files
    trace_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    line_count = 0
    for path in trace_files:
        require_regular(path)
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                item = json.loads(line)
                assert isinstance(item, dict)
                line_count += 1
                trace_types[str(item.get("type"))] += 1
                payload = item.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
        print(
            f"trace_file={path} lines={line_number} "
            f"sha256={sha256_file(path)}"
        )
    print(f"trace_json_objects={line_count}")
    print(f"trace_record_types={dict(sorted(trace_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")

    all_roots = [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ]
    unsupported = []
    for root in all_roots:
        for path in root.rglob("*"):
            mode = path.lstat().st_mode
            if not stat.S_ISREG(mode) and not stat.S_ISDIR(mode):
                unsupported.append(str(path))
    print(f"linked_or_unsupported_entries={unsupported}")
    assert not unsupported
    print("INTEGRITY_CHECK=PASS")


if __name__ == "__main__":
    main()
