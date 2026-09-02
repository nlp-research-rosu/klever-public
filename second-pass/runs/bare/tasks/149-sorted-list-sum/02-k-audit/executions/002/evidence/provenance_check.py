#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs.

This script only reads the immutable mounts.  It deliberately reports both
per-file SHA-256 values and the pipeline's length-delimited tree digest so the
evidence does not depend on host provenance paths.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """The length-delimited tree algorithm used by pipeline_contract.py."""
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError(f"tree root is not a real directory: {root}")
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"not a real regular file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def check_hash(label: str, path: Path, expected: str | None) -> None:
    require_regular(path)
    actual = sha256_file(path)
    status = "MATCH" if actual == expected else "MISMATCH"
    print(f"FILE {label}: {status} actual={actual} expected={expected} path={path}")
    if actual != expected:
        raise RuntimeError(f"hash mismatch for {label}")


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    hashes = audit["hashes"]

    print(f"record_layout={audit['record_layout']}")
    print(f"problem_id={audit['problem_id']}")
    print(f"condition={audit['condition']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"input_provenance={audit['manifest']['input_provenance']}")
    print(f"campaign_block_equals_lock={audit['audit_campaign'] == lock}")
    if audit["audit_campaign"] != lock:
        raise RuntimeError("campaign lock differs from embedded campaign block")

    required = {
        "audit-input": AUDIT,
        "campaign-lock": LOCK,
        "run-manifest": paths["run_manifest"],
        "task-manifest": paths["task_manifest"],
        "stage1-result": paths["stage1_result"],
        "generation-invocation": paths["generation_manifest"],
        "generation-metrics": paths["generation_metrics"],
        "generation-last": paths["generation_last"],
        "generation-output": paths["generation_output"],
        "generation-prompt": paths["generation_root"] / "prompt.txt",
        "generation-usage": paths["generation_root"] / "usage.json",
        "canonical": paths["canonical"],
        "trusted-prompt": paths["trusted_prompt"],
        "trusted-translator": paths["translator"],
    }
    for label, path in required.items():
        require_regular(path)
        print(f"REQUIRED {label}: REGULAR_READABLE {path}")

    expected_hashes = {
        "campaign-lock": hashes["audit_campaign_lock_sha256"],
        "run-manifest": hashes["run_manifest_sha256"],
        "task-manifest": hashes["task_manifest_sha256"],
        "stage1-result": hashes["stage1_result_sha256"],
        "generation-invocation": hashes["stage1_invocation_sha256"],
        "generation-metrics": hashes["generation_metrics_sha256"],
        "generation-last": hashes["generation_codex_last_sha256"],
        "generation-output": hashes["generation_codex_output_sha256"],
        "generation-prompt": hashes["generation_prompt_sha256"],
        "generation-usage": hashes["generation_usage_sha256"],
        "canonical": hashes["canonical_sha256"],
        "trusted-prompt": hashes["trusted_prompt_sha256"],
        "trusted-translator": hashes["trusted_translator_sha256"],
    }
    for label, expected in expected_hashes.items():
        check_hash(label, required[label], expected)

    candidate = paths["candidate"]
    if candidate.is_symlink() or not candidate.is_dir():
        raise RuntimeError("candidate mount is not a real directory")
    for path in sorted(candidate.rglob("*")):
        mode = path.lstat().st_mode
        if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            raise RuntimeError(f"candidate has linked/unsupported entry: {path}")

    candidate_prompt = candidate / "prompt.py"
    candidate_translator = candidate / "py2mpy.py"
    check_hash("candidate-prompt", candidate_prompt, hashes["candidate_prompt_sha256"])
    check_hash(
        "candidate-translator",
        candidate_translator,
        hashes["candidate_translator_sha256"],
    )
    print(
        "candidate_prompt_byte_equal_trusted="
        f"{candidate_prompt.read_bytes() == paths['trusted_prompt'].read_bytes()}"
    )
    print(
        "candidate_translator_byte_equal_trusted="
        f"{candidate_translator.read_bytes() == paths['translator'].read_bytes()}"
    )

    reference_semantics = Path("/reference/reference-semantics")
    print(
        "generated_mode_reference_semantics_absent="
        f"{not os.path.lexists(reference_semantics)}"
    )
    if os.path.lexists(reference_semantics):
        raise RuntimeError("reference semantics is present in GENERATED_SEMANTICS mode")

    result = json.loads(paths["stage1_result"].read_text(encoding="utf-8"))
    invocation = json.loads(paths["generation_manifest"].read_text(encoding="utf-8"))
    usage = json.loads(required["generation-usage"].read_text(encoding="utf-8"))
    task = json.loads(paths["task_manifest"].read_text(encoding="utf-8"))
    run = json.loads(paths["run_manifest"].read_text(encoding="utf-8"))
    print(f"task_problem_matches={task['problem_id'] == audit['problem_id']}")
    print(f"task_condition_matches={task['condition'] == run['condition'] == audit['manifest']['condition']}")
    print(f"result_invocation={result['invocation']} status={result['status']}")
    print(f"invocation_name={invocation['name']} status={invocation['status']}")

    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = paths["generation_root"] / relative
        check_hash(f"stage1-evidence:{relative}", path, expected)

    trace_root = paths["generation_trace"]
    if trace_root.is_symlink() or not trace_root.is_dir():
        raise RuntimeError("trace mount is not a real directory")
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    trace_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    parsed_records = 0
    for trace_file in trace_files:
        require_regular(trace_file)
        with trace_file.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                parsed_records += 1
                trace_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
    print(f"trace_files={len(trace_files)} parsed_json_records={parsed_records}")
    print(f"trace_record_types={dict(sorted(trace_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    trace_digest = sha256_tree(trace_root)
    print(f"trace_pipeline_tree_sha256={trace_digest}")
    print(f"trace_usage_source_sha256={usage['source_trace_sha256']}")
    print(f"trace_usage_digest_matches={trace_digest == usage['source_trace_sha256']}")

    candidate_digest = sha256_tree(candidate)
    print(f"candidate_pipeline_tree_sha256={candidate_digest}")
    print(f"stage1_workspace_sha256={result['outputs']['workspace_sha256']}")
    print(
        "candidate_stage1_workspace_matches="
        f"{candidate_digest == result['outputs']['workspace_sha256']}"
    )
    print(
        "launcher_additional_candidate_tree_sha256="
        f"{hashes['candidate_tree_sha256']}"
    )
    print(
        "launcher_additional_trace_tree_sha256="
        f"{hashes['generation_codex_trace_sha256']}"
    )
    print("PROVENANCE_CHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
