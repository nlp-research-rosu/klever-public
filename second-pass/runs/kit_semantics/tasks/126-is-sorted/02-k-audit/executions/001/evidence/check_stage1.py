#!/usr/bin/env python3
"""Independent, read-only integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(root: Path) -> tuple[str, int, list[str]]:
    """Reviewer-defined digest over type, relative path, link target or bytes."""
    digest = hashlib.sha256()
    count = 0
    unusual: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(dirpath)
        for name in sorted(dirnames + filenames):
            path = current / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISREG(mode):
                record = (
                    f"file\0{rel}\0{sha256_file(path)}\n".encode()
                )
            elif stat.S_ISDIR(mode):
                record = f"dir\0{rel}\n".encode()
            elif stat.S_ISLNK(mode):
                record = f"symlink\0{rel}\0{os.readlink(path)}\n".encode()
                unusual.append(f"symlink {rel} -> {os.readlink(path)}")
            else:
                record = f"other\0{rel}\0{stat.S_IFMT(mode):o}\n".encode()
                unusual.append(f"other {rel} {stat.S_IFMT(mode):o}")
            digest.update(record)
            count += 1
        dirnames[:] = [
            name
            for name in sorted(dirnames)
            if not (current / name).is_symlink()
        ]
    return digest.hexdigest(), count, unusual


def compare_trees(left: Path, right: Path) -> list[str]:
    errors: list[str] = []
    left_entries: dict[str, tuple[str, str | None]] = {}
    right_entries: dict[str, tuple[str, str | None]] = {}

    def collect(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            current = Path(dirpath)
            for name in sorted(dirnames + filenames):
                path = current / name
                rel = path.relative_to(root).as_posix()
                mode = path.lstat().st_mode
                if stat.S_ISREG(mode):
                    result[rel] = ("file", sha256_file(path))
                elif stat.S_ISDIR(mode):
                    result[rel] = ("dir", None)
                elif stat.S_ISLNK(mode):
                    result[rel] = ("symlink", os.readlink(path))
                else:
                    result[rel] = ("other", f"{stat.S_IFMT(mode):o}")
            dirnames[:] = [
                name
                for name in sorted(dirnames)
                if not (current / name).is_symlink()
            ]
        return result

    left_entries = collect(left)
    right_entries = collect(right)
    for rel in sorted(set(left_entries) | set(right_entries)):
        if rel not in left_entries:
            errors.append(f"missing from candidate: {rel}")
        elif rel not in right_entries:
            errors.append(f"additional in candidate: {rel}")
        elif left_entries[rel] != right_entries[rel]:
            errors.append(
                f"entry mismatch {rel}: candidate={left_entries[rel]} "
                f"trusted={right_entries[rel]}"
            )
    return errors


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    expected_hashes = audit["hashes"]
    required = {
        "audit-input": Path("/audit-input.json"),
        "audit-campaign-lock": Path("/audit-campaign-lock.json"),
        "run": Path("/run.json"),
        "task": Path("/task.json"),
        "generation-result": Path("/generation-result.json"),
        "invocation": Path("/generation-evidence/invocation.json"),
        "metrics": Path("/generation-evidence/metrics.json"),
        "runtime-metrics": Path("/generation-evidence/runtime-metrics.json"),
        "usage": Path("/generation-evidence/usage.json"),
        "codex-last": Path("/generation-evidence/codex-last.txt"),
        "codex-output": Path("/generation-evidence/codex-output.log"),
        "generation-prompt": Path("/generation-evidence/prompt.txt"),
        "codex-trace": Path("/generation-evidence/codex-trace"),
        "canonical": Path("/reference/canonical.py"),
        "trusted-prompt": Path("/reference/prompt.py"),
        "translator": Path("/reference/py2mpy.py"),
        "trusted-reference-semantics": Path(
            "/reference/reference-semantics"
        ),
        "candidate": Path("/candidate"),
    }
    failures: list[str] = []

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    for name, path in required.items():
        expected_kind = "directory" if name in {
            "codex-trace",
            "trusted-reference-semantics",
            "candidate",
        } else "regular file"
        if not path.exists():
            failures.append(f"missing {name}: {path}")
            print(f"REQUIRED {name}: MISSING")
            continue
        actual_kind = (
            "symlink"
            if path.is_symlink()
            else "directory"
            if path.is_dir()
            else "regular file"
            if path.is_file()
            else "other"
        )
        print(f"REQUIRED {name}: {actual_kind} {path}")
        if actual_kind != expected_kind:
            failures.append(
                f"mistyped {name}: expected {expected_kind}, got {actual_kind}"
            )

    lock_bytes_hash = sha256_file(Path("/audit-campaign-lock.json"))
    print(f"audit_campaign_lock_sha256={lock_bytes_hash}")
    if lock_bytes_hash != expected_hashes["audit_campaign_lock_sha256"]:
        failures.append("campaign-lock byte hash differs from audit-input")
    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    if lock != audit["audit_campaign"]:
        failures.append("campaign-lock JSON differs from audit_campaign block")
    print(f"campaign_lock_json_equal={lock == audit['audit_campaign']}")

    file_expectations = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"):
            "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"):
            "generation_metrics_sha256",
        Path("/generation-evidence/runtime-metrics.json"):
            "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"):
            "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"):
            "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"):
            "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    }
    for path, key in file_expectations.items():
        actual = sha256_file(path)
        expected = expected_hashes[key]
        matched = actual == expected
        print(f"HASH {path}: {actual} expected={expected} match={matched}")
        if not matched:
            failures.append(f"hash mismatch: {path}")

    candidate_prompt_equal = (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"candidate_prompt_byte_equal={candidate_prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not candidate_prompt_equal:
        failures.append("candidate prompt differs from trusted prompt")
    if not translator_equal:
        failures.append("candidate translator differs from trusted translator")

    semantic_errors = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"reference_semantics_tree_difference_count={len(semantic_errors)}")
    for error in semantic_errors:
        print(f"SEMANTICS_DIFFERENCE {error}")
    failures.extend(semantic_errors)

    for path in (
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
        Path("/generation-evidence/codex-trace"),
        Path("/candidate"),
    ):
        digest, count, unusual = tree_digest(path)
        print(
            f"REVIEWER_TREE_DIGEST {path}: sha256={digest} "
            f"entries={count} unusual={len(unusual)}"
        )
        for item in unusual:
            print(f"UNUSUAL_ENTRY {path}: {item}")
        if path in {
            Path("/reference/reference-semantics"),
            Path("/candidate/reference-semantics"),
            Path("/generation-evidence/codex-trace"),
        } and unusual:
            failures.append(f"unusual entries under {path}")

    task_json = json.loads(Path("/task.json").read_text())
    shared_manifest = {
        key: value
        for key, value in audit["manifest"].items()
        if key in task_json
    }
    print(
        "task_json_equals_shared_audit_manifest_fields="
        f"{task_json == shared_manifest}"
    )
    print(
        "audit_derived_manifest_only_keys="
        f"{sorted(set(audit['manifest']) - set(task_json))}"
    )
    if task_json != shared_manifest:
        failures.append(
            "/task.json differs from the corresponding audit-input "
            "manifest fields"
        )

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
