#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({stat.S_IFMT(mode):o})"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            value = sha256(path) if kind == "file" else None
            if kind == "symlink":
                value = os.readlink(path)
            entries[rel] = (kind, value)
    return entries


def pipeline_tree_sha256(root: Path) -> str:
    """Reproduce the declared pipeline-v3 tree digest algorithm."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in dirs + files:
            path = current_path / name
            kind = entry_kind(path)
            if kind not in {"directory", "file"}:
                raise RuntimeError(f"unsupported tree entry {path}: {kind}")
            entries.append((path.relative_to(root).as_posix(), kind, path))
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def print_hash_check(label: str, path: Path, expected: str) -> None:
    actual = sha256(path)
    print(
        f"HASH {label}: {'MATCH' if actual == expected else 'MISMATCH'} "
        f"expected={expected} actual={actual} path={path}"
    )


def main() -> None:
    record = json.loads(AUDIT_INPUT.read_text())
    hashes = record["hashes"]

    required = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    }

    print("DECLARED record_layout:", record["record_layout"])
    print("DECLARED semantics_mode:", record["semantics_mode"])
    print("DECLARED problem_id:", record["problem_id"])
    print("DECLARED condition:", record["condition"])
    print()

    for key, path in required.items():
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        kind = entry_kind(path) if exists or path.is_symlink() else "missing"
        print(
            f"REQUIRED {key}: exists={exists} readable={readable} "
            f"kind={kind} path={path}"
        )
        if exists and readable and kind == "file":
            print_hash_check(key, path, hashes[key])

    campaign = json.loads(Path("/audit-campaign-lock.json").read_text())
    print()
    print(
        "CAMPAIGN object equality:",
        "MATCH" if campaign == record["audit_campaign"] else "MISMATCH",
    )

    container_paths = record["container_paths"]
    print()
    print("CONTAINER PATH CHECKS")
    for label, raw_path in sorted(container_paths.items()):
        path = Path(raw_path)
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        kind = entry_kind(path) if exists or path.is_symlink() else "missing"
        print(
            f"{label}: exists={exists} readable={readable} "
            f"kind={kind} path={path}"
        )

    required_records = [
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
    print()
    print("PIPELINE-V3 RECORD CHECKS")
    for path in required_records:
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        kind = entry_kind(path) if exists or path.is_symlink() else "missing"
        print(
            f"{path}: exists={exists} readable={readable} kind={kind}"
        )

    trusted_root = Path("/reference/reference-semantics")
    candidate_root = Path("/candidate/reference-semantics")
    trusted = tree_entries(trusted_root)
    candidate = tree_entries(candidate_root)
    all_names = sorted(set(trusted) | set(candidate))
    mismatches = [
        (name, trusted.get(name), candidate.get(name))
        for name in all_names
        if trusted.get(name) != candidate.get(name)
    ]
    print()
    print(
        "REFERENCE SEMANTICS TREE:",
        f"trusted_entries={len(trusted)} candidate_entries={len(candidate)} "
        f"mismatches={len(mismatches)}",
    )
    for name, trusted_value, candidate_value in mismatches:
        print(
            f"TREE MISMATCH {name}: trusted={trusted_value} "
            f"candidate={candidate_value}"
        )
    symlinks = [
        f"{root}:{name}->{value}"
        for root, entries in (("trusted", trusted), ("candidate", candidate))
        for name, (kind, value) in entries.items()
        if kind == "symlink"
    ]
    print("REFERENCE SEMANTICS SYMLINKS:", len(symlinks))
    for item in symlinks:
        print(item)

    prompt_same = (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    translator_same = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print()
    print("CANDIDATE PROMPT BYTE IDENTITY:", prompt_same)
    print("CANDIDATE TRANSLATOR BYTE IDENTITY:", translator_same)

    generation_result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    task = json.loads(Path("/task.json").read_text())
    candidate_pipeline_digest = pipeline_tree_sha256(Path("/candidate"))
    trusted_semantics_pipeline_digest = pipeline_tree_sha256(trusted_root)
    candidate_semantics_pipeline_digest = pipeline_tree_sha256(candidate_root)
    print()
    print(
        "PIPELINE TREE candidate:",
        candidate_pipeline_digest,
        "result_match=",
        candidate_pipeline_digest
        == generation_result["outputs"]["workspace_sha256"],
        "invocation_match=",
        candidate_pipeline_digest == invocation["outputs"]["workspace_sha256"],
    )
    print(
        "PIPELINE TREE trusted semantics:",
        trusted_semantics_pipeline_digest,
        "task_match=",
        trusted_semantics_pipeline_digest
        == task["inputs"]["reference_semantics_sha256"],
        "audit_manifest_match=",
        trusted_semantics_pipeline_digest
        == hashes["trusted_reference_semantics_manifest_sha256"],
    )
    print(
        "PIPELINE TREE candidate semantics:",
        candidate_semantics_pipeline_digest,
        "trusted_match=",
        candidate_semantics_pipeline_digest == trusted_semantics_pipeline_digest,
    )

    trace_root = Path("/generation-evidence/codex-trace")
    trace_entries = tree_entries(trace_root)
    trace_symlinks = [
        (name, value)
        for name, (kind, value) in trace_entries.items()
        if kind == "symlink"
    ]
    trace_files = [
        trace_root / name
        for name, (kind, _) in trace_entries.items()
        if kind == "file"
    ]
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    function_calls: Counter[str] = Counter()
    invalid_json: list[str] = []
    line_count = 0
    first_timestamp = None
    last_timestamp = None
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                line_count += 1
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as err:
                    invalid_json.append(f"{path}:{number}:{err}")
                    continue
                top_types[str(item.get("type"))] += 1
                payload = item.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    if payload.get("type") == "function_call":
                        function_calls[str(payload.get("name"))] += 1
                timestamp = item.get("timestamp")
                if timestamp is not None:
                    first_timestamp = first_timestamp or timestamp
                    last_timestamp = timestamp
    print()
    print(
        "TRACE:",
        f"files={len(trace_files)} entries={len(trace_entries)} "
        f"symlinks={len(trace_symlinks)} lines={line_count} "
        f"invalid_json={len(invalid_json)}",
    )
    print("TRACE timestamps:", first_timestamp, "to", last_timestamp)
    print("TRACE top-level types:", dict(sorted(top_types.items())))
    print("TRACE payload types:", dict(sorted(payload_types.items())))
    print("TRACE function calls:", dict(sorted(function_calls.items())))
    trace_pipeline_digest = pipeline_tree_sha256(trace_root)
    print(
        "TRACE pipeline tree sha256:",
        trace_pipeline_digest,
        "usage_match=",
        trace_pipeline_digest == usage["source_trace_sha256"],
    )
    result_trace_hashes = {
        key: value
        for key, value in generation_result["outputs"]["evidence"].items()
        if key.startswith("codex-trace/")
    }
    for relative, expected in sorted(result_trace_hashes.items()):
        path = Path("/generation-evidence") / relative
        print(
            "TRACE FILE HASH:",
            relative,
            "match=",
            sha256(path) == expected,
            "expected=",
            expected,
            "actual=",
            sha256(path),
        )
    for issue in invalid_json:
        print("TRACE INVALID:", issue)


if __name__ == "__main__":
    main()
