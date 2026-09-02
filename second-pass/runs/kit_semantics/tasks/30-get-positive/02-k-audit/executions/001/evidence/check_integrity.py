#!/usr/bin/env python3
"""Reviewer-authored integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for directory, names, filenames in os.walk(root, topdown=True, followlinks=False):
        names.sort()
        filenames.sort()
        base = Path(directory)
        for name in names + filenames:
            path = base / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = ("other", oct(mode))
    return result


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())
    failures: list[str] = []

    lock_hash = sha256(CAMPAIGN_LOCK)
    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_lock_sha256={lock_hash}")
    print(f"campaign_lock_hash_matches={lock_hash == expected_lock_hash}")
    print(f"campaign_lock_object_matches={lock == audit['audit_campaign']}")
    if lock_hash != expected_lock_hash or lock != audit["audit_campaign"]:
        failures.append("campaign lock mismatch")

    required_pipeline_v3 = [
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
        Path("/generation-evidence/codex-trace"),
    ]
    print(f"record_layout={audit['record_layout']}")
    for path in required_pipeline_v3:
        exists = path.exists()
        symlink = path.is_symlink()
        readable = os.access(path, os.R_OK)
        print(f"required={path} exists={exists} readable={readable} symlink={symlink}")
        if not exists or not readable or symlink:
            failures.append(f"bad required record: {path}")
        if path.suffix == ".json" and exists and not symlink:
            json.loads(path.read_text())

    hash_paths = {
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    for key, path in hash_paths.items():
        actual = sha256(path)
        expected = audit["hashes"][key]
        matches = actual == expected
        print(f"hash={key} matches={matches} actual={actual}")
        if not matches:
            failures.append(f"hash mismatch: {path}")

    trace_files = sorted(
        path for path in Path("/generation-evidence/codex-trace").rglob("*")
        if path.is_file()
    )
    generation_result = json.loads(Path("/generation-result.json").read_text())
    expected_trace = {
        key.removeprefix("codex-trace/"): value
        for key, value in generation_result["outputs"]["evidence"].items()
        if key.startswith("codex-trace/")
    }
    actual_trace = {
        path.relative_to("/generation-evidence/codex-trace").as_posix(): sha256(path)
        for path in trace_files
    }
    print(f"trace_manifest_matches={actual_trace == expected_trace}")
    for rel, digest in actual_trace.items():
        print(f"trace_file={rel} sha256={digest}")
    if actual_trace != expected_trace:
        failures.append("trace manifest mismatch")

    candidate_prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    candidate_translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print(f"candidate_prompt_byte_equal={candidate_prompt_equal}")
    print(f"candidate_translator_byte_equal={candidate_translator_equal}")
    if not candidate_prompt_equal or not candidate_translator_equal:
        failures.append("candidate trusted input mismatch")

    candidate_semantics = scan_tree(Path("/candidate/reference-semantics"))
    trusted_semantics = scan_tree(Path("/reference/reference-semantics"))
    print(f"candidate_semantics_entries={len(candidate_semantics)}")
    print(f"trusted_semantics_entries={len(trusted_semantics)}")
    print(f"semantics_trees_exact={candidate_semantics == trusted_semantics}")
    bad_types = [
        f"{rel}:{kind}"
        for rel, (kind, _) in candidate_semantics.items()
        if kind not in {"directory", "file"}
    ]
    print(f"candidate_semantics_bad_types={bad_types}")
    if candidate_semantics != trusted_semantics or bad_types:
        failures.append("supplied semantics integrity failure")

    candidate_scan = scan_tree(Path("/candidate"))
    trace_scan = scan_tree(Path("/generation-evidence/codex-trace"))
    candidate_bad_types = [
        f"{rel}:{kind}" for rel, (kind, _) in candidate_scan.items()
        if kind not in {"directory", "file"}
    ]
    trace_bad_types = [
        f"{rel}:{kind}" for rel, (kind, _) in trace_scan.items()
        if kind not in {"directory", "file"}
    ]
    print(f"candidate_bad_types={candidate_bad_types}")
    print(f"trace_bad_types={trace_bad_types}")
    if candidate_bad_types or trace_bad_types:
        failures.append("symlink or special file in mounted tree")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE={failure}")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
