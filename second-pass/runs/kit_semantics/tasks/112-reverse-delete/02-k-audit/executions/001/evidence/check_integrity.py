#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import stat
import sys


AUDIT_INPUT = pathlib.Path("/audit-input.json")


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest(root: pathlib.Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            records.append(
                {
                    "path": rel,
                    "type": "file",
                    "size": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
        elif stat.S_ISDIR(mode):
            records.append({"path": rel, "type": "directory"})
        elif stat.S_ISLNK(mode):
            records.append({"path": rel, "type": "symlink", "target": os.readlink(path)})
        else:
            records.append({"path": rel, "type": f"mode-{mode:o}"})
    return records


def manifest_digest(records: list[dict[str, object]]) -> str:
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def require_regular(path: pathlib.Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing: {path}")
    elif path.is_symlink():
        failures.append(f"symlink: {path} -> {os.readlink(path)}")
    elif not path.is_file():
        failures.append(f"not a regular file: {path}")
    elif not os.access(path, os.R_OK):
        failures.append(f"unreadable: {path}")


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    failures: list[str] = []

    required = [
        pathlib.Path("/audit-input.json"),
        pathlib.Path("/audit-campaign-lock.json"),
        pathlib.Path("/run.json"),
        pathlib.Path("/task.json"),
        pathlib.Path("/generation-result.json"),
        pathlib.Path("/generation-evidence/invocation.json"),
        pathlib.Path("/generation-evidence/metrics.json"),
        pathlib.Path("/generation-evidence/runtime-metrics.json"),
        pathlib.Path("/generation-evidence/usage.json"),
        pathlib.Path("/generation-evidence/codex-last.txt"),
        pathlib.Path("/generation-evidence/codex-output.log"),
        pathlib.Path("/generation-evidence/prompt.txt"),
        pathlib.Path("/reference/canonical.py"),
        pathlib.Path("/reference/prompt.py"),
        pathlib.Path("/reference/py2mpy.py"),
        pathlib.Path("/candidate/prompt.py"),
        pathlib.Path("/candidate/py2mpy.py"),
        pathlib.Path("/candidate/solution.py"),
        pathlib.Path("/candidate/solution.mpy"),
        pathlib.Path("/candidate/verification.k"),
        pathlib.Path("/candidate/spec.k"),
        pathlib.Path("/candidate/prove.sh"),
        pathlib.Path("/candidate/PROOF.md"),
    ]
    for path in required:
        require_regular(path, failures)

    campaign = json.loads(pathlib.Path("/audit-campaign-lock.json").read_text())
    if campaign != audit["audit_campaign"]:
        failures.append("campaign lock JSON does not equal audit_input.audit_campaign")

    expected_file_hashes = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    print("FILE HASH CHECKS")
    for name, key in expected_file_hashes.items():
        path = pathlib.Path(name)
        if not path.is_file() or path.is_symlink():
            continue
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        match = actual == expected
        print(f"{match!s:5} {actual} {key} {name}")
        if not match:
            failures.append(f"hash mismatch: {name}: expected {expected}, actual {actual}")

    generation_result = json.loads(pathlib.Path("/generation-result.json").read_text())
    print("\nGENERATION-EVIDENCE OUTPUT HASH CHECKS")
    for rel, expected in sorted(generation_result["outputs"]["evidence"].items()):
        path = pathlib.Path("/generation-evidence") / rel
        require_regular(path, failures)
        if path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            match = actual == expected
            print(f"{match!s:5} {actual} {rel}")
            if not match:
                failures.append(
                    f"generation-result output hash mismatch: {rel}: "
                    f"expected {expected}, actual {actual}"
                )

    trace_root = pathlib.Path("/generation-evidence/codex-trace")
    if not trace_root.is_dir() or trace_root.is_symlink():
        failures.append("generation trace root is missing, symlinked, or not a directory")
    else:
        trace_records = manifest(trace_root)
        trace_non_regular = [
            record for record in trace_records if record["type"] not in {"file", "directory"}
        ]
        if trace_non_regular:
            failures.append(f"generation trace has non-regular entries: {trace_non_regular}")
        print(
            "generation_trace_independent_manifest_sha256="
            f"{manifest_digest(trace_records)}; "
            f"launcher_tree_sha256={audit['hashes']['generation_codex_trace_sha256']}"
        )

    candidate_root = pathlib.Path("/candidate")
    candidate_tree_records = manifest(candidate_root)
    candidate_tree_non_regular = [
        record
        for record in candidate_tree_records
        if record["type"] not in {"file", "directory"}
    ]
    print("\nCANDIDATE TREE INDEPENDENT HASH")
    print(f"entries={len(candidate_tree_records)}")
    print(f"non_regular_entries={candidate_tree_non_regular}")
    print(f"independent_manifest_sha256={manifest_digest(candidate_tree_records)}")
    print(f"launcher_tree_sha256={audit['hashes']['candidate_tree_sha256']}")
    if candidate_tree_non_regular:
        failures.append(f"candidate tree contains non-regular entries: {candidate_tree_non_regular}")

    candidate_semantics = pathlib.Path("/candidate/reference-semantics")
    trusted_semantics = pathlib.Path("/reference/reference-semantics")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append(f"unexpected semantics mode: {audit.get('semantics_mode')!r}")
    for root in (candidate_semantics, trusted_semantics):
        if not root.is_dir() or root.is_symlink():
            failures.append(f"semantics root is missing, symlinked, or not a directory: {root}")

    candidate_records = manifest(candidate_semantics) if candidate_semantics.is_dir() else []
    trusted_records = manifest(trusted_semantics) if trusted_semantics.is_dir() else []
    print("\nSEMANTICS TREE CHECK")
    print(f"candidate_entries={len(candidate_records)}")
    print(f"trusted_entries={len(trusted_records)}")
    print(f"byte_and_type_identity={candidate_records == trusted_records}")
    print(f"candidate_independent_manifest_sha256={manifest_digest(candidate_records)}")
    print(f"trusted_independent_manifest_sha256={manifest_digest(trusted_records)}")
    if candidate_records != trusted_records:
        failures.append("candidate reference-semantics differs from trusted tree")
        candidate_by_path = {record["path"]: record for record in candidate_records}
        trusted_by_path = {record["path"]: record for record in trusted_records}
        for path in sorted(set(candidate_by_path) | set(trusted_by_path)):
            if candidate_by_path.get(path) != trusted_by_path.get(path):
                print(
                    "SEMANTICS_DIFF",
                    path,
                    "candidate=",
                    candidate_by_path.get(path),
                    "trusted=",
                    trusted_by_path.get(path),
                )

    protected_non_regular = [
        record
        for record in candidate_records + trusted_records
        if record["type"] not in {"file", "directory"}
    ]
    if protected_non_regular:
        failures.append(f"semantics trees contain non-regular entries: {protected_non_regular}")

    print("\nCONTAINER PATH CHECKS")
    for key, name in sorted(audit["container_paths"].items()):
        path = pathlib.Path(name)
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        symlink = path.is_symlink()
        print(f"{key}: exists={exists} readable={readable} symlink={symlink} path={path}")
        if not exists or not readable or symlink:
            failures.append(
                f"launcher-declared path invalid: {key}: "
                f"exists={exists}, readable={readable}, symlink={symlink}, path={path}"
            )

    print("\nINTEGRITY FIELD RECOMPUTATION")
    recomputed = {
        "candidate_prompt_matches_trusted":
            sha256_file(pathlib.Path("/candidate/prompt.py"))
            == sha256_file(pathlib.Path("/reference/prompt.py")),
        "candidate_reference_semantics_matches_trusted":
            candidate_records == trusted_records,
        "candidate_translator_matches_trusted":
            sha256_file(pathlib.Path("/candidate/py2mpy.py"))
            == sha256_file(pathlib.Path("/reference/py2mpy.py")),
        "manifest_prompt_hash_matches_trusted":
            audit["manifest"]["inputs"]["problem_prompt_sha256"]
            == sha256_file(pathlib.Path("/reference/prompt.py")),
        "manifest_reference_semantics_hash_matches_trusted":
            audit["manifest"]["inputs"]["reference_semantics_sha256"]
            == audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
        "manifest_translator_hash_matches_trusted":
            audit["manifest"]["inputs"]["translator_sha256"]
            == sha256_file(pathlib.Path("/reference/py2mpy.py")),
    }
    for key, value in recomputed.items():
        recorded = audit["integrity"].get(key)
        print(f"{key}: recomputed={value} recorded={recorded}")
        if value != recorded or not value:
            failures.append(f"integrity field failed: {key}")

    print("\nRESULT")
    if failures:
        for failure in failures:
            print(f"FAILURE: {failure}")
        return 1
    print("all required mounted artifacts are present, regular/readable, and consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
