#!/usr/bin/env python3
"""Independent, read-only provenance checks for audit stage 1."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path
import sys


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require_regular(path: Path) -> None:
    if path.is_symlink():
        raise AssertionError(f"required path is a symlink: {path}")
    if not path.is_file():
        raise AssertionError(f"required regular file missing/mistyped: {path}")
    print(f"REGULAR {path} size={path.stat().st_size}")


def digest_manifest(root: Path) -> tuple[str, list[tuple[str, str]]]:
    rows: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise AssertionError(f"symlink below {root}: {path}")
        if path.is_file():
            rows.append((path.relative_to(root).as_posix(), sha256(path)))
        elif not path.is_dir():
            raise AssertionError(f"special entry below {root}: {path}")
    payload = "".join(f"{name}\t{digest}\n" for name, digest in rows).encode()
    return hashlib.sha256(payload).hexdigest(), rows


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the mounted pipeline_contract.sha256_tree algorithm."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if child.is_symlink():
                raise AssertionError(f"symlink below {root}: {path}")
            if child.is_dir(follow_symlinks=False):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif child.is_file(follow_symlinks=False):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"special entry below {root}: {path} mode={mode:o}")
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


def main() -> int:
    require_regular(AUDIT_INPUT)
    require_regular(CAMPAIGN_LOCK)
    data = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())

    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")
    assert data["record_layout"] == "legacy-selected-stage1"
    assert data["semantics_mode"] == "GENERATED_SEMANTICS"
    assert lock == data["audit_campaign"]
    print("CAMPAIGN_JSON_MATCH true")

    actual_lock_hash = sha256(CAMPAIGN_LOCK)
    expected_lock_hash = data["hashes"]["audit_campaign_lock_sha256"]
    print(f"HASH {CAMPAIGN_LOCK} actual={actual_lock_hash} expected={expected_lock_hash}")
    assert actual_lock_hash == expected_lock_hash

    paths = data["container_paths"]
    required = [
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path(paths["generation_root"]) / "prompt.txt",
        Path(paths["canonical"]),
        Path(paths["trusted_prompt"]),
        Path(paths["translator"]),
    ]
    usage = Path(paths["generation_root"]) / "usage.json"
    if usage.exists() or usage.is_symlink():
        required.append(usage)
    for path in required:
        require_regular(path)

    trace_root = Path(paths["generation_trace"])
    if trace_root.is_symlink() or not trace_root.is_dir():
        raise AssertionError(f"trace root missing/mistyped/symlinked: {trace_root}")
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    if not trace_files:
        raise AssertionError("structured trace contains no JSONL file")
    for path in trace_files:
        require_regular(path)

    expected_hashes = {
        Path(paths["run_manifest"]): data["hashes"]["run_manifest_sha256"],
        Path(paths["task_manifest"]): data["hashes"]["task_manifest_sha256"],
        Path(paths["stage1_result"]): data["hashes"]["stage1_result_sha256"],
        Path(paths["generation_manifest"]): data["hashes"]["stage1_invocation_sha256"],
        Path(paths["generation_metrics"]): data["hashes"]["generation_metrics_sha256"],
        Path(paths["generation_last"]): data["hashes"]["generation_codex_last_sha256"],
        Path(paths["generation_output"]): data["hashes"]["generation_codex_output_sha256"],
        Path(paths["generation_root"]) / "prompt.txt": data["hashes"]["generation_prompt_sha256"],
        Path(paths["canonical"]): data["hashes"]["canonical_sha256"],
        Path(paths["trusted_prompt"]): data["hashes"]["trusted_prompt_sha256"],
        Path(paths["translator"]): data["hashes"]["trusted_translator_sha256"],
    }
    if usage in required:
        expected_hashes[usage] = data["hashes"]["generation_usage_sha256"]
    for path, expected in expected_hashes.items():
        actual = sha256(path)
        print(f"HASH {path} actual={actual} expected={expected}")
        assert actual == expected

    candidate = Path(paths["candidate"])
    if candidate.is_symlink() or not candidate.is_dir():
        raise AssertionError(f"candidate mount missing/mistyped/symlinked: {candidate}")
    for name in (
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ):
        require_regular(candidate / name)
    assert (candidate / "prompt.py").read_bytes() == Path(paths["trusted_prompt"]).read_bytes()
    assert (candidate / "py2mpy.py").read_bytes() == Path(paths["translator"]).read_bytes()
    print("CANDIDATE_PROMPT_BYTE_MATCH true")
    print("CANDIDATE_TRANSLATOR_BYTE_MATCH true")

    forbidden_reference_semantics = Path("/reference/reference-semantics")
    assert not forbidden_reference_semantics.exists()
    assert not forbidden_reference_semantics.is_symlink()
    print("GENERATED_MODE_REFERENCE_SEMANTICS_ABSENT true")

    result = json.loads(Path(paths["stage1_result"]).read_text())
    evidence_root = Path(paths["generation_root"])
    for rel_name, expected in sorted(result["outputs"]["evidence"].items()):
        path = evidence_root / rel_name
        require_regular(path)
        actual = sha256(path)
        print(f"RESULT_HASH {rel_name} actual={actual} expected={expected}")
        assert actual == expected

    candidate_pipeline_hash = pipeline_tree_digest(candidate)
    expected_workspace_hash = result["outputs"]["workspace_sha256"]
    print(
        "CANDIDATE_PIPELINE_TREE_SHA256 "
        f"actual={candidate_pipeline_hash} expected_generation_workspace={expected_workspace_hash}"
    )
    assert candidate_pipeline_hash == expected_workspace_hash
    if usage in required:
        usage_document = json.loads(usage.read_text())
        trace_pipeline_hash = pipeline_tree_digest(trace_root)
        expected_source_trace_hash = usage_document["source_trace_sha256"]
        print(
            "TRACE_PIPELINE_TREE_SHA256 "
            f"actual={trace_pipeline_hash} expected_usage_source_trace={expected_source_trace_hash}"
        )
        assert trace_pipeline_hash == expected_source_trace_hash

    event_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    trace_lines = 0
    for path in trace_files:
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                trace_lines += 1
                event_counts[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_counts[str(payload.get("type"))] += 1
    print(f"TRACE_JSON_VALID files={len(trace_files)} lines={trace_lines}")
    print(f"TRACE_EVENT_COUNTS {dict(sorted(event_counts.items()))}")
    print(f"TRACE_PAYLOAD_COUNTS {dict(sorted(payload_counts.items()))}")

    candidate_digest, candidate_rows = digest_manifest(candidate)
    print(
        "CANDIDATE_INDEPENDENT_MANIFEST_SHA256 "
        f"{candidate_digest} launcher_tree_claim={data['hashes']['candidate_tree_sha256']}"
    )
    for name, digest in candidate_rows:
        print(f"CANDIDATE_FILE {digest} {name}")
    trace_digest, trace_rows = digest_manifest(trace_root)
    print(
        "TRACE_INDEPENDENT_MANIFEST_SHA256 "
        f"{trace_digest} launcher_tree_claim={data['hashes']['generation_codex_trace_sha256']}"
    )
    for name, digest in trace_rows:
        print(f"TRACE_FILE {digest} {name}")

    # Explicitly show that launcher host paths were not used.
    for key in ("candidate", "canonical", "translator", "trusted_prompt"):
        print(f"HOST_PROVENANCE_IGNORED {key}={data[key]}")
    print("PROVENANCE_CHECK PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as err:
        print(f"PROVENANCE_CHECK FAIL: {type(err).__name__}: {err}", file=sys.stderr)
        raise
