#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required regular file has type {stat.filemode(mode)}: {path}")
    if path.is_symlink():
        raise AssertionError(f"required regular file is a symlink: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"required directory has type {stat.filemode(mode)}: {path}")
    if path.is_symlink():
        raise AssertionError(f"required directory is a symlink: {path}")


def inspect_tree(root: Path) -> list[tuple[str, str, int, str]]:
    require_directory(root)
    records: list[tuple[str, str, int, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            records.append((relative, "directory", stat.S_IMODE(mode), "-"))
        elif stat.S_ISREG(mode):
            records.append((relative, "file", stat.S_IMODE(mode), sha256(path)))
        else:
            records.append((relative, stat.filemode(mode), stat.S_IMODE(mode), "-"))
            raise AssertionError(f"linked or unsupported tree entry: {path}")
    return records


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce the pipeline-v3 content/tree digest over real entries."""

    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((relative, "file", path))
        else:
            raise AssertionError(f"unsupported tree entry in digest: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + bytes([0]))
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def compare_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256(path)
    result = "MATCH" if actual == expected else "MISMATCH"
    print(f"HASH {label}: {result} expected={expected} actual={actual} path={path}")
    if actual != expected:
        raise AssertionError(f"{label} hash mismatch")


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    print(f"record_layout={audit_input['record_layout']}")
    print(f"problem_id={audit_input['problem_id']}")
    print(f"condition={audit_input['condition']}")
    print(f"semantics_mode={audit_input['semantics_mode']}")

    assert audit_input["record_layout"] == "legacy-selected-stage1"
    assert audit_input["problem_id"] == "25-factorize"
    assert audit_input["condition"] == "bare"
    assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit_input["mount_reference_semantics"] is False
    assert audit_input["reference_semantics"] is None

    container_paths = audit_input["container_paths"]
    required_path_keys = {
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
    }
    assert required_path_keys <= container_paths.keys()
    print("container_paths required keys: PRESENT")

    required_files = [
        Path("/audit-input.json"),
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
    ]
    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
        print(f"TYPE required regular file: OK {path}")
    for path in required_directories:
        require_directory(path)
        print(f"TYPE required directory: OK {path}")

    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        require_regular(usage)
        print("TYPE optional legacy usage.json: OK")
    runtime_metrics = Path("/generation-evidence/runtime-metrics.json")
    print(f"runtime-metrics present={runtime_metrics.exists()} (not required for this layout)")

    reference_semantics = Path("/reference/reference-semantics")
    print(f"generated-semantics boundary: reference semantics absent={not reference_semantics.exists()}")
    assert not reference_semantics.exists()

    campaign_path = Path(container_paths["audit_campaign_lock"])
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    assert campaign == audit_input["audit_campaign"]
    print("campaign lock object equals audit_input.audit_campaign: MATCH")

    hashes = audit_input["hashes"]
    compare_hash(
        "audit_campaign_lock",
        campaign_path,
        hashes["audit_campaign_lock_sha256"],
    )
    compare_hash("canonical", Path(container_paths["canonical"]), hashes["canonical_sha256"])
    compare_hash(
        "trusted_prompt",
        Path(container_paths["trusted_prompt"]),
        hashes["trusted_prompt_sha256"],
    )
    compare_hash(
        "trusted_translator",
        Path(container_paths["translator"]),
        hashes["trusted_translator_sha256"],
    )
    compare_hash("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"])
    compare_hash("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"])
    compare_hash("stage1_result", Path("/generation-result.json"), hashes["stage1_result_sha256"])
    compare_hash(
        "stage1_invocation",
        Path("/generation-evidence/invocation.json"),
        hashes["stage1_invocation_sha256"],
    )
    compare_hash(
        "generation_metrics",
        Path("/generation-evidence/metrics.json"),
        hashes["generation_metrics_sha256"],
    )
    compare_hash(
        "generation_codex_last",
        Path("/generation-evidence/codex-last.txt"),
        hashes["generation_codex_last_sha256"],
    )
    compare_hash(
        "generation_codex_output",
        Path("/generation-evidence/codex-output.log"),
        hashes["generation_codex_output_sha256"],
    )
    compare_hash(
        "generation_prompt",
        Path("/generation-evidence/prompt.txt"),
        hashes["generation_prompt_sha256"],
    )
    if usage.exists():
        compare_hash("generation_usage", usage, hashes["generation_usage_sha256"])

    candidate_prompt = Path("/candidate/prompt.py")
    candidate_translator = Path("/candidate/py2mpy.py")
    compare_hash("candidate_prompt", candidate_prompt, hashes["candidate_prompt_sha256"])
    compare_hash(
        "candidate_translator",
        candidate_translator,
        hashes["candidate_translator_sha256"],
    )
    assert candidate_prompt.read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert candidate_translator.read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("candidate prompt byte-equals trusted prompt: MATCH")
    print("candidate translator byte-equals trusted translator: MATCH")

    task_manifest = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    embedded_manifest = dict(audit_input["manifest"])
    embedded_config = embedded_manifest.pop("config")
    assert task_manifest == embedded_manifest
    assert embedded_config == audit_input["config"]
    print(
        "task manifest equals audit_input.manifest after removing the "
        "launcher-added config field: MATCH"
    )
    assert hashes["manifest_sha256"] == hashes["task_manifest_sha256"]
    print("manifest hash equals task-manifest hash: MATCH")

    evidence_outputs = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )["outputs"]["evidence"]
    for relative, expected in sorted(evidence_outputs.items()):
        compare_hash(
            f"generation-result evidence {relative}",
            Path("/generation-evidence") / relative,
            expected,
        )

    generation_result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    candidate_pipeline_digest = pipeline_tree_digest(Path("/candidate"))
    candidate_expected = generation_result["outputs"]["workspace_sha256"]
    assert candidate_pipeline_digest == candidate_expected
    assert candidate_pipeline_digest == invocation["retained_workspace_sha256"]
    print(
        "PIPELINE TREE candidate: MATCH "
        f"expected={candidate_expected} actual={candidate_pipeline_digest}"
    )

    trace_pipeline_digest = pipeline_tree_digest(
        Path("/generation-evidence/codex-trace")
    )
    if usage.exists():
        usage_record = json.loads(usage.read_text(encoding="utf-8"))
        assert trace_pipeline_digest == usage_record["source_trace_sha256"]
        print(
            "PIPELINE TREE structured trace: MATCH "
            f"expected={usage_record['source_trace_sha256']} "
            f"actual={trace_pipeline_digest}"
        )

    candidate_records = inspect_tree(Path("/candidate"))
    print("CANDIDATE TREE INVENTORY")
    for relative, entry_type, mode, digest in candidate_records:
        print(f"{entry_type} mode={mode:04o} sha256={digest} path={relative}")
    print(f"candidate entries={len(candidate_records)}")

    trace_records = inspect_tree(Path("/generation-evidence/codex-trace"))
    print("TRACE TREE INVENTORY")
    for relative, entry_type, mode, digest in trace_records:
        print(f"{entry_type} mode={mode:04o} sha256={digest} path={relative}")
    print(f"trace entries={len(trace_records)}")

    trace_files = [
        Path("/generation-evidence/codex-trace") / relative
        for relative, entry_type, _mode, _digest in trace_records
        if entry_type == "file"
    ]
    trace_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    total_trace_lines = 0
    for trace_file in trace_files:
        with trace_file.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_trace_lines += 1
                event = json.loads(line)
                trace_counts[str(event.get("type", "<missing>"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_counts[str(payload.get("type", "<missing>"))] += 1
    print(f"structured trace JSONL parse: OK files={len(trace_files)} lines={total_trace_lines}")
    print(f"trace top-level types={dict(sorted(trace_counts.items()))}")
    print(f"trace payload types={dict(sorted(payload_counts.items()))}")

    for log_path in (
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/prompt.txt"),
    ):
        raw = log_path.read_bytes()
        print(
            f"FULL READ path={log_path} bytes={len(raw)} lines={raw.count(bytes([10]))} "
            f"nul_bytes={raw.count(bytes([0]))} sha256={hashlib.sha256(raw).hexdigest()}"
        )

    print("STAGE1_INTEGRITY_RESULT=PASS")


if __name__ == "__main__":
    main()
