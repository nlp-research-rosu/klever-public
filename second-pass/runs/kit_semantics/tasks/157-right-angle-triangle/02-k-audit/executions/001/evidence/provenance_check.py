#!/usr/bin/env python3
"""Independent provenance/integrity checks for the audit mounts."""

from __future__ import annotations

import collections
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode) or stat.S_ISLNK(mode):
        raise AssertionError(f"not a non-symlink regular file: {path}")


def tree_manifest(root: Path) -> tuple[list[tuple[str, str, str]], str]:
    entries: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries.append(("symlink", rel, os.readlink(path)))
        elif stat.S_ISDIR(mode):
            entries.append(("directory", rel, ""))
        elif stat.S_ISREG(mode):
            entries.append(("file", rel, sha256_file(path)))
        else:
            entries.append(("other", rel, oct(mode)))
    encoded = "".join("\0".join(entry) + "\n" for entry in entries).encode()
    return entries, hashlib.sha256(encoded).hexdigest()


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    required = [
        AUDIT_INPUT,
        paths["audit_campaign_lock"],
        paths["run_manifest"],
        paths["task_manifest"],
        paths["stage1_result"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        paths["generation_last"],
        paths["generation_output"],
        Path("/generation-evidence/prompt.txt"),
        paths["canonical"],
        paths["trusted_prompt"],
        paths["translator"],
    ]
    trace_files = sorted(paths["generation_trace"].rglob("*.jsonl"))
    assert trace_files, "structured trace is missing"
    required.extend(trace_files)
    for path in required:
        require_regular(path)

    direct_hashes = {
        "audit_campaign_lock_sha256": paths["audit_campaign_lock"],
        "run_manifest_sha256": paths["run_manifest"],
        "task_manifest_sha256": paths["task_manifest"],
        "stage1_result_sha256": paths["stage1_result"],
        "stage1_invocation_sha256": paths["generation_manifest"],
        "generation_metrics_sha256": paths["generation_metrics"],
        "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": paths["generation_last"],
        "generation_codex_output_sha256": paths["generation_output"],
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "canonical_sha256": paths["canonical"],
        "trusted_prompt_sha256": paths["trusted_prompt"],
        "trusted_translator_sha256": paths["translator"],
        "candidate_prompt_sha256": paths["candidate"] / "prompt.py",
        "candidate_translator_sha256": paths["candidate"] / "py2mpy.py",
    }
    for field, path in direct_hashes.items():
        require_regular(path)
        actual = sha256_file(path)
        expected = audit["hashes"][field]
        print(f"HASH {field} expected={expected} actual={actual} match={actual == expected}")
        assert actual == expected

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    print(f"CAMPAIGN lock_equals_audit_block={lock == audit['audit_campaign']}")
    assert lock == audit["audit_campaign"]

    stage1 = json.loads(paths["stage1_result"].read_text())
    invocation = json.loads(paths["generation_manifest"].read_text())
    for record_name, record in (("stage1_result", stage1), ("invocation", invocation)):
        for rel, expected in record["outputs"]["evidence"].items():
            path = Path("/generation-evidence") / rel
            require_regular(path)
            actual = sha256_file(path)
            print(
                f"EVIDENCE {record_name} {rel} expected={expected} "
                f"actual={actual} match={actual == expected}"
            )
            assert actual == expected

    candidate_prompt = paths["candidate"] / "prompt.py"
    candidate_translator = paths["candidate"] / "py2mpy.py"
    assert candidate_prompt.read_bytes() == paths["trusted_prompt"].read_bytes()
    assert candidate_translator.read_bytes() == paths["translator"].read_bytes()
    print("COPY prompt candidate_vs_trusted=IDENTICAL")
    print("COPY translator candidate_vs_trusted=IDENTICAL")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = paths["candidate"] / "reference-semantics"
    assert trusted_semantics.is_dir()
    assert candidate_semantics.is_dir()
    trusted_entries, trusted_digest = tree_manifest(trusted_semantics)
    candidate_entries, candidate_digest = tree_manifest(candidate_semantics)
    assert all(kind != "symlink" for kind, _, _ in trusted_entries)
    assert all(kind != "symlink" for kind, _, _ in candidate_entries)
    assert trusted_entries == candidate_entries
    print(
        f"TREE supplied_semantics entries={len(trusted_entries)} "
        f"reviewer_digest={trusted_digest}"
    )
    print(
        f"TREE candidate_semantics entries={len(candidate_entries)} "
        f"reviewer_digest={candidate_digest}"
    )
    print("TREE semantics_recursive_type_path_content=IDENTICAL no_symlinks=true")

    candidate_entries_all, candidate_tree_digest = tree_manifest(paths["candidate"])
    candidate_symlinks = sum(
        1 for kind, _, _ in candidate_entries_all if kind == "symlink"
    )
    print(
        f"TREE candidate_all entries={len(candidate_entries_all)} "
        f"reviewer_digest={candidate_tree_digest} symlinks={candidate_symlinks}"
    )

    trace_entries, trace_tree_digest = tree_manifest(paths["generation_trace"])
    trace_symlinks = sum(1 for kind, _, _ in trace_entries if kind == "symlink")
    print(
        f"TREE generation_trace entries={len(trace_entries)} "
        f"reviewer_digest={trace_tree_digest} symlinks={trace_symlinks}"
    )

    proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for name in proof_artifacts:
        require_regular(paths["candidate"] / name)
    print("PROOF_ARTIFACTS required_regular_non_symlink=true")

    counts: collections.Counter[str] = collections.Counter()
    trace_lines = 0
    for trace in trace_files:
        with trace.open() as stream:
            for line in stream:
                event = json.loads(line)
                trace_lines += 1
                counts[event.get("type", "<missing>")] += 1
    print(f"TRACE files={len(trace_files)} json_lines={trace_lines} top_types={dict(counts)}")
    print("RESULT provenance_integrity=PASS")


if __name__ == "__main__":
    main()
