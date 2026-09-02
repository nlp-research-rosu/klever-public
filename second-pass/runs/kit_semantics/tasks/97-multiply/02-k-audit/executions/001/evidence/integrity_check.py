#!/usr/bin/env python3
"""Independent provenance and mounted-tree integrity checks for this audit."""

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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def regular_file(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode)


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError(f"tree root is not a real directory: {root}")
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
            elif stat.S_ISLNK(mode):
                entries.append((relative, "symlink", path))
            else:
                entries.append((relative, f"mode:{mode:o}", path))
    return sorted(entries)


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        if kind not in ("directory", "file"):
            raise RuntimeError(f"unsupported tree entry: {root / relative} ({kind})")
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    problems: list[str] = []
    left_entries = {relative: (kind, path) for relative, kind, path in tree_entries(left)}
    right_entries = {
        relative: (kind, path) for relative, kind, path in tree_entries(right)
    }
    for relative in sorted(left_entries.keys() | right_entries.keys()):
        if relative not in left_entries:
            problems.append(f"missing-left:{relative}")
            continue
        if relative not in right_entries:
            problems.append(f"missing-right:{relative}")
            continue
        left_kind, left_path = left_entries[relative]
        right_kind, right_path = right_entries[relative]
        if left_kind != right_kind:
            problems.append(f"type:{relative}:{left_kind}!={right_kind}")
        elif left_kind == "file" and left_path.read_bytes() != right_path.read_bytes():
            problems.append(f"content:{relative}")
    return problems


def report_hash(label: str, path: Path, expected: str | None = None) -> None:
    actual = sha256_file(path)
    status = "OK" if expected is None or actual == expected else "MISMATCH"
    print(f"FILE {label}: regular={regular_file(path)} sha256={actual} {status}")


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    print(
        "AUDIT INPUT:",
        f"regular={regular_file(AUDIT_INPUT)}",
        f"layout={audit['record_layout']}",
        f"mode={audit['semantics_mode']}",
        f"problem={audit['problem_id']}",
    )

    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    report_hash("campaign-lock", lock_path, hashes["audit_campaign_lock_sha256"])
    lock = json.loads(lock_path.read_text())
    print("CAMPAIGN JSON EQUALITY:", lock == audit["audit_campaign"])

    file_checks = [
        ("canonical", Path("/reference/canonical.py"), "canonical_sha256"),
        ("trusted-prompt", Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        ("trusted-translator", Path("/reference/py2mpy.py"), "trusted_translator_sha256"),
        ("candidate-prompt", Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        (
            "candidate-translator",
            Path("/candidate/py2mpy.py"),
            "candidate_translator_sha256",
        ),
        ("run", Path("/run.json"), "run_manifest_sha256"),
        ("task", Path("/task.json"), "task_manifest_sha256"),
        ("generation-result", Path("/generation-result.json"), "stage1_result_sha256"),
        (
            "invocation",
            Path("/generation-evidence/invocation.json"),
            "stage1_invocation_sha256",
        ),
        (
            "metrics",
            Path("/generation-evidence/metrics.json"),
            "generation_metrics_sha256",
        ),
        (
            "runtime-metrics",
            Path("/generation-evidence/runtime-metrics.json"),
            "generation_runtime_metrics_sha256",
        ),
        (
            "usage",
            Path("/generation-evidence/usage.json"),
            "generation_usage_sha256",
        ),
        (
            "codex-last",
            Path("/generation-evidence/codex-last.txt"),
            "generation_codex_last_sha256",
        ),
        (
            "codex-output",
            Path("/generation-evidence/codex-output.log"),
            "generation_codex_output_sha256",
        ),
        (
            "generation-prompt",
            Path("/generation-evidence/prompt.txt"),
            "generation_prompt_sha256",
        ),
    ]
    file_hashes_ok = True
    for label, path, hash_key in file_checks:
        report_hash(label, path, hashes[hash_key])
        file_hashes_ok = file_hashes_ok and (
            regular_file(path) and sha256_file(path) == hashes[hash_key]
        )

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics_digest = tree_digest(candidate_semantics)
    trusted_semantics_digest = tree_digest(trusted_semantics)
    print(
        "CANDIDATE SEMANTICS PIPELINE TREE:",
        f"sha256={candidate_semantics_digest}",
        "OK"
        if candidate_semantics_digest
        == hashes["trusted_reference_semantics_manifest_sha256"]
        else "MISMATCH",
    )
    print(
        "TRUSTED SEMANTICS PIPELINE TREE:",
        f"sha256={trusted_semantics_digest}",
        "OK"
        if trusted_semantics_digest
        == hashes["trusted_reference_semantics_manifest_sha256"]
        else "MISMATCH",
    )
    print(
        "AUDIT-RECORDED SEMANTICS CONTENT DIGEST PAIR:",
        f"candidate={hashes['candidate_reference_semantics_sha256']}",
        f"trusted={hashes['trusted_reference_semantics_sha256']}",
        "OK"
        if hashes["candidate_reference_semantics_sha256"]
        == hashes["trusted_reference_semantics_sha256"]
        else "MISMATCH",
    )
    semantics_problems = compare_trees(candidate_semantics, trusted_semantics)
    print("SEMANTICS ENTRY COUNT:", len(tree_entries(candidate_semantics)))
    print("SEMANTICS TREE COMPARISON:", semantics_problems or "IDENTICAL")

    candidate_digest = tree_digest(Path("/candidate"))
    generation_result = json.loads(Path("/generation-result.json").read_text())
    print(
        "CANDIDATE PIPELINE TREE:",
        f"sha256={candidate_digest}",
        "OK"
        if candidate_digest == generation_result["outputs"]["workspace_sha256"]
        else "MISMATCH",
    )
    print("AUDIT-RECORDED CANDIDATE CONTENT DIGEST:", hashes["candidate_tree_sha256"])

    trace_root = Path("/generation-evidence/codex-trace")
    trace_digest = tree_digest(trace_root)
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    print(
        "TRACE PIPELINE TREE:",
        f"sha256={trace_digest}",
        "OK" if trace_digest == usage["source_trace_sha256"] else "MISMATCH",
    )
    print(
        "AUDIT-RECORDED TRACE CONTENT DIGEST:",
        hashes["generation_codex_trace_sha256"],
    )
    trace_files = [
        path
        for relative, kind, path in tree_entries(trace_root)
        if kind == "file" and relative.endswith(".jsonl")
    ]
    print("TRACE JSONL COUNT:", len(trace_files))
    output_hashes = generation_result["outputs"]["evidence"]
    evidence_root = Path("/generation-evidence")
    declared_outputs_ok = True
    for relative, expected in sorted(output_hashes.items()):
        report_hash(f"declared-output:{relative}", evidence_root / relative, expected)
        path = evidence_root / relative
        declared_outputs_ok = declared_outputs_ok and (
            regular_file(path) and sha256_file(path) == expected
        )

    required_proof = (
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    )
    for relative in required_proof:
        path = Path("/candidate") / relative
        print(f"REQUIRED PROOF {relative}: regular={regular_file(path)}")

    all_required_regular = all(
        regular_file(path)
        for _, path, _ in file_checks
    ) and all(regular_file(Path("/candidate") / name) for name in required_proof)
    all_ok = (
        lock == audit["audit_campaign"]
        and candidate_semantics_digest
        == hashes["trusted_reference_semantics_manifest_sha256"]
        and trusted_semantics_digest
        == hashes["trusted_reference_semantics_manifest_sha256"]
        and hashes["candidate_reference_semantics_sha256"]
        == hashes["trusted_reference_semantics_sha256"]
        and not semantics_problems
        and candidate_digest == generation_result["outputs"]["workspace_sha256"]
        and trace_digest == usage["source_trace_sha256"]
        and all_required_regular
        and file_hashes_ok
        and declared_outputs_ok
    )
    print("OVERALL:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
