#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit records."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement /opt/humaneval/tools/pipeline_contract.py:sha256_tree."""
    if not stat.S_ISDIR(root.lstat().st_mode):
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
                raise AssertionError(f"linked/unsupported tree entry: {path}")
    hasher = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        hasher.update(len(encoded).to_bytes(4, "big"))
        hasher.update(encoded)
        hasher.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            hasher.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    hasher.update(chunk)
    return hasher.hexdigest()


def require_regular(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise AssertionError(f"required record is not a real regular file: {path}")


def compare_trees(left: Path, right: Path) -> tuple[int, str]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", digest(path))
            else:
                result[relative] = ("unsupported", None)
        return result

    left_inventory = inventory(left)
    right_inventory = inventory(right)
    if left_inventory != right_inventory:
        left_only = sorted(set(left_inventory) - set(right_inventory))
        right_only = sorted(set(right_inventory) - set(left_inventory))
        changed = sorted(
            path
            for path in set(left_inventory) & set(right_inventory)
            if left_inventory[path] != right_inventory[path]
        )
        return 1, f"left_only={left_only}; right_only={right_only}; changed={changed}"
    return 0, f"{len(left_inventory)} entries identical"


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text())
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    require_regular(lock_path)
    lock = json.loads(lock_path.read_text())
    assert lock == audit["audit_campaign"]
    assert digest(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_lock_sha256={digest(lock_path)} match=true")
    print("campaign_block_match=true")

    paths = audit["container_paths"]
    required_records = [
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path(paths["generation_root"]) / "prompt.txt",
        Path(paths["generation_root"]) / "codex-trace",
    ]
    for path in required_records:
        mode = path.lstat().st_mode
        if path.name == "codex-trace":
            assert stat.S_ISDIR(mode)
        else:
            assert stat.S_ISREG(mode)
        print(f"required_record_ok={path}")
    print("runtime_metrics_required=false (legacy-selected-stage1)")

    file_hash_checks = {
        Path(paths["run_manifest"]): "run_manifest_sha256",
        Path(paths["task_manifest"]): "task_manifest_sha256",
        Path(paths["stage1_result"]): "stage1_result_sha256",
        Path(paths["generation_manifest"]): "stage1_invocation_sha256",
        Path(paths["generation_metrics"]): "generation_metrics_sha256",
        Path(paths["generation_last"]): "generation_codex_last_sha256",
        Path(paths["generation_output"]): "generation_codex_output_sha256",
        Path(paths["generation_root"]) / "prompt.txt": "generation_prompt_sha256",
        Path(paths["generation_root"]) / "usage.json": "generation_usage_sha256",
        Path(paths["canonical"]): "canonical_sha256",
        Path(paths["trusted_prompt"]): "trusted_prompt_sha256",
        Path(paths["translator"]): "trusted_translator_sha256",
    }
    for path, key in file_hash_checks.items():
        require_regular(path)
        actual = digest(path)
        expected = audit["hashes"][key]
        assert actual == expected, (path, actual, expected)
        print(f"sha256_match {path} {actual}")

    task = json.loads(Path(paths["task_manifest"]).read_text())
    run = json.loads(Path(paths["run_manifest"]).read_text())
    result = json.loads(Path(paths["stage1_result"]).read_text())
    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    embedded_task = dict(audit["manifest"])
    embedded_config = embedded_task.pop("config")
    assert task == embedded_task
    assert embedded_config == audit["config"]
    assert run["run_id"] == audit["run_id"]
    assert result["status"] == "SUCCEEDED"
    assert invocation["status"] == "SUCCEEDED"
    print("embedded_task_manifest_match=true")
    print("run_and_stage_identity_match=true")

    candidate = Path(paths["candidate"])
    trusted_prompt = Path(paths["trusted_prompt"])
    trusted_translator = Path(paths["translator"])
    assert digest(candidate / "prompt.py") == digest(trusted_prompt)
    assert digest(candidate / "py2mpy.py") == digest(trusted_translator)
    print("candidate_prompt_match=true")
    print("candidate_translator_match=true")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    assert trusted_semantics.is_dir()
    comparison_status, comparison_detail = compare_trees(
        trusted_semantics, candidate_semantics
    )
    assert comparison_status == 0, comparison_detail
    print(f"supplied_semantics_recursive_match=true ({comparison_detail})")
    trusted_tree_hash = pipeline_tree_digest(trusted_semantics)
    candidate_semantics_hash = pipeline_tree_digest(candidate_semantics)
    assert trusted_tree_hash == candidate_semantics_hash
    assert (
        trusted_tree_hash
        == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    )
    print(f"supplied_semantics_pipeline_tree_sha256={trusted_tree_hash}")

    candidate_tree_hash = pipeline_tree_digest(candidate)
    assert candidate_tree_hash == invocation["retained_workspace_sha256"]
    assert candidate_tree_hash == result["outputs"]["workspace_sha256"]
    print(f"candidate_pipeline_tree_sha256={candidate_tree_hash}")
    print(
        "launcher_candidate_tree_sha256="
        f"{audit['hashes']['candidate_tree_sha256']} "
        "(different launcher digest scheme; recursive content checked above)"
    )

    generation_root = Path(paths["generation_root"])
    for relative, expected in result["outputs"]["evidence"].items():
        path = generation_root / relative
        require_regular(path)
        actual = digest(path)
        assert actual == expected, (relative, actual, expected)
        print(f"stage1_output_hash_match {relative} {actual}")

    trace_root = Path(paths["generation_trace"])
    trace_hash = pipeline_tree_digest(trace_root)
    usage = json.loads((generation_root / "usage.json").read_text())
    assert trace_hash == usage["source_trace_sha256"]
    print(f"trace_pipeline_tree_sha256={trace_hash}")

    trace_files = sorted(trace_root.rglob("*.jsonl"))
    line_count = 0
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    for trace_file in trace_files:
        with trace_file.open() as stream:
            for line_count_in_file, line in enumerate(stream, 1):
                record = json.loads(line)
                top_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict) and "type" in payload:
                    payload_types[str(payload["type"])] += 1
            line_count += line_count_in_file
    print(f"trace_files_read={len(trace_files)} trace_json_records_read={line_count}")
    print(f"trace_top_types={dict(sorted(top_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")

    output_log = Path(paths["generation_output"])
    output_bytes = output_log.read_bytes()
    print(
        "codex_output_full_read="
        f"{len(output_bytes)} bytes kprove_mentions={output_bytes.count(b'kprove')} "
        f"top_mentions={output_bytes.count(b'#Top')}"
    )
    print("PROVENANCE_CHECK=PASS")


if __name__ == "__main__":
    main()
