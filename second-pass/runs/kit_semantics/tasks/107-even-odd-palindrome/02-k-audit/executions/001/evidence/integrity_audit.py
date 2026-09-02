#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Reproduce the pipeline-v3 length-delimited tree digest."""
    mode = root.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise ValueError(f"tree root is not a real directory: {root}")
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            child_mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(child_mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(child_mode):
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


def real_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"unsupported:{stat.S_IFMT(mode):o}"


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            rel = path.relative_to(root).as_posix()
            kind = real_kind(path)
            if kind == "directory":
                result[rel] = (kind, None)
                pending.append(path)
            elif kind == "file":
                result[rel] = (kind, sha256_file(path))
            else:
                result[rel] = (kind, None)
    return result


def check_hash(label: str, path: Path, expected: str) -> bool:
    actual = sha256_file(path)
    matched = actual == expected
    print(
        f"HASH {label}: expected={expected} actual={actual} "
        f"match={str(matched).lower()}"
    )
    return matched


def main() -> int:
    document = json.loads(AUDIT.read_text(encoding="utf-8"))
    hashes = document["hashes"]
    paths = document["container_paths"]
    failures: list[str] = []

    print(f"record_layout={document['record_layout']}")
    print(f"semantics_mode={document['semantics_mode']}")
    if document["record_layout"] != "pipeline-v3":
        failures.append("unexpected record layout")
    if document["semantics_mode"] != "SUPPLIED_SEMANTICS":
        failures.append("unexpected semantics mode")

    campaign_path = Path(paths["audit_campaign_lock"])
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    campaign_equal = campaign == document["audit_campaign"]
    print(f"campaign_block_exact_match={str(campaign_equal).lower()}")
    if not campaign_equal:
        failures.append("campaign block mismatch")
    if not check_hash(
        "audit_campaign_lock",
        campaign_path,
        hashes["audit_campaign_lock_sha256"],
    ):
        failures.append("campaign lock hash mismatch")

    required = {
        "audit_input": Path("/audit-input.json"),
        "audit_campaign_lock": campaign_path,
        "run_manifest": Path(paths["run_manifest"]),
        "task_manifest": Path(paths["task_manifest"]),
        "stage1_result": Path(paths["stage1_result"]),
        "stage1_invocation": Path(paths["generation_manifest"]),
        "generation_metrics": Path(paths["generation_metrics"]),
        "generation_runtime_metrics": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage": Path("/generation-evidence/usage.json"),
        "generation_last": Path(paths["generation_last"]),
        "generation_output": Path(paths["generation_output"]),
        "generation_prompt": Path("/generation-evidence/prompt.txt"),
        "generation_trace": Path(paths["generation_trace"]),
        "candidate": Path(paths["candidate"]),
        "canonical": Path(paths["canonical"]),
        "trusted_prompt": Path(paths["trusted_prompt"]),
        "trusted_translator": Path(paths["translator"]),
        "trusted_semantics": Path("/reference/reference-semantics"),
    }
    for label, path in required.items():
        try:
            kind = real_kind(path)
        except OSError as error:
            failures.append(f"{label} absent/unreadable: {error}")
            print(f"REQUIRED {label}: ERROR {error}")
            continue
        expected_kind = "directory" if label in {
            "generation_trace",
            "candidate",
            "trusted_semantics",
        } else "file"
        ok = kind == expected_kind and os.access(path, os.R_OK)
        print(
            f"REQUIRED {label}: path={path} kind={kind} "
            f"readable={str(os.access(path, os.R_OK)).lower()} "
            f"ok={str(ok).lower()}"
        )
        if not ok:
            failures.append(f"{label} has wrong type or is unreadable")

    direct_hashes = [
        ("run_manifest", required["run_manifest"], "run_manifest_sha256"),
        ("task_manifest", required["task_manifest"], "task_manifest_sha256"),
        ("stage1_result", required["stage1_result"], "stage1_result_sha256"),
        ("stage1_invocation", required["stage1_invocation"], "stage1_invocation_sha256"),
        ("generation_metrics", required["generation_metrics"], "generation_metrics_sha256"),
        (
            "generation_runtime_metrics",
            required["generation_runtime_metrics"],
            "generation_runtime_metrics_sha256",
        ),
        ("generation_usage", required["generation_usage"], "generation_usage_sha256"),
        ("generation_last", required["generation_last"], "generation_codex_last_sha256"),
        (
            "generation_output",
            required["generation_output"],
            "generation_codex_output_sha256",
        ),
        ("generation_prompt", required["generation_prompt"], "generation_prompt_sha256"),
        ("canonical", required["canonical"], "canonical_sha256"),
        ("trusted_prompt", required["trusted_prompt"], "trusted_prompt_sha256"),
        ("candidate_prompt", Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        ("trusted_translator", required["trusted_translator"], "trusted_translator_sha256"),
        (
            "candidate_translator",
            Path("/candidate/py2mpy.py"),
            "candidate_translator_sha256",
        ),
    ]
    for label, path, key in direct_hashes:
        if not check_hash(label, path, hashes[key]):
            failures.append(f"{label} hash mismatch")

    result = json.loads(required["stage1_result"].read_text(encoding="utf-8"))
    output_hashes = result["outputs"]["evidence"]
    generation_root = Path(paths["generation_root"])
    for relative, expected in sorted(output_hashes.items()):
        target = generation_root / relative
        actual = (
            sha256_tree(target)
            if target.is_dir() and not target.is_symlink()
            else sha256_file(target)
        )
        ok = actual == expected
        print(
            f"GENERATION_RESULT {relative}: expected={expected} "
            f"actual={actual} match={str(ok).lower()}"
        )
        if not ok:
            failures.append(f"generation-result output mismatch: {relative}")

    candidate_tree = sha256_tree(required["candidate"])
    result_tree = result["outputs"]["workspace_sha256"]
    print(
        f"CANDIDATE_TREE pipeline_digest={candidate_tree} "
        f"generation_result={result_tree} "
        f"match={str(candidate_tree == result_tree).lower()}"
    )
    if candidate_tree != result_tree:
        failures.append("candidate tree differs from stage-1 output digest")

    trace_tree = sha256_tree(required["generation_trace"])
    usage = json.loads(required["generation_usage"].read_text(encoding="utf-8"))
    print(
        f"TRACE_TREE pipeline_digest={trace_tree} "
        f"usage_source_trace={usage['source_trace_sha256']} "
        f"match={str(trace_tree == usage['source_trace_sha256']).lower()}"
    )
    if trace_tree != usage["source_trace_sha256"]:
        failures.append("trace tree differs from usage source digest")

    trusted_manifest = tree_manifest(required["trusted_semantics"])
    candidate_semantics = Path("/candidate/reference-semantics")
    candidate_manifest = tree_manifest(candidate_semantics)
    differences = []
    for rel in sorted(trusted_manifest.keys() | candidate_manifest.keys()):
        trusted_value = trusted_manifest.get(rel)
        candidate_value = candidate_manifest.get(rel)
        if trusted_value != candidate_value:
            differences.append((rel, trusted_value, candidate_value))
    print(
        f"SEMANTICS_COMPARE trusted_entries={len(trusted_manifest)} "
        f"candidate_entries={len(candidate_manifest)} differences={len(differences)}"
    )
    for difference in differences:
        print(f"SEMANTICS_DIFFERENCE {difference!r}")
    if differences:
        failures.append("candidate reference-semantics differs from trusted tree")
    trusted_tree = sha256_tree(required["trusted_semantics"])
    candidate_semantics_tree = sha256_tree(candidate_semantics)
    declared_manifest = hashes["trusted_reference_semantics_manifest_sha256"]
    print(
        f"SEMANTICS_TREE trusted={trusted_tree} candidate={candidate_semantics_tree} "
        f"declared_manifest={declared_manifest}"
    )
    if trusted_tree != declared_manifest or candidate_semantics_tree != trusted_tree:
        failures.append("semantics tree digest mismatch")

    proof_required = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for relative in proof_required:
        target = required["candidate"] / relative
        try:
            kind = real_kind(target)
            ok = kind == "file" and os.access(target, os.R_OK)
        except OSError:
            kind = "missing"
            ok = False
        print(f"PROOF_ARTIFACT {relative}: kind={kind} ok={str(ok).lower()}")
        if not ok:
            failures.append(f"required candidate proof artifact missing: {relative}")

    trace_files = sorted(required["generation_trace"].rglob("*.jsonl"))
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    trace_lines = 0
    malformed = 0
    for trace_path in trace_files:
        with trace_path.open(encoding="utf-8") as stream:
            for raw_line in stream:
                trace_lines += 1
                try:
                    event = json.loads(raw_line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                event_types[str(event.get("type", "<missing>"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type", "<missing>"))] += 1
    print(
        f"TRACE_PARSE files={len(trace_files)} lines={trace_lines} "
        f"malformed={malformed}"
    )
    print(f"TRACE_EVENT_TYPES {dict(sorted(event_types.items()))}")
    print(f"TRACE_PAYLOAD_TYPES {dict(sorted(payload_types.items()))}")
    if not trace_files or malformed:
        failures.append("structured trace absent or malformed")

    generation_output = required["generation_output"].read_text(
        encoding="utf-8", errors="replace"
    )
    print(
        f"GENERATION_OUTPUT chars={len(generation_output)} "
        f"top_markers={generation_output.count('#Top')} "
        f"stuck_markers={generation_output.count('WarnStuckClaimState')} "
        f"result_markers={generation_output.count('RESULT:')}"
    )

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
