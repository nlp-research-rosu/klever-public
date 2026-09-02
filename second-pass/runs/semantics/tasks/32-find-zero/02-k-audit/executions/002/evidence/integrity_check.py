#!/usr/bin/env python3
"""Independent mount, hash, and supplied-semantics integrity checks."""

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


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({stat.S_IFMT(mode):#o})"


def tree_manifest(root: Path) -> tuple[list[str], str]:
    lines: list[str] = []

    def visit(directory: Path) -> None:
        for child in sorted(directory.iterdir(), key=lambda item: item.name):
            relative = child.relative_to(root).as_posix()
            kind = entry_kind(child)
            if kind == "file":
                lines.append(f"file\t{relative}\t{sha256_file(child)}")
            elif kind == "directory":
                lines.append(f"directory\t{relative}\t-")
                visit(child)
            elif kind == "symlink":
                lines.append(f"symlink\t{relative}\t{os.readlink(child)}")
            else:
                lines.append(f"{kind}\t{relative}\t-")

    visit(root)
    rendered = "".join(line + "\n" for line in lines).encode()
    return lines, hashlib.sha256(rendered).hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    left_lines, _ = tree_manifest(left)
    right_lines, _ = tree_manifest(right)
    left_entries = {line.split("\t", 2)[1]: line for line in left_lines}
    right_entries = {line.split("\t", 2)[1]: line for line in right_lines}
    problems: list[str] = []
    for relative in sorted(left_entries.keys() | right_entries.keys()):
        left_entry = left_entries.get(relative)
        right_entry = right_entries.get(relative)
        if left_entry is None:
            problems.append(f"missing from candidate: {relative}")
        elif right_entry is None:
            problems.append(f"additional in candidate: {relative}")
        elif left_entry != right_entry:
            problems.append(
                f"entry mismatch: {relative}\n"
                f"  candidate: {left_entry}\n"
                f"  trusted:   {right_entry}"
            )
    return problems


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    campaign = json.loads(CAMPAIGN_LOCK.read_text())
    print(f"audit-input type: {entry_kind(AUDIT_INPUT)}")
    print(f"campaign-lock type: {entry_kind(CAMPAIGN_LOCK)}")
    print(f"record_layout: {audit['record_layout']}")
    print(f"semantics_mode: {audit['semantics_mode']}")
    print(f"campaign block exact match: {audit['audit_campaign'] == campaign}")

    expected_lock = audit["hashes"]["audit_campaign_lock_sha256"]
    actual_lock = sha256_file(CAMPAIGN_LOCK)
    print(
        "campaign lock sha256: "
        f"actual={actual_lock} expected={expected_lock} match={actual_lock == expected_lock}"
    )

    print("\nLauncher-declared container mounts:")
    for name, raw_path in sorted(audit["container_paths"].items()):
        path = Path(raw_path)
        readable = os.access(path, os.R_OK)
        kind = entry_kind(path) if path.exists() or path.is_symlink() else "missing"
        print(f"{name}: {path} kind={kind} readable={readable}")

    required_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists() or usage.is_symlink():
        required_records.append(usage)
    print("\nRequired legacy-selected-stage1 records:")
    for path in required_records:
        kind = entry_kind(path) if path.exists() or path.is_symlink() else "missing"
        print(f"{path}: kind={kind} readable={os.access(path, os.R_OK)}")

    file_hash_checks = {
        "audit_campaign_lock_sha256": CAMPAIGN_LOCK,
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    }
    print("\nRecorded single-file hash checks:")
    for key, path in file_hash_checks.items():
        expected = audit["hashes"][key]
        actual = sha256_file(path)
        print(f"{key}: actual={actual} expected={expected} match={actual == expected}")

    result = json.loads(Path("/generation-result.json").read_text())
    print("\nGeneration-result evidence hash checks:")
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / relative
        actual = sha256_file(path)
        print(f"{relative}: actual={actual} expected={expected} match={actual == expected}")

    prompt_equal = (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"\ncandidate prompt byte-identical to trusted: {prompt_equal}")
    print(f"candidate translator byte-identical to trusted: {translator_equal}")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    print(
        "trusted supplied-semantics mount: "
        f"kind={entry_kind(trusted_semantics) if trusted_semantics.exists() else 'missing'} "
        f"readable={os.access(trusted_semantics, os.R_OK)}"
    )
    candidate_lines, candidate_manifest_hash = tree_manifest(candidate_semantics)
    trusted_lines, trusted_manifest_hash = tree_manifest(trusted_semantics)
    semantic_problems = compare_trees(candidate_semantics, trusted_semantics)
    print(
        "candidate reference-semantics independent manifest: "
        f"entries={len(candidate_lines)} sha256={candidate_manifest_hash}"
    )
    print(
        "trusted reference-semantics independent manifest: "
        f"entries={len(trusted_lines)} sha256={trusted_manifest_hash}"
    )
    print(f"reference-semantics recursive exact match: {not semantic_problems}")
    for problem in semantic_problems:
        print(f"SEMANTICS INTEGRITY FAILURE: {problem}")

    candidate_lines, candidate_tree_hash = tree_manifest(Path("/candidate"))
    trace_lines, trace_tree_hash = tree_manifest(Path("/generation-evidence/codex-trace"))
    print(
        "\nIndependent tree manifests "
        "(sorted kind/path/content-hash records; independent of launcher encoding):"
    )
    print(f"candidate: entries={len(candidate_lines)} sha256={candidate_tree_hash}")
    print(f"generation trace: entries={len(trace_lines)} sha256={trace_tree_hash}")
    print("candidate non-regular entries:")
    for line in candidate_lines:
        if not line.startswith(("file\t", "directory\t")):
            print(line)
    print("reference-semantics non-regular entries:")
    for line in trusted_lines:
        if not line.startswith(("file\t", "directory\t")):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
