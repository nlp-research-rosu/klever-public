#!/usr/bin/env python3
"""Independent, read-only provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def tree_records(root: Path) -> list[str]:
    records: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            records.append(f"L\t{rel}\t{os.readlink(path)}")
        elif stat.S_ISDIR(mode):
            records.append(f"D\t{rel}")
        elif stat.S_ISREG(mode):
            records.append(f"F\t{rel}\t{sha256(path)}")
        else:
            records.append(f"O\t{rel}\t{stat.S_IFMT(mode):o}")
    return records


def tree_digest(records: list[str]) -> str:
    payload = "".join(record + "\n" for record in records).encode()
    return hashlib.sha256(payload).hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the pipeline-v3 length/type/size-delimited tree hash."""
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
                raise RuntimeError(f"unsupported tree entry {path}")
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
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    lrecords = tree_records(left)
    rrecords = tree_records(right)
    problems: list[str] = []
    lmap = {record.split("\t", 2)[1]: record for record in lrecords}
    rmap = {record.split("\t", 2)[1]: record for record in rrecords}
    for rel in sorted(lmap.keys() | rmap.keys()):
        if rel not in lmap:
            problems.append(f"missing candidate entry: {rel}")
        elif rel not in rmap:
            problems.append(f"additional candidate entry: {rel}")
        elif lmap[rel] != rmap[rel]:
            problems.append(
                f"changed/type-mismatched candidate entry: {rel}\n"
                f"  candidate={lmap[rel]}\n  trusted={rmap[rel]}"
            )
    return problems


def main() -> int:
    data = json.loads(AUDIT.read_text())
    hashes = data["hashes"]
    required = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }

    failures: list[str] = []
    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")
    for key, path in required.items():
        if not path.exists():
            failures.append(f"missing {path}")
            continue
        if path.is_symlink() or not path.is_file():
            failures.append(f"wrong type or symlink {path}")
            continue
        actual = sha256(path)
        expected = hashes[key]
        ok = actual == expected
        print(f"HASH {path} actual={actual} expected={expected} ok={ok}")
        if not ok:
            failures.append(f"hash mismatch {path}")

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    lock_equal = lock == data["audit_campaign"]
    print(f"CAMPAIGN_OBJECT_MATCH={lock_equal}")
    if not lock_equal:
        failures.append("campaign lock object differs from audit_campaign")

    trace = Path(
        "/generation-evidence/codex-trace/2026/07/29/"
        "rollout-2026-07-29T07-43-15-019fade6-8b81-7002-a3c6-c30d24c4d71e.jsonl"
    )
    result = json.loads(Path("/generation-result.json").read_text())
    trace_rel = str(trace.relative_to("/generation-evidence"))
    expected_trace = result["outputs"]["evidence"][trace_rel]
    actual_trace = sha256(trace)
    trace_ok = actual_trace == expected_trace
    print(
        f"TRACE_FILE_HASH actual={actual_trace} expected={expected_trace} "
        f"ok={trace_ok}"
    )
    if not trace_ok:
        failures.append("structured trace file hash mismatch")

    task = json.loads(Path("/task.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    candidate_pipeline_hash = pipeline_tree_digest(Path("/candidate"))
    expected_workspace_hash = result["outputs"]["workspace_sha256"]
    print(
        f"CANDIDATE_PIPELINE_TREE_HASH actual={candidate_pipeline_hash} "
        f"expected={expected_workspace_hash} "
        f"ok={candidate_pipeline_hash == expected_workspace_hash}"
    )
    if candidate_pipeline_hash != expected_workspace_hash:
        failures.append("candidate tree differs from generation-result workspace")
    semantics_pipeline_hash = pipeline_tree_digest(
        Path("/reference/reference-semantics")
    )
    expected_semantics_hash = task["inputs"]["reference_semantics_sha256"]
    print(
        f"TRUSTED_SEMANTICS_PIPELINE_TREE_HASH actual={semantics_pipeline_hash} "
        f"expected={expected_semantics_hash} "
        f"ok={semantics_pipeline_hash == expected_semantics_hash}"
    )
    if semantics_pipeline_hash != expected_semantics_hash:
        failures.append("trusted supplied semantics differs from task manifest")
    trace_pipeline_hash = pipeline_tree_digest(
        Path("/generation-evidence/codex-trace")
    )
    expected_trace_tree = usage["source_trace_sha256"]
    print(
        f"TRACE_PIPELINE_TREE_HASH actual={trace_pipeline_hash} "
        f"expected={expected_trace_tree} "
        f"ok={trace_pipeline_hash == expected_trace_tree}"
    )
    if trace_pipeline_hash != expected_trace_tree:
        failures.append("structured trace tree differs from usage record")

    for candidate, trusted, label in (
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
            "translator",
        ),
    ):
        equal = candidate.read_bytes() == trusted.read_bytes()
        print(f"{label.upper()}_BYTE_IDENTICAL={equal}")
        if not equal:
            failures.append(f"candidate {label} differs from trusted")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        failures.append("trusted supplied-semantics mount absent/wrong type/symlink")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        failures.append("candidate supplied-semantics tree absent/wrong type/symlink")
    if not failures or (
        trusted_semantics.is_dir() and candidate_semantics.is_dir()
    ):
        candidate_records = tree_records(candidate_semantics)
        trusted_records = tree_records(trusted_semantics)
        print(
            "CANDIDATE_SEMANTICS_INDEPENDENT_DIGEST="
            + tree_digest(candidate_records)
        )
        print(
            "TRUSTED_SEMANTICS_INDEPENDENT_DIGEST="
            + tree_digest(trusted_records)
        )
        problems = compare_trees(candidate_semantics, trusted_semantics)
        print(f"SEMANTICS_ENTRY_COUNT={len(candidate_records)}")
        print(f"SEMANTICS_STRICT_COMPARE_OK={not problems}")
        failures.extend(problems)

    for root in (
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ):
        links = [p for p in root.rglob("*") if p.is_symlink()]
        print(f"SYMLINKS {root} count={len(links)}")
        for link in links:
            print(f"  {link} -> {os.readlink(link)}")

    source_names = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for name in source_names:
        path = Path("/candidate") / name
        if path.is_file() and not path.is_symlink():
            print(f"CANDIDATE_SOURCE_HASH {name} {sha256(path)}")
        else:
            failures.append(f"missing/wrong type/symlink required proof artifact {path}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
