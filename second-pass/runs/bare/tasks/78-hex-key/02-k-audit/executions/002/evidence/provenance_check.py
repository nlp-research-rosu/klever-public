#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Pipeline-v2 tree digest, independently reimplemented."""
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def load_json(path: Path) -> dict:
    require_regular(path)
    value = json.loads(path.read_text())
    assert isinstance(value, dict), f"not a JSON object: {path}"
    return value


def check_hash(label: str, path: Path, expected: str) -> None:
    require_regular(path)
    actual = sha256_file(path)
    result = "OK" if actual == expected else "MISMATCH"
    print(f"{label}: {result} expected={expected} actual={actual} path={path}")
    assert actual == expected


def main() -> None:
    audit = load_json(AUDIT_INPUT)
    lock = load_json(LOCK)

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["problem_id"] == "78-hex-key"
    assert audit["condition"] == "bare"
    assert lock == audit["audit_campaign"]
    print("campaign lock object: OK (exactly equals audit_input.audit_campaign)")

    hashes = audit["hashes"]
    check_hash(
        "audit campaign lock",
        LOCK,
        hashes["audit_campaign_lock_sha256"],
    )

    required_json = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "usage.json",
    ]
    for path in required_json:
        load_json(path)
        print(f"required JSON readable: OK path={path}")

    required_records = [
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
    ]
    for path in required_records:
        require_regular(path)
        print(f"required record regular: OK path={path}")

    require_directory(GENERATION / "codex-trace")
    trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
    for path in trace_files:
        mode = path.lstat().st_mode
        assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), (
            f"linked/unsupported trace entry: {path}"
        )
    trace_jsonl = [p for p in trace_files if p.is_file()]
    assert len(trace_jsonl) == 1
    print(f"structured trace tree types: OK files={len(trace_jsonl)}")

    declared_file_hashes = {
        "canonical_sha256": REFERENCE / "canonical.py",
        "trusted_prompt_sha256": REFERENCE / "prompt.py",
        "trusted_translator_sha256": REFERENCE / "py2mpy.py",
        "candidate_prompt_sha256": CANDIDATE / "prompt.py",
        "candidate_translator_sha256": CANDIDATE / "py2mpy.py",
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": GENERATION / "invocation.json",
        "generation_metrics_sha256": GENERATION / "metrics.json",
        "generation_usage_sha256": GENERATION / "usage.json",
        "generation_codex_last_sha256": GENERATION / "codex-last.txt",
        "generation_codex_output_sha256": GENERATION / "codex-output.log",
        "generation_prompt_sha256": GENERATION / "prompt.txt",
    }
    for key, path in declared_file_hashes.items():
        check_hash(key, path, hashes[key])

    assert (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()
    print("candidate prompt vs trusted prompt: OK byte-identical")
    print("candidate translator vs trusted translator: OK byte-identical")

    assert not (REFERENCE / "reference-semantics").exists()
    assert not (CANDIDATE / "reference-semantics").exists()
    print("generated-semantics mode boundary: OK no reference-semantics tree")

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
        "prompt.py",
        "py2mpy.py",
    ]
    require_directory(CANDIDATE)
    for name in required_candidate:
        require_regular(CANDIDATE / name)
        print(f"candidate artifact regular: OK path=/candidate/{name}")
    for path in CANDIDATE.rglob("*"):
        mode = path.lstat().st_mode
        assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), (
            f"linked/unsupported candidate entry: {path}"
        )
    print("candidate tree types: OK (no symlinks or special entries)")

    generation_result = load_json(Path("/generation-result.json"))
    invocation = load_json(GENERATION / "invocation.json")
    usage = load_json(GENERATION / "usage.json")
    for relative, expected in generation_result["outputs"]["evidence"].items():
        check_hash(
            f"generation-result evidence {relative}",
            GENERATION / relative,
            expected,
        )
    for relative, expected in invocation["outputs"]["evidence"].items():
        check_hash(
            f"invocation evidence {relative}",
            GENERATION / relative,
            expected,
        )

    candidate_digest = sha256_tree(CANDIDATE)
    expected_workspace = generation_result["outputs"]["workspace_sha256"]
    assert candidate_digest == expected_workspace
    assert candidate_digest == invocation["retained_workspace_sha256"]
    print(
        "candidate pipeline tree digest: OK "
        f"expected={expected_workspace} actual={candidate_digest}"
    )

    trace_digest = sha256_tree(GENERATION / "codex-trace")
    assert trace_digest == usage["source_trace_sha256"]
    print(
        "trace pipeline tree digest: OK "
        f"expected={usage['source_trace_sha256']} actual={trace_digest}"
    )

    # These two launcher fields use a launcher-private directory-digest
    # serialization that is not identified in the audit record. Preserve the
    # values alongside independently reproducible per-file and pipeline-v2
    # digests above; do not pretend they were recomputed by another algorithm.
    print(
        "launcher candidate_tree_sha256 (serialization not declared): "
        + hashes["candidate_tree_sha256"]
    )
    print(
        "launcher generation_codex_trace_sha256 "
        "(serialization not declared): "
        + hashes["generation_codex_trace_sha256"]
    )

    trace_path = trace_jsonl[0]
    parsed_lines = 0
    type_counts: dict[str, int] = {}
    for line_number, line in enumerate(trace_path.read_text().splitlines(), 1):
        record = json.loads(line)
        assert isinstance(record, dict)
        parsed_lines += 1
        record_type = str(record.get("type"))
        type_counts[record_type] = type_counts.get(record_type, 0) + 1
    print(
        "structured trace JSONL parse: OK "
        f"lines={parsed_lines} type_counts={json.dumps(type_counts, sort_keys=True)}"
    )
    print("PROVENANCE CHECK COMPLETE")


if __name__ == "__main__":
    main()
