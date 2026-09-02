#!/usr/bin/env python3
"""Independent stage-1 integrity checks for the mounted audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement the pipeline-v2 length-delimited tree hash."""
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
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
    if not path.is_file() or path.is_symlink():
        raise AssertionError(f"missing, linked, or non-regular required file: {path}")
    with path.open("rb") as stream:
        stream.read(1)
    print(f"OK regular readable file: {path}")


def require_directory(path: Path) -> None:
    if not path.is_dir() or path.is_symlink():
        raise AssertionError(f"missing, linked, or non-directory required tree: {path}")
    print(f"OK real directory: {path}")


def check_hash(path: Path, expected: str) -> None:
    actual = sha256_file(path)
    print(f"SHA256 {path}: {actual}")
    if actual != expected:
        raise AssertionError(f"hash mismatch for {path}: expected {expected}")


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    print("record_layout=legacy-selected-stage1")
    print("semantics_mode=GENERATED_SEMANTICS")

    required_files = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    if Path("/generation-evidence/usage.json").exists():
        required_files.append(Path("/generation-evidence/usage.json"))
    required_dirs = [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_dirs:
        require_directory(path)

    lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
    if lock != audit["audit_campaign"]:
        raise AssertionError("campaign lock differs from audit_input.audit_campaign")
    print("OK campaign lock byte-decoded object equals audit_input.audit_campaign")

    hashes = audit["hashes"]
    file_bindings = {
        Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    if Path("/generation-evidence/usage.json").exists():
        file_bindings[Path("/generation-evidence/usage.json")] = (
            "generation_usage_sha256"
        )
    for path, key in file_bindings.items():
        require_regular(path)
        check_hash(path, hashes[key])

    if Path("/candidate/prompt.py").read_bytes() != Path(
        "/reference/prompt.py"
    ).read_bytes():
        raise AssertionError("candidate prompt differs from trusted prompt")
    if Path("/candidate/py2mpy.py").read_bytes() != Path(
        "/reference/py2mpy.py"
    ).read_bytes():
        raise AssertionError("candidate translator differs from trusted translator")
    print("OK candidate prompt is byte-identical to trusted prompt")
    print("OK candidate translator is byte-identical to trusted translator")

    for forbidden in (
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ):
        if forbidden.exists() or forbidden.is_symlink():
            raise AssertionError(f"forbidden generated-mode semantics tree exists: {forbidden}")
    print("OK no reference-semantics tree exists in generated-semantics mode")

    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    output_hashes = invocation["outputs"]["evidence"]
    if output_hashes != result["outputs"]["evidence"]:
        raise AssertionError("invocation/result evidence maps differ")
    for relative, expected in sorted(output_hashes.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        check_hash(path, expected)
    print("OK invocation and result bind the same generation-evidence hashes")

    candidate_tree = pipeline_tree_hash(Path("/candidate"))
    trace_tree = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
    print(f"independent_pipeline_tree_sha256 /candidate: {candidate_tree}")
    print(f"generation recorded workspace_sha256: {invocation['outputs']['workspace_sha256']}")
    if candidate_tree != invocation["outputs"]["workspace_sha256"]:
        raise AssertionError("mounted candidate differs from retained generation workspace")
    usage_path = Path("/generation-evidence/usage.json")
    if usage_path.exists():
        usage = json.loads(usage_path.read_text(encoding="utf-8"))
        print(
            "independent_pipeline_tree_sha256 /generation-evidence/codex-trace: "
            f"{trace_tree}"
        )
        print(f"usage source_trace_sha256: {usage['source_trace_sha256']}")
        if trace_tree != usage["source_trace_sha256"]:
            raise AssertionError("mounted trace tree differs from usage source trace")
    print(f"launcher candidate_tree_sha256 (different declared digest scheme): {hashes['candidate_tree_sha256']}")
    print(
        "launcher generation_codex_trace_sha256 (different declared digest scheme): "
        f"{hashes['generation_codex_trace_sha256']}"
    )

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    if not trace_files:
        raise AssertionError("structured trace has no JSONL files")
    outer_types: collections.Counter[str | None] = collections.Counter()
    payload_types: collections.Counter[str | None] = collections.Counter()
    line_count = 0
    for path in trace_files:
        require_regular(path)
        for line_count, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), line_count + 1
        ):
            record = json.loads(line)
            outer_types[record.get("type")] += 1
            payload = record.get("payload")
            payload_types[
                payload.get("type") if isinstance(payload, dict) else None
            ] += 1
    print(f"structured trace JSONL files={len(trace_files)} records={line_count}")
    print(f"structured trace outer types={dict(outer_types)}")
    print(f"structured trace payload types={dict(payload_types)}")
    print("OK every structured trace record parsed as JSON")

    print("PROVENANCE_CHECK: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"PROVENANCE_CHECK: FAIL: {error}", file=sys.stderr)
        raise
