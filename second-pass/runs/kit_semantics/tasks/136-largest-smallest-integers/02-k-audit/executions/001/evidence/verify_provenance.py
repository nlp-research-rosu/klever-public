#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit mounts."""

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


def require_plain_file(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode) or stat.S_ISLNK(mode):
        raise AssertionError(f"required plain file has wrong type: {path}")


def require_plain_dir(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
        raise AssertionError(f"required plain directory has wrong type: {path}")


def tree_manifest(root: Path) -> tuple[dict[str, tuple[str, str]], str]:
    result: dict[str, tuple[str, str]] = {}
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
            value = os.readlink(path)
        elif stat.S_ISDIR(mode):
            kind = "directory"
            value = "-"
        elif stat.S_ISREG(mode):
            kind = "file"
            value = sha256(path)
        else:
            kind = "other"
            value = "-"
        result[relative] = (kind, value)
        digest.update(f"{relative}\0{kind}\0{value}\n".encode())
    return result, digest.hexdigest()


def check_declared_hash(path: Path, expected: str) -> None:
    require_plain_file(path)
    actual = sha256(path)
    print(f"hash path={path} expected={expected} actual={actual}")
    if actual != expected:
        raise AssertionError(f"hash mismatch: {path}")


def main() -> int:
    require_plain_file(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    if audit["record_layout"] != "pipeline-v3":
        raise AssertionError(f"unexpected layout: {audit['record_layout']}")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise AssertionError(f"unexpected semantics mode: {audit['semantics_mode']}")

    paths = {name: Path(value) for name, value in audit["container_paths"].items()}
    required_plain_files = [
        paths["audit_campaign_lock"],
        paths["canonical"],
        paths["generation_last"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        paths["generation_output"],
        paths["run_manifest"],
        paths["stage1_result"],
        paths["task_manifest"],
        paths["translator"],
        paths["trusted_prompt"],
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required_plain_files:
        require_plain_file(path)
    for path in (paths["candidate"], paths["generation_root"], paths["generation_trace"]):
        require_plain_dir(path)

    campaign = json.loads(paths["audit_campaign_lock"].read_text(encoding="utf-8"))
    if campaign != audit["audit_campaign"]:
        raise AssertionError("campaign lock content does not match audit_campaign")
    check_declared_hash(
        paths["audit_campaign_lock"], audit["hashes"]["audit_campaign_lock_sha256"]
    )

    declared_file_hashes = [
        (paths["canonical"], "canonical_sha256"),
        (paths["run_manifest"], "run_manifest_sha256"),
        (paths["task_manifest"], "task_manifest_sha256"),
        (paths["stage1_result"], "stage1_result_sha256"),
        (paths["generation_manifest"], "stage1_invocation_sha256"),
        (paths["generation_metrics"], "generation_metrics_sha256"),
        (Path("/generation-evidence/runtime-metrics.json"), "generation_runtime_metrics_sha256"),
        (Path("/generation-evidence/usage.json"), "generation_usage_sha256"),
        (paths["generation_last"], "generation_codex_last_sha256"),
        (paths["generation_output"], "generation_codex_output_sha256"),
        (Path("/generation-evidence/prompt.txt"), "generation_prompt_sha256"),
        (paths["translator"], "trusted_translator_sha256"),
        (paths["trusted_prompt"], "trusted_prompt_sha256"),
    ]
    for path, key in declared_file_hashes:
        check_declared_hash(path, audit["hashes"][key])

    invocation = json.loads(paths["generation_manifest"].read_text(encoding="utf-8"))
    result = json.loads(paths["stage1_result"].read_text(encoding="utf-8"))
    trace_files = sorted(paths["generation_trace"].rglob("*"))
    trace_files = [path for path in trace_files if path.is_file() and not path.is_symlink()]
    expected_outputs = result["outputs"]["evidence"]
    if invocation["outputs"]["evidence"] != expected_outputs:
        raise AssertionError("invocation and generation-result output maps differ")
    generation_root = paths["generation_root"]
    for relative, expected in sorted(expected_outputs.items()):
        path = generation_root / relative
        check_declared_hash(path, expected)
    expected_trace_names = {
        (generation_root / relative).resolve()
        for relative in expected_outputs
        if relative.startswith("codex-trace/")
    }
    actual_trace_names = {path.resolve() for path in trace_files}
    if actual_trace_names != expected_trace_names:
        raise AssertionError(
            f"trace entry mismatch expected={expected_trace_names} actual={actual_trace_names}"
        )

    candidate_prompt = paths["candidate"] / "prompt.py"
    candidate_translator = paths["candidate"] / "py2mpy.py"
    require_plain_file(candidate_prompt)
    require_plain_file(candidate_translator)
    if candidate_prompt.read_bytes() != paths["trusted_prompt"].read_bytes():
        raise AssertionError("candidate prompt differs from trusted prompt")
    if candidate_translator.read_bytes() != paths["translator"].read_bytes():
        raise AssertionError("candidate translator differs from trusted translator")

    candidate_semantics = paths["candidate"] / "reference-semantics"
    trusted_semantics = Path("/reference/reference-semantics")
    require_plain_dir(candidate_semantics)
    require_plain_dir(trusted_semantics)
    candidate_manifest, candidate_digest = tree_manifest(candidate_semantics)
    trusted_manifest, trusted_digest = tree_manifest(trusted_semantics)
    print(
        "semantics "
        f"candidate_entries={len(candidate_manifest)} trusted_entries={len(trusted_manifest)} "
        f"candidate_independent_digest={candidate_digest} "
        f"trusted_independent_digest={trusted_digest}"
    )
    if candidate_manifest != trusted_manifest:
        missing = sorted(set(trusted_manifest) - set(candidate_manifest))
        additional = sorted(set(candidate_manifest) - set(trusted_manifest))
        changed = sorted(
            key
            for key in set(candidate_manifest) & set(trusted_manifest)
            if candidate_manifest[key] != trusted_manifest[key]
        )
        raise AssertionError(
            f"semantics mismatch missing={missing} additional={additional} changed={changed}"
        )

    candidate_manifest, candidate_digest = tree_manifest(paths["candidate"])
    print(
        f"candidate entries={len(candidate_manifest)} "
        f"independent_manifest_digest={candidate_digest}"
    )
    generation_manifest, generation_digest = tree_manifest(paths["generation_root"])
    print(
        f"generation_evidence entries={len(generation_manifest)} "
        f"independent_manifest_digest={generation_digest}"
    )
    print("PROVENANCE-INTEGRITY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
