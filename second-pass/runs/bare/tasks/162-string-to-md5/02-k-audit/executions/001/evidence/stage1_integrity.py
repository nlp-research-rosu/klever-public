#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the content-tree digest used by pipeline-v3 records."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
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


def require_file(path: Path, errors: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        errors.append(f"missing/unreadable required file {path}: {error}")
        return
    if not stat.S_ISREG(mode):
        errors.append(f"required file is not a real regular file: {path}")


def require_dir(path: Path, errors: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        errors.append(f"missing/unreadable required directory {path}: {error}")
        return
    if not stat.S_ISDIR(mode):
        errors.append(f"required directory is not a real directory: {path}")


def check_hash(
    label: str, path: Path, expected: str | None, errors: list[str]
) -> str:
    actual = sha256_file(path)
    status = "MATCH" if expected == actual else "MISMATCH"
    print(f"{label}: {status} expected={expected} actual={actual} path={path}")
    if expected != actual:
        errors.append(f"{label} hash mismatch")
    return actual


def main() -> int:
    errors: list[str] = []
    audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    paths = {key: Path(value) for key, value in audit_input["container_paths"].items()}
    hashes = audit_input["hashes"]

    print(
        "declared:",
        f"layout={audit_input['record_layout']}",
        f"problem={audit_input['problem_id']}",
        f"condition={audit_input['condition']}",
        f"semantics_mode={audit_input['semantics_mode']}",
    )
    if audit_input["record_layout"] != "pipeline-v3":
        errors.append("record layout is not pipeline-v3")
    if audit_input["semantics_mode"] != "GENERATED_SEMANTICS":
        errors.append("semantics mode is not GENERATED_SEMANTICS")

    required_files = [
        AUDIT_INPUT,
        paths["audit_campaign_lock"],
        paths["run_manifest"],
        paths["task_manifest"],
        paths["stage1_result"],
        paths["canonical"],
        paths["trusted_prompt"],
        paths["translator"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        paths["generation_last"],
        paths["generation_output"],
        Path("/generation-evidence/prompt.txt"),
    ]
    required_dirs = [
        paths["candidate"],
        paths["generation_root"],
        paths["generation_trace"],
    ]
    for path in required_files:
        require_file(path, errors)
    for path in required_dirs:
        require_dir(path, errors)

    if Path("/reference/reference-semantics").exists() or Path(
        "/reference/reference-semantics"
    ).is_symlink():
        errors.append(
            "reference semantics unexpectedly exists in GENERATED_SEMANTICS mode"
        )
    else:
        print("generated-semantics boundary: no /reference/reference-semantics (OK)")

    campaign = json.loads(paths["audit_campaign_lock"].read_text(encoding="utf-8"))
    print(
        "campaign content equality:",
        "MATCH" if campaign == audit_input["audit_campaign"] else "MISMATCH",
    )
    if campaign != audit_input["audit_campaign"]:
        errors.append("campaign lock content differs from audit_input.audit_campaign")
    check_hash(
        "campaign lock",
        paths["audit_campaign_lock"],
        hashes["audit_campaign_lock_sha256"],
        errors,
    )

    checks = [
        ("run manifest", paths["run_manifest"], hashes["run_manifest_sha256"]),
        ("task manifest", paths["task_manifest"], hashes["task_manifest_sha256"]),
        ("stage1 result", paths["stage1_result"], hashes["stage1_result_sha256"]),
        (
            "generation invocation",
            paths["generation_manifest"],
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation metrics",
            paths["generation_metrics"],
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation runtime metrics",
            Path("/generation-evidence/runtime-metrics.json"),
            hashes["generation_runtime_metrics_sha256"],
        ),
        (
            "generation usage",
            Path("/generation-evidence/usage.json"),
            hashes["generation_usage_sha256"],
        ),
        (
            "generation codex-last",
            paths["generation_last"],
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation codex-output",
            paths["generation_output"],
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation prompt",
            Path("/generation-evidence/prompt.txt"),
            hashes["generation_prompt_sha256"],
        ),
        ("canonical", paths["canonical"], hashes["canonical_sha256"]),
        ("trusted prompt", paths["trusted_prompt"], hashes["trusted_prompt_sha256"]),
        ("trusted translator", paths["translator"], hashes["trusted_translator_sha256"]),
        (
            "candidate prompt",
            paths["candidate"] / "prompt.py",
            hashes["candidate_prompt_sha256"],
        ),
        (
            "candidate translator",
            paths["candidate"] / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
    ]
    for label, path, expected in checks:
        check_hash(label, path, expected, errors)

    task = json.loads(paths["task_manifest"].read_text(encoding="utf-8"))
    audit_manifest = audit_input["manifest"]
    differing_common_keys = [
        key
        for key in task
        if key not in audit_manifest or task[key] != audit_manifest[key]
    ]
    if differing_common_keys:
        errors.append(
            "task manifest differs from audit_input.manifest on common fields: "
            + ", ".join(differing_common_keys)
        )
        print("task/audit-input common manifest fields: MISMATCH")
    else:
        print("task/audit-input common manifest fields: MATCH")
    extra_audit_fields = {
        key: value for key, value in audit_manifest.items() if key not in task
    }
    print("audit-input derived manifest-only fields:", extra_audit_fields)
    if extra_audit_fields != {"config": audit_input["manifest_config"]}:
        errors.append("unexpected audit-input manifest-only fields")

    result = json.loads(paths["stage1_result"].read_text(encoding="utf-8"))
    invocation = json.loads(paths["generation_manifest"].read_text(encoding="utf-8"))
    for record_name, record in (("stage1 result", result), ("invocation", invocation)):
        evidence = record["outputs"]["evidence"]
        for relative, expected in sorted(evidence.items()):
            check_hash(
                f"{record_name} evidence {relative}",
                paths["generation_root"] / relative,
                expected,
                errors,
            )

    candidate_digest = pipeline_tree_digest(paths["candidate"])
    result_digest = result["outputs"]["workspace_sha256"]
    invocation_digest = invocation["outputs"]["workspace_sha256"]
    print(
        "candidate pipeline content-tree:",
        f"actual={candidate_digest}",
        f"result={result_digest}",
        f"invocation={invocation_digest}",
        "MATCH"
        if candidate_digest == result_digest == invocation_digest
        else "MISMATCH",
    )
    if candidate_digest != result_digest or candidate_digest != invocation_digest:
        errors.append("candidate content-tree differs from pipeline-v3 output digest")
    print(
        "audit-input launcher candidate tree hash (separately recorded):",
        hashes["candidate_tree_sha256"],
    )

    trace_digest = pipeline_tree_digest(paths["generation_trace"])
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    usage_digest = usage["source_trace_sha256"]
    print(
        "trace pipeline content-tree:",
        f"actual={trace_digest}",
        f"usage={usage_digest}",
        "MATCH" if trace_digest == usage_digest else "MISMATCH",
    )
    if trace_digest != usage_digest:
        errors.append("trace content-tree differs from usage source digest")
    print(
        "audit-input launcher trace tree hash (separately recorded):",
        hashes["generation_codex_trace_sha256"],
    )

    type_counts: Counter[str] = Counter()
    payload_type_counts: Counter[str] = Counter()
    trace_lines = 0
    trace_files = sorted(paths["generation_trace"].rglob("*.jsonl"))
    if not trace_files:
        errors.append("structured trace has no jsonl files")
    for trace_file in trace_files:
        with trace_file.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    event = json.loads(line)
                except ValueError as error:
                    errors.append(
                        f"malformed trace JSON {trace_file}:{line_number}: {error}"
                    )
                    continue
                type_counts[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_type_counts[str(payload.get("type"))] += 1
    print(f"structured trace: files={len(trace_files)} lines={trace_lines}")
    print("trace top-level type counts:", dict(sorted(type_counts.items())))
    print("trace payload type counts:", dict(sorted(payload_type_counts.items())))

    print(f"integrity errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
