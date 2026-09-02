#!/usr/bin/env python3
"""Independent launcher/candidate integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def path_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def deterministic_tree_hash(root: Path) -> tuple[str, int]:
    """Hash relative names, entry types, permissions, and regular-file bytes."""
    digest = hashlib.sha256()
    count = 0
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        count += 1
        relative = path.relative_to(root).as_posix().encode()
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            kind = b"d"
        elif stat.S_ISREG(info.st_mode):
            kind = b"f"
        elif stat.S_ISLNK(info.st_mode):
            kind = b"l"
        else:
            kind = b"o"
        digest.update(kind + b"\0" + relative + b"\0")
        digest.update(oct(stat.S_IMODE(info.st_mode)).encode() + b"\0")
        if kind == b"f":
            digest.update(bytes.fromhex(sha256(path)))
        elif kind == b"l":
            digest.update(os.readlink(path).encode())
        digest.update(b"\0")
    return digest.hexdigest(), count


def recorded_tree_hash(root: Path) -> str:
    """Reproduce the launcher-declared length/type/size tree encoding."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"unsupported tree entry: {path}")
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


def manifest_tree_hash(root: Path) -> str:
    """Reproduce the audit manifest's relative-path/type/content tree encoding."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def check_regular(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"MISSING: {path}")
        return
    kind = path_kind(path)
    if kind != "file":
        errors.append(f"MISTYPED: {path}: {kind}, expected file")
        return
    try:
        path.open("rb").read(1)
    except OSError as err:
        errors.append(f"UNREADABLE: {path}: {err}")


def check_directory(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"MISSING: {path}")
        return
    kind = path_kind(path)
    if kind != "directory":
        errors.append(f"MISTYPED: {path}: {kind}, expected directory")


def compare_tree(left: Path, right: Path, errors: list[str]) -> None:
    left_entries = {
        p.relative_to(left).as_posix(): p for p in left.rglob("*")
    }
    right_entries = {
        p.relative_to(right).as_posix(): p for p in right.rglob("*")
    }
    for missing in sorted(set(left_entries) - set(right_entries)):
        errors.append(f"SEMANTICS MISSING IN CANDIDATE: {missing}")
    for extra in sorted(set(right_entries) - set(left_entries)):
        errors.append(f"SEMANTICS ADDITIONAL IN CANDIDATE: {extra}")
    for relative in sorted(set(left_entries) & set(right_entries)):
        trusted = left_entries[relative]
        candidate = right_entries[relative]
        trusted_kind = path_kind(trusted)
        candidate_kind = path_kind(candidate)
        if candidate_kind == "symlink":
            errors.append(f"SEMANTICS SYMLINK IN CANDIDATE: {relative}")
        if trusted_kind != candidate_kind:
            errors.append(
                f"SEMANTICS TYPE CHANGE: {relative}: "
                f"trusted={trusted_kind} candidate={candidate_kind}"
            )
        elif trusted_kind == "file" and sha256(trusted) != sha256(candidate):
            errors.append(f"SEMANTICS CONTENT CHANGE: {relative}")


def main() -> int:
    errors: list[str] = []
    check_regular(AUDIT, errors)
    check_regular(LOCK, errors)
    if errors:
        print("\n".join(errors))
        return 1

    audit = load_json(AUDIT)
    lock = load_json(LOCK)
    assert isinstance(audit, dict)
    assert isinstance(lock, dict)

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    print(
        "campaign_block_equals_lock="
        f"{audit.get('audit_campaign') == lock}"
    )
    if audit.get("audit_campaign") != lock:
        errors.append("CAMPAIGN BLOCK DOES NOT MATCH LOCK")

    expected_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "runtime-metrics.json",
        GENERATION / "usage.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
    ]
    expected_directories = [
        CANDIDATE,
        REFERENCE / "reference-semantics",
        GENERATION,
        GENERATION / "codex-trace",
    ]
    for path in expected_files:
        check_regular(path, errors)
    for path in expected_directories:
        check_directory(path, errors)

    container_paths = audit.get("container_paths", {})
    assert isinstance(container_paths, dict)
    for label, raw_path in sorted(container_paths.items()):
        path = Path(str(raw_path))
        if not path.exists():
            errors.append(f"DECLARED MOUNT MISSING: {label}={path}")
        elif path.is_symlink():
            errors.append(f"DECLARED MOUNT SYMLINK: {label}={path}")
        print(f"container_path[{label}]={path} kind={path_kind(path) if path.exists() else 'missing'}")

    hash_expectations = {
        LOCK: "audit_campaign_lock_sha256",
        REFERENCE / "canonical.py": "canonical_sha256",
        REFERENCE / "prompt.py": "trusted_prompt_sha256",
        REFERENCE / "py2mpy.py": "trusted_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        GENERATION / "invocation.json": "stage1_invocation_sha256",
        GENERATION / "metrics.json": "generation_metrics_sha256",
        GENERATION / "runtime-metrics.json": "generation_runtime_metrics_sha256",
        GENERATION / "usage.json": "generation_usage_sha256",
        GENERATION / "codex-last.txt": "generation_codex_last_sha256",
        GENERATION / "codex-output.log": "generation_codex_output_sha256",
        GENERATION / "prompt.txt": "generation_prompt_sha256",
        CANDIDATE / "prompt.py": "candidate_prompt_sha256",
        CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
    }
    recorded_hashes = audit.get("hashes", {})
    assert isinstance(recorded_hashes, dict)
    for path, key in hash_expectations.items():
        check_regular(path, errors)
        if path.exists() and path_kind(path) == "file":
            actual = sha256(path)
            expected = str(recorded_hashes.get(key))
            match = actual == expected
            print(f"sha256 {path} {actual} expected[{key}]={expected} match={match}")
            if not match:
                errors.append(f"HASH MISMATCH: {path} against {key}")

    result = load_json(Path("/generation-result.json"))
    assert isinstance(result, dict)
    evidence_hashes = result.get("outputs", {}).get("evidence", {})
    assert isinstance(evidence_hashes, dict)
    for relative, expected in sorted(evidence_hashes.items()):
        path = GENERATION / relative
        check_regular(path, errors)
        if path.exists() and path_kind(path) == "file":
            actual = sha256(path)
            match = actual == expected
            print(f"result evidence sha256 {relative} {actual} expected={expected} match={match}")
            if not match:
                errors.append(f"GENERATION EVIDENCE HASH MISMATCH: {relative}")

    candidate_prompt = CANDIDATE / "prompt.py"
    candidate_translator = CANDIDATE / "py2mpy.py"
    if candidate_prompt.exists():
        prompt_match = candidate_prompt.read_bytes() == (REFERENCE / "prompt.py").read_bytes()
        print(f"candidate_prompt_byte_identical={prompt_match}")
        if not prompt_match:
            errors.append("CANDIDATE PROMPT DIFFERS FROM TRUSTED PROMPT")
    if candidate_translator.exists():
        translator_match = (
            candidate_translator.read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()
        )
        print(f"candidate_translator_byte_identical={translator_match}")
        if not translator_match:
            errors.append("CANDIDATE TRANSLATOR DIFFERS FROM TRUSTED TRANSLATOR")

    compare_tree(
        REFERENCE / "reference-semantics",
        CANDIDATE / "reference-semantics",
        errors,
    )
    trusted_tree_hash, trusted_count = deterministic_tree_hash(
        REFERENCE / "reference-semantics"
    )
    candidate_sem_hash, candidate_sem_count = deterministic_tree_hash(
        CANDIDATE / "reference-semantics"
    )
    candidate_tree_hash, candidate_count = deterministic_tree_hash(CANDIDATE)
    trace_tree_hash, trace_count = deterministic_tree_hash(GENERATION / "codex-trace")
    print(
        f"independent_tree_sha256 trusted_semantics={trusted_tree_hash} "
        f"entries={trusted_count}"
    )
    print(
        f"independent_tree_sha256 candidate_semantics={candidate_sem_hash} "
        f"entries={candidate_sem_count}"
    )
    print(
        f"independent_tree_sha256 candidate={candidate_tree_hash} "
        f"entries={candidate_count}"
    )
    print(
        f"independent_tree_sha256 generation_trace={trace_tree_hash} "
        f"entries={trace_count}"
    )
    if trusted_tree_hash != candidate_sem_hash:
        errors.append("CANDIDATE SEMANTICS TREE DIFFERS FROM TRUSTED TREE")

    usage = load_json(GENERATION / "usage.json")
    assert isinstance(usage, dict)
    recorded_tree_expectations = [
        (
            CANDIDATE,
            str(result.get("outputs", {}).get("workspace_sha256")),
            "generation-result.outputs.workspace_sha256",
        ),
        (
            CANDIDATE / "reference-semantics",
            str(recorded_hashes.get("trusted_reference_semantics_manifest_sha256")),
            "trusted_reference_semantics_manifest_sha256",
        ),
        (
            REFERENCE / "reference-semantics",
            str(recorded_hashes.get("trusted_reference_semantics_manifest_sha256")),
            "trusted_reference_semantics_manifest_sha256",
        ),
        (
            GENERATION / "codex-trace",
            str(usage.get("source_trace_sha256")),
            "usage.source_trace_sha256",
        ),
    ]
    for path, expected, label in recorded_tree_expectations:
        actual = recorded_tree_hash(path)
        match = actual == expected
        print(
            f"recorded_tree_sha256 {path} {actual} "
            f"expected[{label}]={expected} match={match}"
        )
        if not match:
            errors.append(f"RECORDED TREE HASH MISMATCH: {path} against {label}")

    alternate_tree_records = [
        (CANDIDATE, "candidate_tree_sha256"),
        (
            CANDIDATE / "reference-semantics",
            "candidate_reference_semantics_sha256",
        ),
        (
            REFERENCE / "reference-semantics",
            "trusted_reference_semantics_sha256",
        ),
        (
            GENERATION / "codex-trace",
            "generation_codex_trace_sha256",
        ),
    ]
    for path, key in alternate_tree_records:
        actual = manifest_tree_hash(path)
        recorded = str(recorded_hashes.get(key))
        print(
            f"independent_content_tree_sha256 {path}={actual}; "
            f"alternate_launcher_record[{key}]={recorded}"
        )

    print("trusted semantics regular-file hashes:")
    for path in sorted((REFERENCE / "reference-semantics").rglob("*")):
        if path.is_file() and not path.is_symlink():
            print(f"  {path.relative_to(REFERENCE / 'reference-semantics')} {sha256(path)}")

    print(f"errors={len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
