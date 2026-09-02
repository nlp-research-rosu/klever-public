#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    errors: list[str] = []
    left_entries = {p.relative_to(left): p for p in left.rglob("*")}
    right_entries = {p.relative_to(right): p for p in right.rglob("*")}
    for rel in sorted(left_entries.keys() | right_entries.keys()):
        lp = left_entries.get(rel)
        rp = right_entries.get(rel)
        if lp is None:
            errors.append(f"missing candidate entry: {rel}")
            continue
        if rp is None:
            errors.append(f"additional candidate entry: {rel}")
            continue
        ls = os.lstat(lp)
        rs = os.lstat(rp)
        if stat.S_IFMT(ls.st_mode) != stat.S_IFMT(rs.st_mode):
            errors.append(f"type mismatch: {rel}")
            continue
        if stat.S_ISLNK(ls.st_mode) or stat.S_ISLNK(rs.st_mode):
            errors.append(f"symlink prohibited: {rel}")
            continue
        if stat.S_ISREG(ls.st_mode) and sha256(lp) != sha256(rp):
            errors.append(f"content mismatch: {rel}")
    return errors


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the launcher pipeline's length-delimited tree hash."""
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        mode = os.lstat(path).st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            kind = "directory"
        elif stat.S_ISREG(mode):
            kind = "file"
        else:
            raise ValueError(f"linked or unsupported tree entry: {path}")
        entries.append((relative, kind, path))
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            contents = path.read_bytes()
            digest.update(len(contents).to_bytes(8, "big"))
            digest.update(contents)
    return digest.hexdigest()


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_exact_match={audit['audit_campaign'] == lock}")

    hashes = audit["hashes"]
    checks = {
        "audit_campaign_lock_sha256": LOCK,
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
    }
    failed = False
    for key, path in checks.items():
        actual = sha256(path)
        expected = hashes[key]
        matches = actual == expected
        failed |= not matches
        print(f"{key}: match={matches} actual={actual}")

    trace = Path(
        "/generation-evidence/codex-trace/2026/07/23/"
        "rollout-2026-07-23T00-28-36-019f8d72-7511-7951-be00-bd7479873c9d.jsonl"
    )
    trace_actual = sha256(trace)
    trace_expected = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )["outputs"]["evidence"][str(trace.relative_to("/generation-evidence"))]
    trace_match = trace_actual == trace_expected
    failed |= not trace_match
    print(f"trace_sha256: match={trace_match} actual={trace_actual}")

    prompt_equal = (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    failed |= not prompt_equal or not translator_equal

    tree_errors = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"reference_semantics_tree_errors={len(tree_errors)}")
    for error in tree_errors:
        print(error)
    failed |= bool(tree_errors)

    candidate_tree = pipeline_tree_sha256(Path("/candidate"))
    stage1_workspace = json.loads(Path("/generation-result.json").read_text())[
        "outputs"
    ]["workspace_sha256"]
    candidate_workspace_match = candidate_tree == stage1_workspace
    print(f"candidate_pipeline_tree_sha256={candidate_tree}")
    print(f"candidate_matches_stage1_workspace={candidate_workspace_match}")
    failed |= not candidate_workspace_match

    candidate_semantics_tree = pipeline_tree_sha256(
        Path("/candidate/reference-semantics")
    )
    trusted_semantics_tree = pipeline_tree_sha256(
        Path("/reference/reference-semantics")
    )
    expected_semantics_tree = hashes[
        "trusted_reference_semantics_manifest_sha256"
    ]
    semantics_manifest_match = (
        candidate_semantics_tree
        == trusted_semantics_tree
        == expected_semantics_tree
    )
    print(
        "reference_semantics_pipeline_tree_sha256="
        f"{candidate_semantics_tree}"
    )
    print(f"reference_semantics_manifest_match={semantics_manifest_match}")
    failed |= not semantics_manifest_match

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/usage.json"),
        trace,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    print(f"missing_required_records={missing}")
    failed |= bool(missing)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
