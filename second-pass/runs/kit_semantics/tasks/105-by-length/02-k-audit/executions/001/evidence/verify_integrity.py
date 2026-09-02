#!/usr/bin/env python3
"""Independent audit-input, provenance, and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest(root: Path) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            result.append((relative, "symlink", os.readlink(path)))
        elif stat.S_ISDIR(mode):
            result.append((relative, "directory", "-"))
        elif stat.S_ISREG(mode):
            result.append((relative, "file", sha256_file(path)))
        else:
            result.append((relative, "other", oct(mode)))
    return result


def manifest_digest(manifest: list[tuple[str, str, str]]) -> str:
    encoded = json.dumps(manifest, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the pipeline-v3 length-delimited tree digest independently."""
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((relative, "file", path))
        else:
            raise ValueError(f"unsupported entry in pipeline tree digest: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            raw = path.read_bytes()
            digest.update(len(raw).to_bytes(8, "big"))
            digest.update(raw)
    return digest.hexdigest()


def require_regular(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required regular file: {path}")
    elif path.is_symlink():
        errors.append(f"required regular file is symlinked: {path}")
    elif not path.is_file():
        errors.append(f"required regular file has wrong type: {path}")


def require_directory(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required directory: {path}")
    elif path.is_symlink():
        errors.append(f"required directory is symlinked: {path}")
    elif not path.is_dir():
        errors.append(f"required directory has wrong type: {path}")


def main() -> int:
    errors: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    print(f"condition={audit.get('condition')}")

    if audit.get("record_layout") != "pipeline-v3":
        errors.append("record layout is not pipeline-v3")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        errors.append("semantics mode is not SUPPLIED_SEMANTICS")
    if audit.get("audit_campaign") != lock:
        errors.append("campaign lock JSON does not exactly match audit_campaign block")
    else:
        print("campaign_block_exact_match=true")

    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    actual_lock_hash = sha256_file(CAMPAIGN_LOCK)
    print(f"audit_campaign_lock expected={expected_lock_hash} actual={actual_lock_hash}")
    if actual_lock_hash != expected_lock_hash:
        errors.append("campaign lock byte hash mismatch")

    container_paths = audit.get("container_paths", {})
    file_keys = {
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
    directory_keys = {"candidate", "generation_root", "generation_trace"}
    for key, raw_path in sorted(container_paths.items()):
        path = Path(raw_path)
        if key in file_keys:
            require_regular(path, errors)
        elif key in directory_keys:
            require_directory(path, errors)
        else:
            errors.append(f"unclassified launcher container path: {key}={path}")
        print(f"container_path {key}={path}")

    required_pipeline_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required_pipeline_files:
        require_regular(path, errors)

    trace_root = Path("/generation-evidence/codex-trace")
    require_directory(trace_root, errors)
    trace_manifest = tree_manifest(trace_root) if trace_root.is_dir() else []
    trace_files = [entry for entry in trace_manifest if entry[1] == "file"]
    if not trace_files:
        errors.append("structured trace contains no regular files")
    for relative, kind, payload in trace_manifest:
        if kind not in {"file", "directory"}:
            errors.append(f"structured trace has disallowed {kind}: {relative} -> {payload}")
    print(f"trace_entries={len(trace_manifest)} trace_files={len(trace_files)}")
    print(f"trace_manifest_sha256_independent={manifest_digest(trace_manifest)}")
    if trace_root.is_dir():
        print(f"trace_pipeline_tree_sha256={pipeline_tree_digest(trace_root)}")

    file_hash_checks = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    }
    hashes = audit["hashes"]
    for path, hash_key in file_hash_checks.items():
        require_regular(path, errors)
        if path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            expected = hashes[hash_key]
            ok = actual == expected
            print(f"hash {path} key={hash_key} expected={expected} actual={actual} match={ok}")
            if not ok:
                errors.append(f"hash mismatch: {path} ({hash_key})")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    require_directory(trusted_semantics, errors)
    require_directory(candidate_semantics, errors)
    trusted_manifest = tree_manifest(trusted_semantics) if trusted_semantics.is_dir() else []
    candidate_manifest = tree_manifest(candidate_semantics) if candidate_semantics.is_dir() else []
    for label, manifest in (
        ("trusted semantics", trusted_manifest),
        ("candidate semantics", candidate_manifest),
    ):
        for relative, kind, payload in manifest:
            if kind not in {"file", "directory"}:
                errors.append(f"{label} has disallowed {kind}: {relative} -> {payload}")
    print(f"trusted_semantics_entries={len(trusted_manifest)}")
    print(f"candidate_semantics_entries={len(candidate_manifest)}")
    print(f"trusted_semantics_manifest_sha256_independent={manifest_digest(trusted_manifest)}")
    print(f"candidate_semantics_manifest_sha256_independent={manifest_digest(candidate_manifest)}")
    if trusted_semantics.is_dir():
        trusted_pipeline_digest = pipeline_tree_digest(trusted_semantics)
        print(f"trusted_semantics_pipeline_tree_sha256={trusted_pipeline_digest}")
        expected = hashes["trusted_reference_semantics_manifest_sha256"]
        if trusted_pipeline_digest != expected:
            errors.append("trusted semantics pipeline tree hash mismatch")
    if candidate_semantics.is_dir():
        candidate_pipeline_digest = pipeline_tree_digest(candidate_semantics)
        print(f"candidate_semantics_pipeline_tree_sha256={candidate_pipeline_digest}")
        if candidate_pipeline_digest != hashes["trusted_reference_semantics_manifest_sha256"]:
            errors.append("candidate semantics pipeline tree hash differs from trusted recorded hash")
    if trusted_manifest != candidate_manifest:
        trusted_set = set(trusted_manifest)
        candidate_set = set(candidate_manifest)
        for entry in sorted(trusted_set - candidate_set):
            errors.append(f"candidate semantics missing/changed entry: {entry}")
        for entry in sorted(candidate_set - trusted_set):
            errors.append(f"candidate semantics additional/changed entry: {entry}")
    else:
        print("candidate_semantics_recursive_type_and_byte_match=true")

    candidate_root = Path("/candidate")
    candidate_manifest_all = tree_manifest(candidate_root) if candidate_root.is_dir() else []
    print(f"candidate_entries={len(candidate_manifest_all)}")
    print(f"candidate_manifest_sha256_independent={manifest_digest(candidate_manifest_all)}")
    if candidate_root.is_dir():
        candidate_pipeline_digest = pipeline_tree_digest(candidate_root)
        print(f"candidate_pipeline_tree_sha256={candidate_pipeline_digest}")
        generation_result = json.loads(Path("/generation-result.json").read_text())
        expected_workspace = generation_result["outputs"]["workspace_sha256"]
        if candidate_pipeline_digest != expected_workspace:
            errors.append("candidate tree differs from generation-result workspace hash")
        else:
            print("candidate_matches_generation_workspace_hash=true")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    for label, record in (("generation-result", generation_result), ("invocation", invocation)):
        evidence_hashes = record["outputs"]["evidence"]
        for relative, expected in sorted(evidence_hashes.items()):
            path = Path("/generation-evidence") / relative
            require_regular(path, errors)
            if path.is_file() and not path.is_symlink():
                actual = sha256_file(path)
                print(
                    f"{label}_evidence_hash {relative} expected={expected} "
                    f"actual={actual} match={expected == actual}"
                )
                if expected != actual:
                    errors.append(f"{label} evidence hash mismatch: {relative}")
    for required_name in (
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ):
        require_regular(candidate_root / required_name, errors)

    print(f"errors={len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
