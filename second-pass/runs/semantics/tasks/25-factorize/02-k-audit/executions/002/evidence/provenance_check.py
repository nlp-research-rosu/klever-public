#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(path: Path) -> str:
    try:
        info = path.lstat()
    except OSError as err:
        return f"MISSING/UNREADABLE: {err}"
    if stat.S_ISREG(info.st_mode):
        kind = "regular"
    elif stat.S_ISDIR(info.st_mode):
        kind = "directory"
    elif stat.S_ISLNK(info.st_mode):
        kind = f"symlink->{os.readlink(path)}"
    else:
        kind = f"other-mode-{stat.S_IFMT(info.st_mode):o}"
    return f"{kind} mode={stat.S_IMODE(info.st_mode):04o} readable={os.access(path, os.R_OK)}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                entries[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(info.st_mode):
                entries[rel] = ("directory", None)
            elif stat.S_ISREG(info.st_mode):
                entries[rel] = ("regular", sha256(path))
            else:
                entries[rel] = (f"other-{stat.S_IFMT(info.st_mode):o}", None)
    return entries


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    print(f"audit-input: {describe(AUDIT)}")
    print(f"audit-campaign-lock: {describe(LOCK)}")
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"campaign_block_equals_lock={audit.get('audit_campaign') == lock}")
    actual_lock_hash = sha256(LOCK)
    recorded_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_lock_sha256 actual={actual_lock_hash} recorded={recorded_lock_hash} match={actual_lock_hash == recorded_lock_hash}")

    container_paths = audit["container_paths"]
    print("launcher-declared container paths:")
    for key, raw_path in sorted(container_paths.items()):
        path = Path(raw_path)
        print(f"  {key}: {path}: {describe(path)}")

    required = {
        "run_manifest": Path("/run.json"),
        "task_manifest": Path("/task.json"),
        "stage1_result": Path("/generation-result.json"),
        "invocation": Path("/generation-evidence/invocation.json"),
        "metrics": Path("/generation-evidence/metrics.json"),
        "codex_last": Path("/generation-evidence/codex-last.txt"),
        "codex_output": Path("/generation-evidence/codex-output.log"),
        "prompt": Path("/generation-evidence/prompt.txt"),
        "trace": Path("/generation-evidence/codex-trace"),
    }
    if Path("/generation-evidence/usage.json").exists():
        required["usage_present"] = Path("/generation-evidence/usage.json")
    print("required legacy-selected-stage1 records:")
    missing = False
    for name, path in required.items():
        desc = describe(path)
        ok = path.exists() and os.access(path, os.R_OK) and not path.is_symlink()
        missing |= not ok
        print(f"  {name}: ok={ok} {desc}")
    print(f"required_records_all_intact={not missing}")

    direct_hashes = {
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    }
    all_direct_match = True
    print("independent direct-file hashes:")
    for key, path in direct_hashes.items():
        actual = sha256(path)
        recorded = audit["hashes"].get(key)
        match = actual == recorded
        all_direct_match &= match
        print(f"  {key}: actual={actual} recorded={recorded} match={match}")
    print(f"all_recorded_direct_hashes_match={all_direct_match}")

    prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print(f"candidate_prompt_byte_equal_trusted={prompt_equal}")
    print(f"candidate_translator_byte_equal_trusted={translator_equal}")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    print(f"trusted_semantics: {describe(trusted_semantics)}")
    print(f"candidate_semantics: {describe(candidate_semantics)}")
    trusted_entries = tree_entries(trusted_semantics)
    candidate_entries = tree_entries(candidate_semantics)
    print(f"trusted_semantics_entry_count={len(trusted_entries)}")
    print(f"candidate_semantics_entry_count={len(candidate_entries)}")
    missing_entries = sorted(set(trusted_entries) - set(candidate_entries))
    additional_entries = sorted(set(candidate_entries) - set(trusted_entries))
    changed_entries = sorted(
        path
        for path in set(trusted_entries) & set(candidate_entries)
        if trusted_entries[path] != candidate_entries[path]
    )
    print(f"semantics_missing_entries={missing_entries}")
    print(f"semantics_additional_entries={additional_entries}")
    print(f"semantics_changed_or_mistyped_entries={changed_entries}")
    print(f"semantics_exact_recursive_match={not (missing_entries or additional_entries or changed_entries)}")
    print("trusted semantics independent entry inventory:")
    for rel, (kind, detail) in sorted(trusted_entries.items()):
        print(f"  {rel}: {kind}" + (f" sha256={detail}" if detail else ""))

    print("candidate independent entry inventory:")
    for rel, (kind, detail) in sorted(tree_entries(Path("/candidate")).items()):
        print(f"  {rel}: {kind}" + (f" sha256={detail}" if detail else ""))

    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text(encoding="utf-8"))
    recorded_outputs = result["outputs"]["evidence"]
    invocation_outputs = invocation["outputs"]["evidence"]
    print("generation-evidence output hash cross-check:")
    output_match = True
    for rel, expected in sorted(recorded_outputs.items()):
        path = Path("/generation-evidence") / rel
        actual = sha256(path)
        inv_expected = invocation_outputs.get(rel)
        match = actual == expected == inv_expected
        output_match &= match
        print(f"  {rel}: actual={actual} result={expected} invocation={inv_expected} match={match}")
    print(f"generation_output_hashes_match_manifests={output_match}")
    return 0 if (not missing and all_direct_match and prompt_equal and translator_equal and not (missing_entries or additional_entries or changed_entries) and output_match and audit.get("audit_campaign") == lock and actual_lock_hash == recorded_lock_hash) else 1


if __name__ == "__main__":
    raise SystemExit(main())
