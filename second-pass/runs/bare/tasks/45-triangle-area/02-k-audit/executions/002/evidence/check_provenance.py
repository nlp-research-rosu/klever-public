#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

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
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def size_tagged_tree_sha256(root: Path) -> str:
    """Reproduce the pipeline-v2 retained-workspace tree digest independently."""
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"not a real regular file: {path}")
    path.open("rb").close()


def require_real_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise RuntimeError(f"not a real directory: {path}")


def report_hash(label: str, path: Path, expected: str | None) -> None:
    actual = sha256_file(path)
    print(f"{label}: {actual}")
    if expected is not None:
        print(f"  expected: {expected}")
        print(f"  match: {actual == expected}")
        if actual != expected:
            raise RuntimeError(f"hash mismatch for {path}")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    paths = audit["container_paths"]
    if audit["record_layout"] != "legacy-selected-stage1":
        raise RuntimeError(f"unexpected record layout: {audit['record_layout']}")
    if audit["semantics_mode"] != "GENERATED_SEMANTICS":
        raise RuntimeError(f"unexpected semantics mode: {audit['semantics_mode']}")

    required_files = {
        "audit input": AUDIT_INPUT,
        "campaign lock": Path(paths["audit_campaign_lock"]),
        "run manifest": Path(paths["run_manifest"]),
        "task manifest": Path(paths["task_manifest"]),
        "generation result": Path(paths["stage1_result"]),
        "generation invocation": Path(paths["generation_manifest"]),
        "generation metrics": Path(paths["generation_metrics"]),
        "generation last": Path(paths["generation_last"]),
        "generation output": Path(paths["generation_output"]),
        "generation prompt": Path(paths["generation_root"]) / "prompt.txt",
        "trusted canonical": Path(paths["canonical"]),
        "trusted prompt": Path(paths["trusted_prompt"]),
        "trusted translator": Path(paths["translator"]),
    }
    usage = Path(paths["generation_root"]) / "usage.json"
    if usage.exists():
        required_files["generation usage"] = usage
    for label, path in required_files.items():
        require_regular(path)
        print(f"regular-readable {label}: {path}")

    required_directories = {
        "candidate": Path(paths["candidate"]),
        "generation root": Path(paths["generation_root"]),
        "generation trace": Path(paths["generation_trace"]),
    }
    for label, path in required_directories.items():
        require_real_directory(path)
        print(f"real-directory {label}: {path}")

    reference_semantics = Path("/reference/reference-semantics")
    print(f"generated-mode reference semantics absent: {not reference_semantics.exists()}")
    if reference_semantics.exists():
        raise RuntimeError("generated mode unexpectedly mounted reference semantics")

    lock = json.loads(Path(paths["audit_campaign_lock"]).read_text())
    print(f"campaign block equals lock: {lock == audit['audit_campaign']}")
    if lock != audit["audit_campaign"]:
        raise RuntimeError("campaign lock does not equal audit campaign block")

    report_hash(
        "campaign lock sha256",
        Path(paths["audit_campaign_lock"]),
        hashes["audit_campaign_lock_sha256"],
    )
    report_hash("run manifest sha256", Path(paths["run_manifest"]), hashes["run_manifest_sha256"])
    report_hash("task manifest sha256", Path(paths["task_manifest"]), hashes["task_manifest_sha256"])
    report_hash("generation result sha256", Path(paths["stage1_result"]), hashes["stage1_result_sha256"])
    report_hash(
        "generation invocation sha256",
        Path(paths["generation_manifest"]),
        hashes["stage1_invocation_sha256"],
    )
    report_hash("generation metrics sha256", Path(paths["generation_metrics"]), hashes["generation_metrics_sha256"])
    report_hash("generation last sha256", Path(paths["generation_last"]), hashes["generation_codex_last_sha256"])
    report_hash("generation output sha256", Path(paths["generation_output"]), hashes["generation_codex_output_sha256"])
    report_hash(
        "generation prompt sha256",
        Path(paths["generation_root"]) / "prompt.txt",
        hashes["generation_prompt_sha256"],
    )
    if usage.exists():
        report_hash("generation usage sha256", usage, hashes["generation_usage_sha256"])
    report_hash("canonical sha256", Path(paths["canonical"]), hashes["canonical_sha256"])
    report_hash("trusted prompt sha256", Path(paths["trusted_prompt"]), hashes["trusted_prompt_sha256"])
    report_hash("trusted translator sha256", Path(paths["translator"]), hashes["trusted_translator_sha256"])
    report_hash(
        "candidate prompt sha256",
        Path(paths["candidate"]) / "prompt.py",
        hashes["candidate_prompt_sha256"],
    )
    report_hash(
        "candidate translator sha256",
        Path(paths["candidate"]) / "py2mpy.py",
        hashes["candidate_translator_sha256"],
    )

    generation_result = json.loads(Path(paths["stage1_result"]).read_text())
    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    candidate_digest = size_tagged_tree_sha256(Path(paths["candidate"]))
    print(f"candidate size-tagged tree sha256: {candidate_digest}")
    print(
        "  matches generation-result retained workspace: "
        f"{candidate_digest == generation_result['outputs']['workspace_sha256']}"
    )
    print(
        "  matches invocation retained workspace: "
        f"{candidate_digest == invocation['retained_workspace_sha256']}"
    )
    if candidate_digest != generation_result["outputs"]["workspace_sha256"]:
        raise RuntimeError("candidate mount differs from generation result workspace digest")
    if candidate_digest != invocation["retained_workspace_sha256"]:
        raise RuntimeError("candidate mount differs from invocation retained workspace digest")

    trace_root = Path(paths["generation_trace"])
    trace_digest = size_tagged_tree_sha256(trace_root)
    usage_doc = json.loads(usage.read_text()) if usage.exists() else {}
    print(f"trace size-tagged tree sha256: {trace_digest}")
    print(
        "  matches usage source trace: "
        f"{trace_digest == usage_doc.get('source_trace_sha256')}"
    )
    if usage.exists() and trace_digest != usage_doc["source_trace_sha256"]:
        raise RuntimeError("trace mount differs from usage source trace digest")

    evidence_map = generation_result["outputs"]["evidence"]
    evidence_root = Path(paths["generation_root"])
    for relative, expected in sorted(evidence_map.items()):
        evidence_path = evidence_root / relative
        require_regular(evidence_path)
        actual = sha256_file(evidence_path)
        print(f"generation-result evidence {relative}: {actual} match={actual == expected}")
        if actual != expected:
            raise RuntimeError(f"generation evidence mismatch: {relative}")

    trace_files = sorted(trace_root.rglob("*"))
    for path in trace_files:
        mode = path.lstat().st_mode
        if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
            raise RuntimeError(f"trace has linked or unsupported entry: {path}")
    jsonl_files = [path for path in trace_files if path.is_file()]
    line_count = 0
    for path in jsonl_files:
        with path.open() as stream:
            for line in stream:
                json.loads(line)
                line_count += 1
    print(f"trace JSONL files: {len(jsonl_files)}")
    print(f"trace valid JSON records: {line_count}")

    print("integrity fields:")
    for key, value in sorted(audit["integrity"].items()):
        print(f"  {key}: {value}")
    if not all(value is True or value is None for value in audit["integrity"].values()):
        raise RuntimeError("launcher integrity field records failure")


if __name__ == "__main__":
    main()
