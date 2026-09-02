#!/usr/bin/env python3
"""Independent mounted-input, record, and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def entry_map(root: Path) -> dict[str, tuple[str, str]]:
    """Map relative path to (kind, payload/hash), rejecting links distinctly."""
    result: dict[str, tuple[str, str]] = {}
    for base, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        base_path = Path(base)
        names = sorted(dirnames + filenames)
        for name in names:
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
                if name in dirnames:
                    dirnames.remove(name)
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", "")
            elif stat.S_ISREG(mode):
                result[rel] = ("file", file_sha256(path))
            else:
                result[rel] = ("other", oct(mode))
    return result


def check_file(
    label: str,
    path: Path,
    expected: str | None,
    failures: list[str],
) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        failures.append(f"{label}: unreadable or absent: {err}")
        return
    if not stat.S_ISREG(mode):
        failures.append(f"{label}: expected regular file, mode={oct(mode)}")
        return
    actual = file_sha256(path)
    print(f"FILE {label} {path} sha256={actual}")
    if expected is not None and actual != expected:
        failures.append(f"{label}: hash mismatch expected={expected} actual={actual}")


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text())
    hashes = data["hashes"]
    paths = data["container_paths"]
    failures: list[str] = []

    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")

    lock_path = Path(paths["audit_campaign_lock"])
    check_file(
        "audit_campaign_lock",
        lock_path,
        hashes["audit_campaign_lock_sha256"],
        failures,
    )
    if lock_path.is_file():
        lock = json.loads(lock_path.read_text())
        if lock != data["audit_campaign"]:
            failures.append("audit campaign lock JSON differs from audit_input.audit_campaign")
        else:
            print("CAMPAIGN_BLOCK_MATCH=true")

    declared_files = {
        "canonical": (paths["canonical"], hashes["canonical_sha256"]),
        "trusted_prompt": (paths["trusted_prompt"], hashes["trusted_prompt_sha256"]),
        "translator": (paths["translator"], hashes["trusted_translator_sha256"]),
        "run_manifest": (paths["run_manifest"], hashes["run_manifest_sha256"]),
        "task_manifest": (paths["task_manifest"], hashes["task_manifest_sha256"]),
        "stage1_result": (paths["stage1_result"], hashes["stage1_result_sha256"]),
        "generation_manifest": (
            paths["generation_manifest"],
            hashes["stage1_invocation_sha256"],
        ),
        "generation_metrics": (
            paths["generation_metrics"],
            hashes["generation_metrics_sha256"],
        ),
        "generation_last": (
            paths["generation_last"],
            hashes["generation_codex_last_sha256"],
        ),
        "generation_output": (
            paths["generation_output"],
            hashes["generation_codex_output_sha256"],
        ),
    }
    for label, (raw_path, expected) in declared_files.items():
        check_file(label, Path(raw_path), expected, failures)

    generation_root = Path(paths["generation_root"])
    for name, hash_key in (
        ("prompt.txt", "generation_prompt_sha256"),
        ("usage.json", "generation_usage_sha256"),
    ):
        check_file(name, generation_root / name, hashes[hash_key], failures)

    trace_root = Path(paths["generation_trace"])
    trace_entries = entry_map(trace_root)
    trace_files = {
        rel: payload
        for rel, (kind, payload) in trace_entries.items()
        if kind == "file"
    }
    trace_bad = {
        rel: info
        for rel, info in trace_entries.items()
        if info[0] in {"symlink", "other"}
    }
    print(f"TRACE regular_files={len(trace_files)} bad_entries={trace_bad}")
    if len(trace_files) == 0:
        failures.append("structured trace contains no regular files")
    if trace_bad:
        failures.append(f"structured trace has non-regular entries: {trace_bad}")
    for rel, digest in sorted(trace_files.items()):
        print(f"TRACE_FILE {rel} sha256={digest}")
    expected_trace_leaf = json.loads(
        Path(paths["generation_manifest"]).read_text()
    )["outputs"]["evidence"]
    trace_prefix = "codex-trace/"
    expected_trace = {
        key[len(trace_prefix) :]: value
        for key, value in expected_trace_leaf.items()
        if key.startswith(trace_prefix)
    }
    if trace_files != expected_trace:
        failures.append(
            f"structured trace manifest mismatch expected={expected_trace} actual={trace_files}"
        )

    candidate = Path(paths["candidate"])
    candidate_entries = entry_map(candidate)
    bad_candidate = {
        rel: info
        for rel, info in candidate_entries.items()
        if info[0] in {"symlink", "other"}
    }
    print(f"CANDIDATE entries={len(candidate_entries)} bad_entries={bad_candidate}")
    if bad_candidate:
        failures.append(f"candidate has symlink/non-regular entries: {bad_candidate}")

    checks = (
        (
            "candidate prompt",
            candidate / "prompt.py",
            Path(paths["trusted_prompt"]),
            hashes["candidate_prompt_sha256"],
        ),
        (
            "candidate translator",
            candidate / "py2mpy.py",
            Path(paths["translator"]),
            hashes["candidate_translator_sha256"],
        ),
    )
    for label, left, right, recorded in checks:
        left_hash = file_sha256(left)
        right_hash = file_sha256(right)
        print(
            f"IDENTITY {label} left={left_hash} right={right_hash} "
            f"recorded={recorded}"
        )
        if not (left_hash == right_hash == recorded):
            failures.append(f"{label}: candidate/trusted/recorded hashes do not agree")

    candidate_semantics = entry_map(candidate / "reference-semantics")
    trusted_semantics = entry_map(Path("/reference/reference-semantics"))
    print(
        "SEMANTICS_TREE "
        f"candidate_entries={len(candidate_semantics)} "
        f"trusted_entries={len(trusted_semantics)}"
    )
    if candidate_semantics != trusted_semantics:
        all_paths = sorted(set(candidate_semantics) | set(trusted_semantics))
        differences = [
            (
                rel,
                candidate_semantics.get(rel),
                trusted_semantics.get(rel),
            )
            for rel in all_paths
            if candidate_semantics.get(rel) != trusted_semantics.get(rel)
        ]
        failures.append(f"supplied-semantics trees differ: {differences}")
    else:
        print("SEMANTICS_TREE_IDENTITY=true")
    for label, tree in (
        ("candidate", candidate_semantics),
        ("trusted", trusted_semantics),
    ):
        bad = {
            rel: info for rel, info in tree.items() if info[0] in {"symlink", "other"}
        }
        if bad:
            failures.append(f"{label} semantics tree has bad entries: {bad}")

    required_candidate = (
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
        "prompt.py",
        "py2mpy.py",
    )
    for name in required_candidate:
        path = candidate / name
        if not path.is_file() or path.is_symlink():
            failures.append(f"required candidate proof artifact is not a regular file: {path}")

    print("FAILURES_BEGIN")
    for failure in failures:
        print(failure)
    print("FAILURES_END")
    print(f"INTEGRITY_OK={not failures}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
