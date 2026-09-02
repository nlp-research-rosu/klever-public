#!/usr/bin/env python3
"""Independent Stage-1 provenance and mount-integrity audit."""

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


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement /opt/humaneval/tools/pipeline_contract.py::sha256_tree."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            mode = child.stat(follow_symlinks=False).st_mode
            path = Path(child.path)
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
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required record is not a real regular file: {path}"
    assert os.access(path, os.R_OK), f"required record is unreadable: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"required mount is not a real directory: {path}"
    assert os.access(path, os.R_OK | os.X_OK), f"required directory is unreadable: {path}"


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    paths = audit["container_paths"]

    required_files = [
        Path("/audit-input.json"),
        Path(paths["audit_campaign_lock"]),
        Path(paths["canonical"]),
        Path(paths["translator"]),
        Path(paths["trusted_prompt"]),
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path(paths["generation_root"]) / "prompt.txt",
    ]
    # usage.json is optional for this legacy-selected-stage1 layout, but present.
    usage = Path(paths["generation_root"]) / "usage.json"
    if usage.exists():
        required_files.append(usage)
    required_directories = [
        Path(paths["candidate"]),
        Path(paths["generation_root"]),
        Path(paths["generation_trace"]),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_directories:
        require_directory(path)
    for artifact in (
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ):
        require_regular(Path(paths["candidate"]) / artifact)
    print("required candidate proof artifacts are real readable files: true")

    hidden_semantics = Path("/reference/reference-semantics")
    assert not hidden_semantics.exists() and not hidden_semantics.is_symlink()

    campaign = json.loads(Path(paths["audit_campaign_lock"]).read_text())
    assert campaign == audit["audit_campaign"]

    expected = audit["hashes"]
    file_checks = {
        "audit_campaign_lock_sha256": Path(paths["audit_campaign_lock"]),
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
        "candidate_prompt_sha256": Path(paths["candidate"]) / "prompt.py",
        "candidate_translator_sha256": Path(paths["candidate"]) / "py2mpy.py",
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
        "generation_usage_sha256": usage,
    }
    print("FILE DIGEST CHECKS")
    for key, path in file_checks.items():
        actual = sha256_file(path)
        recorded = expected[key]
        print(f"{key}: recorded={recorded} actual={actual} match={actual == recorded}")
        assert actual == recorded

    candidate_prompt = Path(paths["candidate"]) / "prompt.py"
    candidate_translator = Path(paths["candidate"]) / "py2mpy.py"
    assert candidate_prompt.read_bytes() == Path(paths["trusted_prompt"]).read_bytes()
    assert candidate_translator.read_bytes() == Path(paths["translator"]).read_bytes()
    print("candidate prompt byte-identical to trusted prompt: true")
    print("candidate translator byte-identical to trusted translator: true")
    print("campaign block byte-equal as parsed JSON to campaign lock: true")
    print("generated-semantics boundary (trusted semantics absent): true")

    generation = json.loads(Path("/generation-result.json").read_text())
    candidate_tree = pipeline_tree_hash(Path(paths["candidate"]))
    trace_tree = pipeline_tree_hash(Path(paths["generation_trace"]))
    print("PIPELINE TREE DIGESTS")
    print(f"candidate pipeline tree digest: {candidate_tree}")
    print(
        "candidate matches Stage-1 retained workspace digest: "
        f"{candidate_tree == generation['outputs']['workspace_sha256']}"
    )
    print(f"trace pipeline tree digest: {trace_tree}")
    if usage.exists():
        usage_doc = json.loads(usage.read_text())
        print(
            "trace matches usage source_trace_sha256: "
            f"{trace_tree == usage_doc['source_trace_sha256']}"
        )
    assert candidate_tree == generation["outputs"]["workspace_sha256"]
    assert candidate_tree == json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )["retained_workspace_sha256"]

    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    for relative, recorded in invocation["outputs"]["evidence"].items():
        evidence_path = Path("/generation-evidence") / relative
        require_regular(evidence_path)
        actual = sha256_file(evidence_path)
        print(
            f"invocation evidence {relative}: recorded={recorded} "
            f"actual={actual} match={recorded == actual}"
        )
        assert recorded == actual

    trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
    jsonl_files = [path for path in trace_files if path.is_file()]
    assert jsonl_files
    parsed_lines = 0
    for path in jsonl_files:
        require_regular(path)
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as error:
                raise AssertionError(f"bad JSONL {path}:{line_number}: {error}") from error
            parsed_lines += 1
    print(f"structured trace files parsed: {len(jsonl_files)}")
    print(f"structured trace JSON events parsed: {parsed_lines}")
    print("STAGE1_INTEGRITY_OK")


if __name__ == "__main__":
    main()
