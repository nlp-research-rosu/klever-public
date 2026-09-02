#!/usr/bin/env python3
"""Independent integrity/provenance checks for audit 98-count-upper."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest_digest(root: Path) -> str:
    """Reproduce pipeline-v3's length-delimited path/kind/size tree digest."""
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def compare_trees(left: Path, right: Path) -> None:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        found: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                found[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                found[relative] = ("file", sha256_file(path))
            else:
                found[relative] = ("unsupported", None)
        return found

    left_inventory = inventory(left)
    right_inventory = inventory(right)
    assert left_inventory == right_inventory, "reference-semantics trees differ"
    unsupported = [
        relative
        for relative, (kind, _) in right_inventory.items()
        if kind == "unsupported"
    ]
    assert not unsupported, f"candidate reference semantics has unsupported entries: {unsupported}"
    print(f"REFERENCE_TREE_COMPARE=PASS entries={len(left_inventory)}")


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["problem_id"] == "98-count-upper"
    assert audit["condition"] == "kit-semantics"
    assert audit["audit_campaign"] == lock
    assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
    print("CAMPAIGN_LOCK=PASS")

    container_paths = audit["container_paths"]
    for key, rendered in sorted(container_paths.items()):
        path = Path(rendered)
        if key in {"candidate", "generation_root", "generation_trace"}:
            require_directory(path)
        else:
            require_regular(path)
    print(f"DECLARED_CONTAINER_PATHS=PASS count={len(container_paths)}")

    required_pipeline_files = [
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
    ]
    for path in required_pipeline_files:
        require_regular(path)
        # Read every required record, including the non-JSON records.
        raw = path.read_bytes()
        assert raw or path.name == "codex-last.txt"
        if path.suffix == ".json":
            json.loads(raw)
    print(f"PIPELINE_V3_RECORDS=PASS count={len(required_pipeline_files)}")

    required_candidate_files = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
        Path("/candidate/PROOF.md"),
    ]
    for path in required_candidate_files:
        require_regular(path)
        assert path.read_bytes()
    print(f"CANDIDATE_REQUIRED_ARTIFACTS=PASS count={len(required_candidate_files)}")

    expected_file_hashes = {
        LOCK: "audit_campaign_lock_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    }
    for path, field in expected_file_hashes.items():
        actual = sha256_file(path)
        expected = audit["hashes"][field]
        assert actual == expected, f"{field}: {actual} != {expected}"
        print(f"FILE_HASH {field} {actual} PASS")

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    compare_trees(
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    )

    task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    audit_manifest = dict(audit["manifest"])
    audit_manifest.pop("config")
    assert task == audit_manifest
    assert audit["manifest"]["config"] == audit["manifest_config"]
    assert task["problem_id"] == audit["problem_id"]
    assert task["condition"]["name"] == audit["condition"]
    assert result["outputs"] == invocation["outputs"]
    assert result["session_id"] == invocation["session_id"]

    semantics_digest = tree_manifest_digest(Path("/reference/reference-semantics"))
    candidate_semantics_digest = tree_manifest_digest(
        Path("/candidate/reference-semantics")
    )
    candidate_digest = tree_manifest_digest(Path("/candidate"))
    trace_digest = tree_manifest_digest(Path("/generation-evidence/codex-trace"))
    assert semantics_digest == task["inputs"]["reference_semantics_sha256"]
    assert candidate_semantics_digest == semantics_digest
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    assert trace_digest == usage["source_trace_sha256"]
    print(f"PIPELINE_TREE reference-semantics {semantics_digest} PASS")
    print(f"PIPELINE_TREE candidate {candidate_digest} PASS")
    print(f"PIPELINE_TREE codex-trace {trace_digest} PASS")
    print("LAUNCHER_RECORDED_AGGREGATES")
    for field in (
        "candidate_reference_semantics_sha256",
        "trusted_reference_semantics_sha256",
        "candidate_tree_sha256",
        "generation_codex_trace_sha256",
    ):
        print(f"  {field}={audit['hashes'][field]}")

    generated_hashes = result["outputs"]["evidence"]
    evidence_root = Path("/generation-evidence")
    for relative, expected in sorted(generated_hashes.items()):
        path = evidence_root / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, f"generation result evidence mismatch: {relative}"
        print(f"GENERATION_OUTPUT_HASH {relative} {actual} PASS")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert trace_files
    counts: collections.Counter[str] = collections.Counter()
    total_lines = 0
    for path in trace_files:
        require_regular(path)
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                event = json.loads(line)
                assert isinstance(event, dict)
                counts[str(event.get("type"))] += 1
                total_lines += 1
    print(
        "STRUCTURED_TRACE=PASS "
        f"files={len(trace_files)} lines={total_lines} "
        f"top_level_types={dict(sorted(counts.items()))}"
    )
    print("INTEGRITY_STATUS=PASS")


if __name__ == "__main__":
    main()
