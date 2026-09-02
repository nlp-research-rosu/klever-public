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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Launcher pipeline_contract.sha256_tree algorithm, independently restated."""
    digest = hashlib.sha256()
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
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    assert os.access(path, os.R_OK), f"not readable: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    assert os.access(path, os.R_OK | os.X_OK), f"not readable/searchable: {path}"


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    print(f"{label}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["mount_reference_semantics"] is False
    assert not Path("/reference/reference-semantics").exists()

    lock_match = lock == audit["audit_campaign"]
    print(f"campaign_lock_exact_object_match={lock_match}")
    assert lock_match
    check_hash(
        "audit_campaign_lock",
        LOCK,
        audit["hashes"]["audit_campaign_lock_sha256"],
    )

    paths = audit["container_paths"]
    regular_keys = (
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
    )
    directory_keys = ("candidate", "generation_root", "generation_trace")
    for key in regular_keys:
        require_regular(Path(paths[key]))
        print(f"container_path {key}: regular readable {paths[key]}")
    for key in directory_keys:
        require_directory(Path(paths[key]))
        print(f"container_path {key}: real directory {paths[key]}")

    layout_required = (
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    )
    for path in layout_required:
        require_regular(path)
        print(f"layout_required: regular readable {path}")
    require_directory(Path("/generation-evidence/codex-trace"))
    usage = Path("/generation-evidence/usage.json")
    require_regular(usage)
    print(f"optional_present: regular readable {usage}")
    runtime_metrics = Path("/generation-evidence/runtime-metrics.json")
    print(
        "historical_runtime_metrics_present="
        f"{runtime_metrics.exists()} (not required for legacy-selected-stage1)"
    )

    hashes = audit["hashes"]
    checks = {
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
    }
    for label, path in checks.items():
        check_hash(label, path, hashes[label])

    prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print(f"candidate_prompt_byte_equal_trusted={prompt_equal}")
    print(f"candidate_translator_byte_equal_trusted={translator_equal}")
    assert prompt_equal and translator_equal

    task = json.loads(Path("/task.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    usage_doc = json.loads(usage.read_text())
    embedded_manifest = audit["manifest"]
    task_with_config = dict(task)
    task_with_config["config"] = audit["config"]
    assert task_with_config == embedded_manifest
    assert task["inputs"]["problem_prompt_sha256"] == hashes["trusted_prompt_sha256"]
    assert task["inputs"]["translator_sha256"] == hashes["trusted_translator_sha256"]
    assert (
        task["inputs"]["instruction_prompt_sha256"]
        == hashes["generation_prompt_sha256"]
    )
    print(
        "task_manifest_matches_embedded_after_launcher_config_annotation=True"
    )
    print(
        "invocation_identity="
        f"{invocation['name']} status={invocation['status']} "
        f"exit_code={invocation['exit_code']}"
    )
    print(
        "generation_result="
        f"status={result['status']} marker={result['result_marker']}"
    )

    for relative, expected in result["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        require_regular(path)
        check_hash(f"generation_result evidence {relative}", path, expected)

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    assert trace_files
    event_types: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        require_regular(path)
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            record = json.loads(line)
            assert isinstance(record, dict)
            assert "timestamp" in record and "type" in record and "payload" in record
            event_types[record["type"]] += 1
            trace_lines += 1
    print(f"structured_trace_files={len(trace_files)} valid_jsonl_lines={trace_lines}")
    print(f"structured_trace_event_types={dict(sorted(event_types.items()))}")
    trace_tree = sha256_tree(trace_root)
    print(
        "structured_trace_pipeline_tree_sha256="
        f"{trace_tree} usage_source_trace_match="
        f"{trace_tree == usage_doc['source_trace_sha256']}"
    )
    assert trace_tree == usage_doc["source_trace_sha256"]

    candidate_tree = sha256_tree(Path("/candidate"))
    print(f"candidate_pipeline_tree_sha256={candidate_tree}")
    print(
        "candidate_generation_result_workspace_match="
        f"{candidate_tree == result['outputs']['workspace_sha256']}"
    )
    assert candidate_tree == result["outputs"]["workspace_sha256"]

    for root in (
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ):
        unsupported = []
        for path in root.rglob("*"):
            mode = path.lstat().st_mode
            if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                unsupported.append(str(path))
        print(f"unsupported_or_linked_entries {root}: {unsupported}")
        assert not unsupported

    print("PROVENANCE_CHECK=PASS")


if __name__ == "__main__":
    main()
