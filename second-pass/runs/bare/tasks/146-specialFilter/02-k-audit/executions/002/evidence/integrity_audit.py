#!/usr/bin/env python3
"""Independent provenance checks for the 146-specialFilter audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_style_tree_digest(root: Path) -> str:
    """Reimplement /opt/humaneval's content-and-path tree digest."""
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
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    campaign = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))
    hashes = audit["hashes"]
    paths = audit["container_paths"]

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["problem_id"] == "146-specialFilter"
    assert audit["condition"] == "bare"
    assert audit["audit_campaign"] == campaign

    required_files = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        Path(paths["canonical"]),
        Path(paths["trusted_prompt"]),
        Path(paths["translator"]),
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path(paths["generation_root"]) / "prompt.txt",
    ]
    usage = Path(paths["generation_root"]) / "usage.json"
    if usage.exists():
        required_files.append(usage)
    required_dirs = [
        Path(paths["candidate"]),
        Path(paths["generation_root"]),
        Path(paths["generation_trace"]),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_dirs:
        require_directory(path)

    expected_file_hashes = {
        CAMPAIGN_LOCK: hashes["audit_campaign_lock_sha256"],
        Path(paths["canonical"]): hashes["canonical_sha256"],
        Path(paths["trusted_prompt"]): hashes["trusted_prompt_sha256"],
        Path(paths["translator"]): hashes["trusted_translator_sha256"],
        Path(paths["run_manifest"]): hashes["run_manifest_sha256"],
        Path(paths["task_manifest"]): hashes["task_manifest_sha256"],
        Path(paths["stage1_result"]): hashes["stage1_result_sha256"],
        Path(paths["generation_manifest"]): hashes["stage1_invocation_sha256"],
        Path(paths["generation_metrics"]): hashes["generation_metrics_sha256"],
        Path(paths["generation_last"]): hashes["generation_codex_last_sha256"],
        Path(paths["generation_output"]): hashes["generation_codex_output_sha256"],
        Path(paths["generation_root"]) / "prompt.txt": hashes[
            "generation_prompt_sha256"
        ],
        usage: hashes["generation_usage_sha256"],
    }
    for path, expected in expected_file_hashes.items():
        actual = sha256_file(path)
        assert actual == expected, (path, expected, actual)
        print(f"FILE_HASH_OK {actual} {path}")

    candidate = Path(paths["candidate"])
    candidate_prompt = candidate / "prompt.py"
    candidate_translator = candidate / "py2mpy.py"
    require_regular(candidate_prompt)
    require_regular(candidate_translator)
    assert sha256_file(candidate_prompt) == hashes["candidate_prompt_sha256"]
    assert sha256_file(candidate_translator) == hashes["candidate_translator_sha256"]
    assert candidate_prompt.read_bytes() == Path(paths["trusted_prompt"]).read_bytes()
    assert candidate_translator.read_bytes() == Path(paths["translator"]).read_bytes()

    assert not (Path("/reference/reference-semantics").exists())
    assert not (candidate / "reference-semantics").exists()

    result = json.loads(Path(paths["stage1_result"]).read_text(encoding="utf-8"))
    invocation = json.loads(
        Path(paths["generation_manifest"]).read_text(encoding="utf-8")
    )
    evidence_hashes = invocation["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        evidence_path = Path(paths["generation_root"]) / relative
        require_regular(evidence_path)
        actual = sha256_file(evidence_path)
        assert actual == expected, (evidence_path, expected, actual)
        assert result["outputs"]["evidence"][relative] == expected
        print(f"EVIDENCE_HASH_OK {actual} {evidence_path}")

    trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
    jsonl_files = [path for path in trace_files if path.is_file()]
    assert len(jsonl_files) == 1
    rows = [
        json.loads(line)
        for line in jsonl_files[0].read_text(encoding="utf-8").splitlines()
    ]
    assert len(rows) == 286
    assert rows[284]["type"] == "event_msg"

    candidate_digest = pipeline_style_tree_digest(candidate)
    trace_digest = pipeline_style_tree_digest(Path(paths["generation_trace"]))
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    usage_doc = json.loads(usage.read_text(encoding="utf-8"))
    assert trace_digest == usage_doc["source_trace_sha256"]

    print(f"CAMPAIGN_EQUAL {audit['audit_campaign'] == campaign}")
    print(f"CANDIDATE_PIPELINE_TREE {candidate_digest}")
    print(f"CANDIDATE_AUDIT_INPUT_AGGREGATE {hashes['candidate_tree_sha256']}")
    print(f"TRACE_PIPELINE_TREE {trace_digest}")
    print(f"TRACE_AUDIT_INPUT_AGGREGATE {hashes['generation_codex_trace_sha256']}")
    print(f"TRACE_JSONL_ROWS {len(rows)}")
    print("SEMANTICS_BOUNDARY_OK generated semantics; no trusted tree mounted")
    print("INTEGRITY_CHECKS_OK")


if __name__ == "__main__":
    main()
