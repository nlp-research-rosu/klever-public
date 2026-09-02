#!/usr/bin/env python3
"""Independent read-only checks of the launcher provenance and mounted inputs."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reviewer_tree_sha256(root: Path) -> str:
    """Path-, kind-, size-, and content-sensitive deterministic tree digest."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise RuntimeError(f"not a real directory: {root}")
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
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


def require_real_file(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"required record is not a regular file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def compare_trees(left: Path, right: Path) -> list[str]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            else:
                result[relative] = ("unsupported", None)
        return result

    li = inventory(left)
    ri = inventory(right)
    problems = []
    for name in sorted(li.keys() | ri.keys()):
        if li.get(name) != ri.get(name):
            problems.append(f"{name}: candidate={li.get(name)} trusted={ri.get(name)}")
    return problems


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_block_equals_lock={audit['audit_campaign'] == lock}")

    required = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    for path in required:
        require_real_file(path)
    print(f"required_regular_readable_files={len(required)}")

    expected_hashes = {
        CAMPAIGN_LOCK: "audit_campaign_lock_sha256",
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
        Path("/generation-evidence/runtime-metrics.json"):
            "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"):
            "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"):
            "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    mismatches = 0
    for path, field in expected_hashes.items():
        actual = sha256_file(path)
        expected = audit["hashes"][field]
        ok = actual == expected
        mismatches += not ok
        print(f"hash {path} {actual} expected_field={field} match={ok}")
    print(f"declared_regular_file_hash_mismatches={mismatches}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    result_evidence = generation_result["outputs"]["evidence"]
    trace_hash_mismatches = 0
    trace_line_count = 0
    trace_type_counts: Counter[str] = Counter()
    response_payload_counts: Counter[str] = Counter()
    for path in trace_files:
        relative = path.relative_to(Path("/generation-evidence")).as_posix()
        actual = sha256_file(path)
        expected = result_evidence.get(relative)
        ok = expected == actual
        trace_hash_mismatches += not ok
        print(f"trace_file {relative} sha256={actual} result_manifest_match={ok}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                item = json.loads(line)
                trace_line_count += 1
                trace_type_counts[item.get("type", "<missing>")] += 1
                if item.get("type") == "response_item":
                    response_payload_counts[
                        item.get("payload", {}).get("type", "<missing>")
                    ] += 1
    print(f"trace_files={len(trace_files)}")
    print(f"trace_lines_valid_json={trace_line_count}")
    print(f"trace_top_level_types={dict(sorted(trace_type_counts.items()))}")
    print(
        "trace_response_payload_types="
        f"{dict(sorted(response_payload_counts.items()))}"
    )
    print(f"trace_result_manifest_hash_mismatches={trace_hash_mismatches}")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise RuntimeError("script is scoped to the declared supplied-semantics mode")
    if not trusted_semantics.is_dir():
        raise RuntimeError("trusted supplied semantics is absent")
    semantic_problems = compare_trees(candidate_semantics, trusted_semantics)
    print(f"semantics_entry_differences={len(semantic_problems)}")
    for problem in semantic_problems:
        print(f"semantics_difference {problem}")

    for root in [
        Path("/candidate"),
        candidate_semantics,
        trusted_semantics,
        trace_root,
    ]:
        print(f"reviewer_tree_sha256 {root} {reviewer_tree_sha256(root)}")
    expected_workspace = generation_result["outputs"]["workspace_sha256"]
    actual_workspace = reviewer_tree_sha256(Path("/candidate"))
    print(f"candidate_matches_stage1_workspace={actual_workspace == expected_workspace}")
    expected_semantics_manifest = audit["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    actual_semantics_manifest = reviewer_tree_sha256(trusted_semantics)
    print(
        "trusted_semantics_manifest_matches="
        f"{actual_semantics_manifest == expected_semantics_manifest}"
    )
    expected_trace_tree = json.loads(
        Path("/generation-evidence/usage.json").read_text()
    )["source_trace_sha256"]
    actual_trace_tree = reviewer_tree_sha256(trace_root)
    print(f"trace_tree_matches_usage={actual_trace_tree == expected_trace_tree}")

    manifest = json.loads(Path("/generation-evidence/invocation.json").read_text())
    manifest_mismatches = 0
    for relative, expected in manifest["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        actual = sha256_file(path)
        ok = actual == expected
        manifest_mismatches += not ok
        print(f"invocation_evidence {relative} match={ok}")
    print(f"invocation_evidence_hash_mismatches={manifest_mismatches}")

    if (
        audit["audit_campaign"] != lock
        or mismatches
        or trace_hash_mismatches
        or semantic_problems
        or manifest_mismatches
        or actual_workspace != expected_workspace
        or actual_semantics_manifest != expected_semantics_manifest
        or actual_trace_tree != expected_trace_tree
    ):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
