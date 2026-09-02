#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hash(root: Path) -> str:
    """Reproduce the launcher pipeline's length-delimited tree hash."""
    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
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


def load_regular_json(path: Path) -> dict:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise ValueError(f"not a real regular file: {path}")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"not a JSON object: {path}")
    return value


def report_hash(label: str, path: Path, expected: str | None, tree: bool = False) -> bool:
    actual = tree_hash(path) if tree else file_hash(path)
    matches = actual == expected
    print(
        f"HASH {label}: expected={expected} actual={actual} "
        f"match={str(matches).lower()}"
    )
    return matches


def main() -> int:
    document = load_regular_json(AUDIT_INPUT)
    hashes = document["hashes"]
    paths = document["container_paths"]
    result = load_regular_json(Path(paths["stage1_result"]))
    usage = load_regular_json(Path(paths["generation_root"]) / "usage.json")
    failures: list[str] = []

    required_files = {
        "audit-input": AUDIT_INPUT,
        "audit-campaign-lock": Path(paths["audit_campaign_lock"]),
        "run": Path(paths["run_manifest"]),
        "task": Path(paths["task_manifest"]),
        "generation-result": Path(paths["stage1_result"]),
        "invocation": Path(paths["generation_manifest"]),
        "metrics": Path(paths["generation_metrics"]),
        "usage": Path(paths["generation_root"]) / "usage.json",
        "generation-last": Path(paths["generation_last"]),
        "generation-output": Path(paths["generation_output"]),
        "generation-prompt": Path(paths["generation_root"]) / "prompt.txt",
        "trusted-canonical": Path(paths["canonical"]),
        "trusted-prompt": Path(paths["trusted_prompt"]),
        "trusted-translator": Path(paths["translator"]),
        "candidate-prompt": Path(paths["candidate"]) / "prompt.py",
        "candidate-translator": Path(paths["candidate"]) / "py2mpy.py",
    }
    for label, path in required_files.items():
        try:
            mode = path.lstat().st_mode
        except OSError as error:
            failures.append(f"{label} absent/unreadable: {error}")
            continue
        regular = stat.S_ISREG(mode)
        readable = os.access(path, os.R_OK)
        print(f"REQUIRED {label}: path={path} regular={regular} readable={readable}")
        if not regular or not readable:
            failures.append(f"{label} is not a readable regular file")

    required_dirs = {
        "candidate": Path(paths["candidate"]),
        "generation-root": Path(paths["generation_root"]),
        "generation-trace": Path(paths["generation_trace"]),
    }
    for label, path in required_dirs.items():
        try:
            mode = path.lstat().st_mode
        except OSError as error:
            failures.append(f"{label} absent/unreadable: {error}")
            continue
        real_dir = stat.S_ISDIR(mode)
        readable = os.access(path, os.R_OK)
        print(f"REQUIRED {label}: path={path} real_dir={real_dir} readable={readable}")
        if not real_dir or not readable:
            failures.append(f"{label} is not a readable real directory")

    lock = load_regular_json(Path(paths["audit_campaign_lock"]))
    campaign_match = lock == document["audit_campaign"]
    print(f"CAMPAIGN block_equals_lock={campaign_match}")
    if not campaign_match:
        failures.append("campaign lock does not equal audit campaign block")

    checks = [
        report_hash(
            "audit-campaign-lock",
            Path(paths["audit_campaign_lock"]),
            hashes["audit_campaign_lock_sha256"],
        ),
        report_hash(
            "candidate-tree-pipeline",
            Path(paths["candidate"]),
            result["outputs"]["workspace_sha256"],
            tree=True,
        ),
        report_hash("canonical", Path(paths["canonical"]), hashes["canonical_sha256"]),
        report_hash("candidate-prompt", Path(paths["candidate"]) / "prompt.py", hashes["candidate_prompt_sha256"]),
        report_hash("trusted-prompt", Path(paths["trusted_prompt"]), hashes["trusted_prompt_sha256"]),
        report_hash(
            "candidate-translator",
            Path(paths["candidate"]) / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
        report_hash("trusted-translator", Path(paths["translator"]), hashes["trusted_translator_sha256"]),
        report_hash("generation-last", Path(paths["generation_last"]), hashes["generation_codex_last_sha256"]),
        report_hash(
            "generation-output",
            Path(paths["generation_output"]),
            hashes["generation_codex_output_sha256"],
        ),
        report_hash(
            "generation-trace-pipeline",
            Path(paths["generation_trace"]),
            usage["source_trace_sha256"],
            tree=True,
        ),
        report_hash(
            "generation-metrics",
            Path(paths["generation_metrics"]),
            hashes["generation_metrics_sha256"],
        ),
        report_hash(
            "generation-prompt",
            Path(paths["generation_root"]) / "prompt.txt",
            hashes["generation_prompt_sha256"],
        ),
        report_hash(
            "generation-usage",
            Path(paths["generation_root"]) / "usage.json",
            hashes["generation_usage_sha256"],
        ),
        report_hash("run-manifest", Path(paths["run_manifest"]), hashes["run_manifest_sha256"]),
        report_hash("task-manifest", Path(paths["task_manifest"]), hashes["task_manifest_sha256"]),
        report_hash(
            "stage1-invocation",
            Path(paths["generation_manifest"]),
            hashes["stage1_invocation_sha256"],
        ),
        report_hash("stage1-result", Path(paths["stage1_result"]), hashes["stage1_result_sha256"]),
    ]
    if not all(checks):
        failures.append("one or more launcher-recorded hashes mismatch")
    print(
        "AUDIT_TREE_DIGEST_FIELDS "
        f"candidate_tree_sha256={hashes['candidate_tree_sha256']} "
        f"generation_codex_trace_sha256={hashes['generation_codex_trace_sha256']} "
        "(launcher records use a distinct tree-digest encoding; byte integrity "
        "is checked above against the recorded pipeline tree hashes and below "
        "against every recorded member hash)"
    )

    prompt_equal = (
        (Path(paths["candidate"]) / "prompt.py").read_bytes()
        == Path(paths["trusted_prompt"]).read_bytes()
    )
    translator_equal = (
        (Path(paths["candidate"]) / "py2mpy.py").read_bytes()
        == Path(paths["translator"]).read_bytes()
    )
    print(f"BYTE_IDENTITY candidate_prompt_vs_trusted={prompt_equal}")
    print(f"BYTE_IDENTITY candidate_translator_vs_trusted={translator_equal}")
    if not prompt_equal or not translator_equal:
        failures.append("candidate prompt or translator differs from trusted input")

    hidden_semantics = Path("/reference/reference-semantics")
    print(
        "GENERATED_SEMANTICS_BOUNDARY "
        f"trusted_reference_semantics_exists={hidden_semantics.exists()} "
        f"declared_mount={document['mount_reference_semantics']}"
    )
    if hidden_semantics.exists() or document["mount_reference_semantics"]:
        failures.append("generated-semantics boundary contradicted")

    invocation = load_regular_json(Path(paths["generation_manifest"]))
    evidence_root = Path(paths["generation_root"])
    for relative, expected in result["outputs"]["evidence"].items():
        evidence_path = evidence_root / relative
        actual = file_hash(evidence_path)
        match = actual == expected
        print(
            f"RESULT_EVIDENCE {relative}: expected={expected} "
            f"actual={actual} match={str(match).lower()}"
        )
        if not match:
            failures.append(f"generation-result evidence mismatch: {relative}")
    if invocation["outputs"]["evidence"] != result["outputs"]["evidence"]:
        failures.append("invocation/result evidence maps differ")
    print(
        "RECORD_LAYOUT "
        f"value={document['record_layout']} semantics_mode={document['semantics_mode']} "
        f"problem={document['problem_id']} condition={document['condition']}"
    )

    print(f"SUMMARY failures={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
