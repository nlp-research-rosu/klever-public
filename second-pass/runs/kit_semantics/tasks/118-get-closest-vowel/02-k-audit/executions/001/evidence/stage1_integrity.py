#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Independent implementation of the pipeline-v3 tree-hash contract."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported entry: {path}")
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required record is not a regular file: {path}"


def compare_trees(left: Path, right: Path) -> tuple[int, list[str]]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            elif stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            else:
                result[relative] = ("unsupported", None)
        return result

    left_inventory = inventory(left)
    right_inventory = inventory(right)
    differences: list[str] = []
    for relative in sorted(set(left_inventory) | set(right_inventory)):
        if left_inventory.get(relative) != right_inventory.get(relative):
            differences.append(
                f"{relative}: candidate={left_inventory.get(relative)!r} "
                f"trusted={right_inventory.get(relative)!r}"
            )
    return len(left_inventory), differences


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

    required = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": GENERATION / "invocation.json",
        "generation_metrics_sha256": GENERATION / "metrics.json",
        "generation_runtime_metrics_sha256": GENERATION / "runtime-metrics.json",
        "generation_usage_sha256": GENERATION / "usage.json",
        "generation_codex_last_sha256": GENERATION / "codex-last.txt",
        "generation_codex_output_sha256": GENERATION / "codex-output.log",
        "generation_prompt_sha256": GENERATION / "prompt.txt",
        "canonical_sha256": REFERENCE / "canonical.py",
        "trusted_prompt_sha256": REFERENCE / "prompt.py",
        "trusted_translator_sha256": REFERENCE / "py2mpy.py",
        "candidate_prompt_sha256": CANDIDATE / "prompt.py",
        "candidate_translator_sha256": CANDIDATE / "py2mpy.py",
    }
    print("REQUIRED FILE HASHES")
    for key, path in required.items():
        require_regular(path)
        actual = sha256_file(path)
        expected = hashes[key]
        print(f"{key}: actual={actual} expected={expected} match={actual == expected}")
        assert actual == expected

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    print(f"campaign_lock_exact_match={lock == audit['audit_campaign']}")
    assert lock == audit["audit_campaign"]

    for json_path in (
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "runtime-metrics.json",
        GENERATION / "usage.json",
    ):
        parsed = json.loads(json_path.read_text())
        assert isinstance(parsed, dict)
        print(f"valid_json_object={json_path}")

    task = json.loads(Path("/task.json").read_text())
    run = json.loads(Path("/run.json").read_text())
    common_manifest = {
        key: audit["manifest"][key]
        for key in task
    }
    print(
        "audit_embedded_manifest_common_fields_match="
        f"{common_manifest == task}"
    )
    assert common_manifest == task
    assert task["problem_id"] == audit["problem_id"]
    assert task["condition"]["name"] == audit["condition"]
    assert run["condition"]["name"] == audit["condition"]
    print("problem_and_condition_cross_records_match=True")

    stage1 = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((GENERATION / "invocation.json").read_text())
    evidence_hashes = stage1["outputs"]["evidence"]
    assert evidence_hashes == invocation["outputs"]["evidence"]
    print("stage1_and_invocation_evidence_maps_match=True")
    for relative, expected in sorted(evidence_hashes.items()):
        path = GENERATION / relative
        require_regular(path)
        actual = sha256_file(path)
        print(
            f"generation_output={relative} actual={actual} "
            f"expected={expected} match={actual == expected}"
        )
        assert actual == expected

    trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
    trace_regular = [path for path in trace_files if path.is_file()]
    trace_types: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_regular:
        require_regular(path)
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                event = json.loads(line)
                assert isinstance(event, dict)
                trace_types[str(event.get("type"))] += 1
                trace_lines += 1
    print(
        f"trace_files={len(trace_regular)} trace_lines={trace_lines} "
        f"trace_types={dict(sorted(trace_types.items()))}"
    )
    trace_hash = pipeline_tree_hash(GENERATION / "codex-trace")
    print(
        f"trace_pipeline_tree_hash={trace_hash} "
        f"usage_source_trace_sha256="
        f"{json.loads((GENERATION / 'usage.json').read_text())['source_trace_sha256']}"
    )
    assert trace_hash == json.loads(
        (GENERATION / "usage.json").read_text()
    )["source_trace_sha256"]

    semantics_count, semantics_differences = compare_trees(
        CANDIDATE / "reference-semantics",
        REFERENCE / "reference-semantics",
    )
    print(
        f"supplied_semantics_entries={semantics_count} "
        f"differences={len(semantics_differences)}"
    )
    for difference in semantics_differences:
        print(f"SEMANTICS_DIFFERENCE {difference}")
    assert not semantics_differences

    candidate_semantics_hash = pipeline_tree_hash(
        CANDIDATE / "reference-semantics"
    )
    trusted_semantics_hash = pipeline_tree_hash(
        REFERENCE / "reference-semantics"
    )
    expected_semantics_manifest_hash = hashes[
        "trusted_reference_semantics_manifest_sha256"
    ]
    print(
        f"candidate_semantics_pipeline_hash={candidate_semantics_hash} "
        f"trusted_semantics_pipeline_hash={trusted_semantics_hash} "
        f"expected_manifest_hash={expected_semantics_manifest_hash}"
    )
    assert candidate_semantics_hash == trusted_semantics_hash
    assert trusted_semantics_hash == expected_semantics_manifest_hash

    candidate_tree_hash = pipeline_tree_hash(CANDIDATE)
    generated_tree_hash = stage1["outputs"]["workspace_sha256"]
    print(
        f"candidate_pipeline_tree_hash={candidate_tree_hash} "
        f"generation_result_workspace_sha256={generated_tree_hash}"
    )
    assert candidate_tree_hash == generated_tree_hash
    print(
        "launcher_snapshot_hashes="
        f"candidate_tree:{hashes['candidate_tree_sha256']} "
        f"candidate_semantics:{hashes['candidate_reference_semantics_sha256']} "
        f"trusted_semantics:{hashes['trusted_reference_semantics_sha256']} "
        f"generation_trace:{hashes['generation_codex_trace_sha256']}"
    )
    assert (
        hashes["candidate_reference_semantics_sha256"]
        == hashes["trusted_reference_semantics_sha256"]
    )

    symlinks = []
    for root in (CANDIDATE, GENERATION, REFERENCE):
        for path in root.rglob("*"):
            if path.is_symlink():
                symlinks.append(str(path))
    print(f"symlink_count={len(symlinks)}")
    for path in symlinks:
        print(f"SYMLINK {path}")
    assert not symlinks

    prompt_equal = (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    translator_equal = (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    assert prompt_equal and translator_equal
    print("STAGE1_INTEGRITY=PASS")


if __name__ == "__main__":
    main()
