#!/usr/bin/env python3
"""Independent pipeline-v3 provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_sha256(root: Path) -> str:
    """The pipeline-v3 tree algorithm from pipeline_contract.sha256_tree."""
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")


def compare_trees(left: Path, right: Path) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", file_sha256(path))
            elif stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            else:
                result[relative] = ("unsupported", None)
        return result

    left_entries = entries(left)
    right_entries = entries(right)
    assert left_entries == right_entries, "candidate/trusted semantics entry mismatch"
    print(f"semantics_recursive_identity: PASS ({len(left_entries)} entries)")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert Path("/reference/reference-semantics").is_dir()
    print("layout_and_mode: PASS (pipeline-v3, SUPPLIED_SEMANTICS)")

    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    require_regular(lock_path)
    lock = json.loads(lock_path.read_text())
    assert lock == audit["audit_campaign"]
    lock_hash = file_sha256(lock_path)
    assert lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_lock_block_and_hash: PASS {lock_hash}")

    required_records = {
        "run_manifest": Path(audit["container_paths"]["run_manifest"]),
        "task_manifest": Path(audit["container_paths"]["task_manifest"]),
        "stage1_result": Path(audit["container_paths"]["stage1_result"]),
        "generation_manifest": Path(audit["container_paths"]["generation_manifest"]),
        "generation_metrics": Path(audit["container_paths"]["generation_metrics"]),
        "generation_runtime_metrics": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage": Path("/generation-evidence/usage.json"),
        "generation_last": Path(audit["container_paths"]["generation_last"]),
        "generation_output": Path(audit["container_paths"]["generation_output"]),
        "generation_prompt": Path("/generation-evidence/prompt.txt"),
    }
    for label, path in required_records.items():
        require_regular(path)
        print(f"required_record_{label}: PASS {path} {file_sha256(path)}")

    trace_root = Path(audit["container_paths"]["generation_trace"])
    assert trace_root.is_dir()
    trace_files = sorted(trace_root.rglob("*"))
    assert trace_files
    for path in trace_files:
        if path.is_file():
            require_regular(path)
        elif path.is_symlink():
            raise AssertionError(f"trace symlink: {path}")
    print(f"structured_trace_tree: PASS {tree_sha256(trace_root)}")

    hash_map = {
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
        Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, key in hash_map.items():
        require_regular(path)
        actual = file_sha256(path)
        expected = audit["hashes"][key]
        assert actual == expected, f"{path}: {actual} != {expected}"
        print(f"recorded_hash_{key}: PASS {actual}")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    for record_name, expected_hash in result["outputs"]["evidence"].items():
        record_path = Path("/generation-evidence") / record_name
        require_regular(record_path)
        actual_hash = file_sha256(record_path)
        assert actual_hash == expected_hash
        assert invocation["outputs"]["evidence"][record_name] == expected_hash
        print(f"stage1_output_evidence_{record_name}: PASS {actual_hash}")
    candidate_tree = tree_sha256(Path("/candidate"))
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    assert candidate_tree == invocation["outputs"]["workspace_sha256"]
    print(f"candidate_tree_matches_stage1_records: PASS {candidate_tree}")

    trace_tree = tree_sha256(trace_root)
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    assert trace_tree == usage["source_trace_sha256"]
    print(f"trace_tree_matches_usage_record: PASS {trace_tree}")

    compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    candidate_semantics_tree = tree_sha256(Path("/candidate/reference-semantics"))
    trusted_semantics_tree = tree_sha256(Path("/reference/reference-semantics"))
    assert candidate_semantics_tree == trusted_semantics_tree
    assert trusted_semantics_tree == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    assert trusted_semantics_tree == audit["manifest"]["inputs"]["reference_semantics_sha256"]
    print(f"semantics_pipeline_tree_hash: PASS {trusted_semantics_tree}")

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("candidate_prompt_and_translator_byte_identity: PASS")

    # The launcher also records content-tree digests whose algorithm is not
    # declared in audit-input.json. Byte/entry identity plus the declared
    # pipeline tree hash above independently establishes the mounted integrity.
    print(
        "launcher_content_digest_claims_unrecomputed:",
        audit["hashes"]["candidate_reference_semantics_sha256"],
        audit["hashes"]["trusted_reference_semantics_sha256"],
        audit["hashes"]["candidate_tree_sha256"],
    )


if __name__ == "__main__":
    main()
