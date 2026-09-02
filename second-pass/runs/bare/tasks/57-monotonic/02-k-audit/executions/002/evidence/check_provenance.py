#!/usr/bin/env python3
"""Independent checks over launcher-mounted provenance records.

This script intentionally treats every generation record as data.  It checks
mount presence/type, direct SHA-256 declarations, the campaign lock, and the
condition-aware semantics boundary without importing candidate code.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_file(label: str, path: Path, expected: str | None = None) -> bool:
    regular = path.is_file() and not path.is_symlink()
    readable = os.access(path, os.R_OK)
    actual = sha256(path) if regular and readable else None
    ok = regular and readable and (expected is None or actual == expected)
    print(
        f"{label}: path={path} regular={regular} readable={readable} "
        f"sha256={actual} expected={expected} ok={ok}"
    )
    return ok


def pipeline_sha256_tree(root: Path) -> str:
    """Recompute the mounted pipeline tree digest from names, kinds, sizes, and bytes."""
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text())
    hashes = data["hashes"]
    paths = {key: Path(value) for key, value in data["container_paths"].items()}
    overall = True

    lock_path = paths["audit_campaign_lock"]
    overall &= check_file(
        "audit_campaign_lock",
        lock_path,
        hashes["audit_campaign_lock_sha256"],
    )
    lock = json.loads(lock_path.read_text())
    lock_equal = lock == data["audit_campaign"]
    print(f"campaign_lock_exact_object_match={lock_equal}")
    overall &= lock_equal

    print(
        "declared_identity="
        f"problem_id:{data['problem_id']} "
        f"condition:{data['condition']} "
        f"record_layout:{data['record_layout']} "
        f"semantics_mode:{data['semantics_mode']}"
    )
    identity_ok = (
        data["problem_id"] == "57-monotonic"
        and data["condition"] == "bare"
        and data["record_layout"] == "legacy-selected-stage1"
        and data["semantics_mode"] == "GENERATED_SEMANTICS"
    )
    print(f"declared_identity_ok={identity_ok}")
    overall &= identity_ok

    declared_mount_types = {
        "audit_campaign_lock": "file",
        "candidate": "dir",
        "canonical": "file",
        "generation_last": "file",
        "generation_manifest": "file",
        "generation_metrics": "file",
        "generation_output": "file",
        "generation_root": "dir",
        "generation_trace": "dir",
        "run_manifest": "file",
        "stage1_result": "file",
        "task_manifest": "file",
        "translator": "file",
        "trusted_prompt": "file",
    }
    for key, expected_type in declared_mount_types.items():
        path = paths[key]
        actual_type_ok = (
            path.is_dir() if expected_type == "dir" else path.is_file()
        ) and not path.is_symlink()
        readable = os.access(path, os.R_OK)
        ok = actual_type_ok and readable
        print(
            f"mount:{key}: path={path} expected_type={expected_type} "
            f"not_symlink={not path.is_symlink()} readable={readable} ok={ok}"
        )
        overall &= ok

    direct_hash_checks = [
        ("canonical", paths["canonical"], hashes["canonical_sha256"]),
        ("trusted_prompt", paths["trusted_prompt"], hashes["trusted_prompt_sha256"]),
        ("translator", paths["translator"], hashes["trusted_translator_sha256"]),
        ("run_manifest", paths["run_manifest"], hashes["run_manifest_sha256"]),
        ("task_manifest", paths["task_manifest"], hashes["task_manifest_sha256"]),
        ("stage1_result", paths["stage1_result"], hashes["stage1_result_sha256"]),
        (
            "generation_manifest",
            paths["generation_manifest"],
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation_metrics",
            paths["generation_metrics"],
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation_last",
            paths["generation_last"],
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_output",
            paths["generation_output"],
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation_prompt",
            paths["generation_root"] / "prompt.txt",
            hashes["generation_prompt_sha256"],
        ),
        (
            "generation_usage",
            paths["generation_root"] / "usage.json",
            hashes["generation_usage_sha256"],
        ),
    ]
    for label, path, expected in direct_hash_checks:
        overall &= check_file(label, path, expected)

    candidate = paths["candidate"]
    result_record = json.loads(Path("/generation-result.json").read_text())
    invocation_record = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    candidate_tree_actual = pipeline_sha256_tree(candidate)
    candidate_tree_expected = result_record["outputs"]["workspace_sha256"]
    candidate_tree_ok = (
        candidate_tree_actual == candidate_tree_expected
        and candidate_tree_actual == invocation_record["retained_workspace_sha256"]
    )
    print(
        f"candidate_pipeline_tree_sha256={candidate_tree_actual} "
        f"result_expected={candidate_tree_expected} "
        f"invocation_expected={invocation_record['retained_workspace_sha256']} "
        f"ok={candidate_tree_ok}"
    )
    overall &= candidate_tree_ok

    usage_record = json.loads(
        (paths["generation_root"] / "usage.json").read_text()
    )
    trace_tree_actual = pipeline_sha256_tree(paths["generation_trace"])
    trace_tree_expected = usage_record["source_trace_sha256"]
    trace_tree_ok = trace_tree_actual == trace_tree_expected
    print(
        f"generation_trace_pipeline_tree_sha256={trace_tree_actual} "
        f"usage_expected={trace_tree_expected} ok={trace_tree_ok}"
    )
    overall &= trace_tree_ok
    print(
        "audit_input_separate_composite_hash_records="
        f"candidate:{hashes['candidate_tree_sha256']} "
        f"trace:{hashes['generation_codex_trace_sha256']}"
    )

    candidate_prompt = candidate / "prompt.py"
    candidate_translator = candidate / "py2mpy.py"
    overall &= check_file(
        "candidate_prompt",
        candidate_prompt,
        hashes["candidate_prompt_sha256"],
    )
    overall &= check_file(
        "candidate_translator",
        candidate_translator,
        hashes["candidate_translator_sha256"],
    )
    prompt_same = candidate_prompt.read_bytes() == paths["trusted_prompt"].read_bytes()
    translator_same = (
        candidate_translator.read_bytes() == paths["translator"].read_bytes()
    )
    print(f"candidate_prompt_byte_identity={prompt_same}")
    print(f"candidate_translator_byte_identity={translator_same}")
    overall &= prompt_same and translator_same

    required_legacy_selected = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_legacy_selected:
        ok = (
            (path.is_dir() if path.name == "codex-trace" else path.is_file())
            and not path.is_symlink()
            and os.access(path, os.R_OK)
        )
        print(f"required_record:{path}: ok={ok}")
        overall &= ok

    result = result_record
    invocation = invocation_record
    for owner, record in (("result", result), ("invocation", invocation)):
        for relative, expected in record["outputs"]["evidence"].items():
            artifact = Path("/generation-evidence") / relative
            ok = check_file(f"{owner}.outputs.evidence:{relative}", artifact, expected)
            overall &= ok

    no_reference_semantics = not Path("/reference/reference-semantics").exists()
    no_candidate_reference_semantics = not (
        candidate / "reference-semantics"
    ).exists()
    print(f"trusted_reference_semantics_absent={no_reference_semantics}")
    print(f"candidate_reference_semantics_absent={no_candidate_reference_semantics}")
    overall &= no_reference_semantics

    symlinks = [
        str(path)
        for root in (candidate, Path("/reference"), Path("/generation-evidence"))
        for path in root.rglob("*")
        if path.is_symlink()
    ]
    print(f"symlinks={symlinks}")
    overall &= not symlinks

    trace_files = sorted(paths["generation_trace"].rglob("*"))
    regular_trace_files = [
        path for path in trace_files if path.is_file() and not path.is_symlink()
    ]
    print(f"trace_regular_files={[str(path) for path in regular_trace_files]}")
    overall &= len(regular_trace_files) > 0

    print(f"OVERALL_DIRECT_PROVENANCE_CHECK={overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
