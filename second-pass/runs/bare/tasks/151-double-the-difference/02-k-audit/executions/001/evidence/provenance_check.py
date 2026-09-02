#!/usr/bin/env python3
"""Independent structural and cryptographic checks of the mounted audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the pipeline-v3 sha256_tree encoding independently."""
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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
                raise AssertionError(f"linked or unsupported entry: {path}")
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
        raise AssertionError(f"required record is not a regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"required mount is not a real directory: {path}")


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    status_text = "MATCH" if actual == expected else "MISMATCH"
    print(f"{label}: {status_text}")
    print(f"  expected={expected}")
    print(f"  actual  ={actual}")
    if actual != expected:
        raise AssertionError(f"hash mismatch for {label}")


def load_json(path: Path) -> object:
    require_regular(path)
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def main() -> int:
    audit = load_json(AUDIT_INPUT)
    assert isinstance(audit, dict)
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["problem_id"] == "151-double-the-difference"

    container_paths = audit["container_paths"]
    required_files = [
        AUDIT_INPUT,
        LOCK,
        Path(container_paths["run_manifest"]),
        Path(container_paths["task_manifest"]),
        Path(container_paths["stage1_result"]),
        Path(container_paths["generation_manifest"]),
        Path(container_paths["generation_metrics"]),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path(container_paths["generation_last"]),
        Path(container_paths["generation_output"]),
        Path("/generation-evidence/prompt.txt"),
        Path(container_paths["canonical"]),
        Path(container_paths["translator"]),
        Path(container_paths["trusted_prompt"]),
    ]
    for path in required_files:
        require_regular(path)
    for path in (
        Path(container_paths["candidate"]),
        Path(container_paths["generation_root"]),
        Path(container_paths["generation_trace"]),
        Path("/reference"),
    ):
        require_directory(path)
    print(f"required_regular_files={len(required_files)}")
    print("required_directories=4")

    lock = load_json(LOCK)
    assert lock == audit["audit_campaign"]
    check_hash(
        "audit campaign lock",
        LOCK,
        audit["hashes"]["audit_campaign_lock_sha256"],
    )
    print("campaign_block_equals_lock=true")

    hash_checks = {
        "candidate prompt": (
            Path("/candidate/prompt.py"),
            audit["hashes"]["candidate_prompt_sha256"],
        ),
        "candidate translator": (
            Path("/candidate/py2mpy.py"),
            audit["hashes"]["candidate_translator_sha256"],
        ),
        "trusted prompt": (
            Path("/reference/prompt.py"),
            audit["hashes"]["trusted_prompt_sha256"],
        ),
        "trusted translator": (
            Path("/reference/py2mpy.py"),
            audit["hashes"]["trusted_translator_sha256"],
        ),
        "canonical": (
            Path("/reference/canonical.py"),
            audit["hashes"]["canonical_sha256"],
        ),
        "run manifest": (
            Path("/run.json"),
            audit["hashes"]["run_manifest_sha256"],
        ),
        "task manifest": (
            Path("/task.json"),
            audit["hashes"]["task_manifest_sha256"],
        ),
        "stage1 result": (
            Path("/generation-result.json"),
            audit["hashes"]["stage1_result_sha256"],
        ),
        "stage1 invocation": (
            Path("/generation-evidence/invocation.json"),
            audit["hashes"]["stage1_invocation_sha256"],
        ),
        "generation metrics": (
            Path("/generation-evidence/metrics.json"),
            audit["hashes"]["generation_metrics_sha256"],
        ),
        "generation runtime metrics": (
            Path("/generation-evidence/runtime-metrics.json"),
            audit["hashes"]["generation_runtime_metrics_sha256"],
        ),
        "generation usage": (
            Path("/generation-evidence/usage.json"),
            audit["hashes"]["generation_usage_sha256"],
        ),
        "generation last": (
            Path("/generation-evidence/codex-last.txt"),
            audit["hashes"]["generation_codex_last_sha256"],
        ),
        "generation output": (
            Path("/generation-evidence/codex-output.log"),
            audit["hashes"]["generation_codex_output_sha256"],
        ),
        "generation prompt": (
            Path("/generation-evidence/prompt.txt"),
            audit["hashes"]["generation_prompt_sha256"],
        ),
    }
    for label, (path, expected) in hash_checks.items():
        check_hash(label, path, expected)

    if Path("/reference/reference-semantics").exists() or Path(
        "/reference/reference-semantics"
    ).is_symlink():
        raise AssertionError("forbidden reference semantics mount exists")
    print("reference_semantics_absent=true")

    assert (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    assert (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print("candidate_prompt_byte_identical_to_trusted=true")
    print("candidate_translator_byte_identical_to_trusted=true")

    for root in (
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/reference"),
    ):
        for entry in root.rglob("*"):
            mode = entry.lstat().st_mode
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                raise AssertionError(f"linked or unsupported mounted entry: {entry}")
    print("mounted_tree_symlink_or_special_entries=0")

    result = load_json(Path("/generation-result.json"))
    invocation = load_json(Path("/generation-evidence/invocation.json"))
    task = load_json(Path("/task.json"))
    run = load_json(Path("/run.json"))
    usage = load_json(Path("/generation-evidence/usage.json"))
    assert isinstance(result, dict)
    assert isinstance(invocation, dict)
    assert isinstance(task, dict)
    assert isinstance(run, dict)
    assert isinstance(usage, dict)
    normalized_task = dict(task)
    normalized_task["config"] = audit["config"]
    assert normalized_task == audit["manifest"]
    assert task["problem_id"] == audit["problem_id"]
    assert run["run_id"] == audit["run_id"]
    assert run["condition"] == task["condition"] == audit["manifest"]["condition"]
    assert result["session_id"] == invocation["session_id"]
    assert result["outputs"] == invocation["outputs"]
    print("manifest_cross_consistency=true")

    for relative, expected in result["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        check_hash(f"result evidence {relative}", path, expected)

    candidate_digest = pipeline_tree_digest(Path("/candidate"))
    trace_digest = pipeline_tree_digest(Path("/generation-evidence/codex-trace"))
    print(f"candidate_pipeline_tree_digest={candidate_digest}")
    print(
        "candidate_matches_generation_workspace="
        f"{candidate_digest == result['outputs']['workspace_sha256']}"
    )
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    print(f"trace_pipeline_tree_digest={trace_digest}")
    print(
        "trace_matches_usage_source="
        f"{trace_digest == usage['source_trace_sha256']}"
    )
    assert trace_digest == usage["source_trace_sha256"]
    print(
        "launcher_candidate_tree_record="
        f"{audit['hashes']['candidate_tree_sha256']}"
    )
    print(
        "launcher_generation_trace_record="
        f"{audit['hashes']['generation_codex_trace_sha256']}"
    )

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert trace_files
    outer_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    total_records = 0
    final_messages = 0
    for trace_file in trace_files:
        require_regular(trace_file)
        with trace_file.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                total_records += 1
                outer_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    if (
                        payload.get("type") == "agent_message"
                        and payload.get("phase") == "final_answer"
                    ):
                        final_messages += 1
    selected_path = (
        Path("/generation-evidence/codex-trace")
        / usage["selected_event"]["relative_path"]
    )
    selected_line_number = usage["selected_event"]["line_number"]
    with selected_path.open(encoding="utf-8") as stream:
        selected_line = next(
            line
            for number, line in enumerate(stream, 1)
            if number == selected_line_number
        )
    selected_record = json.loads(selected_line)
    assert selected_record["payload"]["type"] == "token_count"
    print(f"trace_files={len(trace_files)}")
    print(f"trace_records={total_records}")
    print(f"trace_outer_types={dict(sorted(outer_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_final_agent_messages={final_messages}")
    print("usage_selected_trace_record_is_token_count=true")

    output_text = Path("/generation-evidence/codex-output.log").read_text(
        encoding="utf-8"
    )
    print(f"codex_output_lines={len(output_text.splitlines())}")
    print(f"codex_output_top_mentions={output_text.count('#Top')}")
    print(
        "codex_output_result_marker_mentions="
        f"{output_text.count('RESULT: KPROVE_PASSED')}"
    )
    print("PROVENANCE_CHECK=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"PROVENANCE_CHECK=FAIL: {type(error).__name__}: {error}")
        raise
