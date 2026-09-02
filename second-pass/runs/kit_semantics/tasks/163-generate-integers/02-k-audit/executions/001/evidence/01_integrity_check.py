#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit record.

This script is reviewer-authored.  It only reads launcher/candidate mounts and
prints its findings; it does not rely on candidate reports or compiled output.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode) or path.is_symlink():
        raise AssertionError(f"not a real regular file: {path}")
    if not os.access(path, os.R_OK):
        raise AssertionError(f"not readable: {path}")
    print(f"OK regular readable {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode) or path.is_symlink():
        raise AssertionError(f"not a real directory: {path}")
    if not os.access(path, os.R_OK | os.X_OK):
        raise AssertionError(f"not readable/searchable: {path}")
    print(f"OK directory readable {path}")


def regular_tree(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            entry_path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                pending.append(entry_path)
            elif stat.S_ISREG(mode):
                relative = entry_path.relative_to(root).as_posix()
                result[relative] = digest(entry_path)
            else:
                raise AssertionError(
                    f"linked or unsupported tree entry: {entry_path}"
                )
    return dict(sorted(result.items()))


def manifest_digest(entries: dict[str, str]) -> str:
    """Reviewer-defined digest of the explicit relative-path/content manifest."""
    encoded = json.dumps(
        entries, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def check_recorded_hash(
    name: str, path: Path, recorded: dict[str, str]
) -> None:
    actual = digest(path)
    expected = recorded[name]
    if actual != expected:
        raise AssertionError(
            f"hash mismatch {name}: expected {expected}, actual {actual}"
        )
    print(f"OK sha256 {name} {actual} {path}")


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/01_integrity_check.py")
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    if audit["record_layout"] != "pipeline-v3":
        raise AssertionError(f"unexpected record layout: {audit['record_layout']}")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise AssertionError(
            f"unexpected semantics mode: {audit['semantics_mode']}"
        )

    required_files = [
        AUDIT_INPUT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_directories:
        require_directory(path)

    paths = audit["container_paths"]
    expected_container_paths = {
        "audit_campaign_lock": "/audit-campaign-lock.json",
        "candidate": "/candidate",
        "canonical": "/reference/canonical.py",
        "generation_last": "/generation-evidence/codex-last.txt",
        "generation_manifest": "/generation-evidence/invocation.json",
        "generation_metrics": "/generation-evidence/metrics.json",
        "generation_output": "/generation-evidence/codex-output.log",
        "generation_root": "/generation-evidence",
        "generation_trace": "/generation-evidence/codex-trace",
        "run_manifest": "/run.json",
        "stage1_result": "/generation-result.json",
        "task_manifest": "/task.json",
        "translator": "/reference/py2mpy.py",
        "trusted_prompt": "/reference/prompt.py",
    }
    if paths != expected_container_paths:
        raise AssertionError(f"unexpected container_paths: {paths}")
    print("OK launcher container_paths map")

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    if audit["audit_campaign"] != lock:
        raise AssertionError("audit campaign block differs from campaign lock")
    print("OK campaign block equals lock JSON")

    hashes = audit["hashes"]
    checks = {
        "audit_campaign_lock_sha256": LOCK,
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path(
            "/generation-evidence/invocation.json"
        ),
        "generation_metrics_sha256": Path(
            "/generation-evidence/metrics.json"
        ),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path(
            "/generation-evidence/usage.json"
        ),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path(
            "/generation-evidence/prompt.txt"
        ),
    }
    for name, path in checks.items():
        check_recorded_hash(name, path, hashes)

    if Path("/candidate/prompt.py").read_bytes() != Path(
        "/reference/prompt.py"
    ).read_bytes():
        raise AssertionError("candidate prompt differs from trusted prompt")
    if Path("/candidate/py2mpy.py").read_bytes() != Path(
        "/reference/py2mpy.py"
    ).read_bytes():
        raise AssertionError("candidate translator differs from trusted translator")
    print("OK candidate prompt and translator byte identity")

    candidate_tree = regular_tree(Path("/candidate"))
    required_candidate_artifacts = {
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
        "prompt.py",
        "py2mpy.py",
    }
    missing_candidate = sorted(required_candidate_artifacts - set(candidate_tree))
    if missing_candidate:
        raise AssertionError(
            f"missing required candidate proof artifacts: {missing_candidate}"
        )
    print(
        "OK full candidate tree regular entries "
        f"files={len(candidate_tree)} "
        f"reviewer_manifest_sha256={manifest_digest(candidate_tree)}"
    )

    trusted_semantics = regular_tree(Path("/reference/reference-semantics"))
    candidate_semantics = regular_tree(Path("/candidate/reference-semantics"))
    if trusted_semantics != candidate_semantics:
        trusted_names = set(trusted_semantics)
        candidate_names = set(candidate_semantics)
        raise AssertionError(
            "reference-semantics mismatch: "
            f"missing={sorted(trusted_names - candidate_names)}, "
            f"additional={sorted(candidate_names - trusted_names)}, "
            f"changed={sorted(name for name in trusted_names & candidate_names if trusted_semantics[name] != candidate_semantics[name])}"
        )
    print(
        "OK reference-semantics recursive type/name/content identity "
        f"files={len(trusted_semantics)} "
        f"reviewer_manifest_sha256={manifest_digest(trusted_semantics)}"
    )

    result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    for record_name, record in (
        ("generation-result", result),
        ("invocation", invocation),
    ):
        for relative, expected in record["outputs"]["evidence"].items():
            artifact = Path("/generation-evidence") / relative
            require_regular(artifact)
            actual = digest(artifact)
            if actual != expected:
                raise AssertionError(
                    f"{record_name} evidence mismatch {relative}: "
                    f"expected {expected}, actual {actual}"
                )
        print(f"OK all evidence hashes in {record_name}")

    trace_tree = regular_tree(Path("/generation-evidence/codex-trace"))
    print(
        "OK trace tree regular entries "
        f"files={len(trace_tree)} "
        f"reviewer_manifest_sha256={manifest_digest(trace_tree)}"
    )
    type_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    trace_lines = 0
    for relative in trace_tree:
        trace_path = Path("/generation-evidence/codex-trace") / relative
        with trace_path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                event = json.loads(line)
                trace_lines += 1
                type_counts[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_counts[str(payload.get("type"))] += 1
    print(f"OK structured trace JSON lines={trace_lines}")
    print(f"TRACE top-level types={dict(sorted(type_counts.items()))}")
    print(f"TRACE payload types={dict(sorted(payload_counts.items()))}")

    task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    audit_manifest = dict(audit["manifest"])
    audit_manifest_config = audit_manifest.pop("config", None)
    if task != audit_manifest:
        raise AssertionError(
            "task manifest differs from the launcher manifest fields"
        )
    if audit_manifest_config != audit["config"]:
        raise AssertionError(
            "launcher-added manifest config differs from top-level config"
        )
    print(
        "OK task manifest equals launcher manifest fields; "
        "launcher-added config agrees with top level"
    )

    print("RESULT: integrity checks passed")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"RESULT: integrity checks FAILED: {error}", file=sys.stderr)
        raise
