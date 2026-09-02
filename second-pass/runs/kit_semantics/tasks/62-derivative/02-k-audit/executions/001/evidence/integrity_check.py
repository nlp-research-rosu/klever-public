#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path, *, infrastructure: bool = True) -> bool:
    label = "INFRA" if infrastructure else "CANDIDATE"
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        print(f"{label}_ERROR missing/unreadable {path}: {err}")
        return False
    if not stat.S_ISREG(mode) or path.is_symlink():
        print(f"{label}_ERROR not a regular non-symlink file: {path}")
        return False
    try:
        with path.open("rb") as stream:
            stream.read(1)
    except OSError as err:
        print(f"{label}_ERROR unreadable {path}: {err}")
        return False
    print(f"OK regular readable {path}")
    return True


def walk_tree(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries[relative] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                entries[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                entries[relative] = ("file", sha256_file(path))
            else:
                entries[relative] = ("special", f"mode={oct(mode)}")
    return entries


def tree_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    """Reviewer-defined digest; individual entries remain the primary check."""
    digest = hashlib.sha256()
    for relative, (kind, value) in sorted(entries.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(kind.encode("ascii"))
        digest.update(b"\0")
        digest.update((value or "").encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def check_hash(path: Path, expected: str, label: str) -> bool:
    actual = sha256_file(path)
    ok = actual == expected
    print(f"{'OK' if ok else 'MISMATCH'} {label}: expected={expected} actual={actual} path={path}")
    return ok


def main() -> int:
    infra_ok = True
    candidate_ok = True

    if not require_regular(AUDIT_INPUT):
        return 2
    if not require_regular(LOCK):
        return 2

    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    same_campaign = audit["audit_campaign"] == lock
    print(f"{'OK' if same_campaign else 'INFRA_ERROR'} campaign lock content equality: {same_campaign}")
    infra_ok &= same_campaign
    infra_ok &= check_hash(
        LOCK,
        audit["hashes"]["audit_campaign_lock_sha256"],
        "audit campaign lock SHA-256",
    )

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    if audit.get("record_layout") != "pipeline-v3":
        print("INFRA_ERROR unexpected record layout")
        infra_ok = False
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        print("INFRA_ERROR rendered semantics-mode contradiction")
        infra_ok = False

    required = {
        "run_manifest": Path("/run.json"),
        "task_manifest": Path("/task.json"),
        "stage1_result": Path("/generation-result.json"),
        "generation_manifest": Path("/generation-evidence/invocation.json"),
        "generation_metrics": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage": Path("/generation-evidence/usage.json"),
        "generation_last": Path("/generation-evidence/codex-last.txt"),
        "generation_output": Path("/generation-evidence/codex-output.log"),
        "generation_prompt": Path("/generation-evidence/prompt.txt"),
        "trusted_canonical": Path("/reference/canonical.py"),
        "trusted_prompt": Path("/reference/prompt.py"),
        "trusted_translator": Path("/reference/py2mpy.py"),
    }
    for path in required.values():
        infra_ok &= require_regular(path)

    expected_hashes = {
        "/run.json": audit["hashes"]["run_manifest_sha256"],
        "/task.json": audit["hashes"]["task_manifest_sha256"],
        "/generation-result.json": audit["hashes"]["stage1_result_sha256"],
        "/generation-evidence/invocation.json": audit["hashes"]["stage1_invocation_sha256"],
        "/generation-evidence/metrics.json": audit["hashes"]["generation_metrics_sha256"],
        "/generation-evidence/runtime-metrics.json": audit["hashes"]["generation_runtime_metrics_sha256"],
        "/generation-evidence/usage.json": audit["hashes"]["generation_usage_sha256"],
        "/generation-evidence/codex-last.txt": audit["hashes"]["generation_codex_last_sha256"],
        "/generation-evidence/codex-output.log": audit["hashes"]["generation_codex_output_sha256"],
        "/generation-evidence/prompt.txt": audit["hashes"]["generation_prompt_sha256"],
        "/reference/canonical.py": audit["hashes"]["canonical_sha256"],
        "/reference/prompt.py": audit["hashes"]["trusted_prompt_sha256"],
        "/reference/py2mpy.py": audit["hashes"]["trusted_translator_sha256"],
        "/candidate/prompt.py": audit["hashes"]["candidate_prompt_sha256"],
        "/candidate/py2mpy.py": audit["hashes"]["candidate_translator_sha256"],
    }
    for raw_path, expected in expected_hashes.items():
        path = Path(raw_path)
        if require_regular(path, infrastructure=not raw_path.startswith("/candidate/")):
            match = check_hash(path, expected, "recorded SHA-256")
            if raw_path.startswith("/candidate/"):
                candidate_ok &= match
            else:
                infra_ok &= match
        elif raw_path.startswith("/candidate/"):
            candidate_ok = False
        else:
            infra_ok = False

    result = json.loads(Path("/generation-result.json").read_text())
    evidence_hashes = result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        if require_regular(path):
            infra_ok &= check_hash(path, expected, "generation-result evidence SHA-256")
        else:
            infra_ok = False

    trace_root = Path("/generation-evidence/codex-trace")
    trace_entries = walk_tree(trace_root)
    trace_files = [name for name, (kind, _) in trace_entries.items() if kind == "file"]
    trace_bad = [(name, kind) for name, (kind, _) in trace_entries.items() if kind not in {"file", "directory"}]
    print(f"trace regular files={len(trace_files)} entries={trace_files}")
    print(f"trace non-regular entries={trace_bad}")
    infra_ok &= len(trace_files) > 0 and not trace_bad
    print(f"recorded launcher trace-tree digest={audit['hashes']['generation_codex_trace_sha256']}")
    print(f"reviewer trace-tree digest={tree_digest(trace_entries)}")

    candidate_root = Path("/candidate")
    if not candidate_root.is_dir() or candidate_root.is_symlink():
        print("INFRA_ERROR candidate mount missing or not a real directory")
        infra_ok = False
    else:
        candidate_tree_entries = walk_tree(candidate_root)
        candidate_tree_bad = [
            (name, kind)
            for name, (kind, _) in candidate_tree_entries.items()
            if kind not in {"file", "directory"}
        ]
        print(f"candidate tree entries={len(candidate_tree_entries)}")
        print(f"candidate tree non-regular entries={candidate_tree_bad}")
        print(f"recorded launcher candidate-tree digest={audit['hashes']['candidate_tree_sha256']}")
        print(f"reviewer candidate-tree digest={tree_digest(candidate_tree_entries)}")
        candidate_ok &= not candidate_tree_bad

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        print("INFRA_ERROR trusted supplied semantics missing or not a real directory")
        infra_ok = False
    else:
        trusted_entries = walk_tree(trusted_semantics)
        print(f"trusted semantics entries={len(trusted_entries)} reviewer_digest={tree_digest(trusted_entries)}")
        trusted_bad = [(name, kind) for name, (kind, _) in trusted_entries.items() if kind not in {"file", "directory"}]
        if trusted_bad:
            print(f"INFRA_ERROR trusted semantics non-regular entries={trusted_bad}")
            infra_ok = False

    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        print("CANDIDATE_ERROR supplied-semantics copy missing or not a real directory")
        candidate_ok = False
    elif trusted_semantics.is_dir():
        candidate_entries = walk_tree(candidate_semantics)
        print(f"candidate semantics entries={len(candidate_entries)} reviewer_digest={tree_digest(candidate_entries)}")
        missing = sorted(set(trusted_entries) - set(candidate_entries))
        additional = sorted(set(candidate_entries) - set(trusted_entries))
        changed = sorted(
            name
            for name in set(trusted_entries) & set(candidate_entries)
            if trusted_entries[name] != candidate_entries[name]
        )
        print(f"semantics missing={missing}")
        print(f"semantics additional={additional}")
        print(f"semantics changed_or_mistyped={changed}")
        candidate_ok &= not missing and not additional and not changed

    for candidate_path, trusted_path, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]:
        same = candidate_path.read_bytes() == trusted_path.read_bytes()
        print(f"{'OK' if same else 'CANDIDATE_ERROR'} byte-identical {label}: {same}")
        candidate_ok &= same

    candidate_required = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
        Path("/candidate/PROOF.md"),
    ]
    for path in candidate_required:
        candidate_ok &= require_regular(path, infrastructure=False)

    print(f"INFRASTRUCTURE_INTEGRITY={'PASS' if infra_ok else 'FAIL'}")
    print(f"CANDIDATE_PROVENANCE_INTEGRITY={'PASS' if candidate_ok else 'FAIL'}")
    return 0 if infra_ok else 2


if __name__ == "__main__":
    sys.exit(main())
