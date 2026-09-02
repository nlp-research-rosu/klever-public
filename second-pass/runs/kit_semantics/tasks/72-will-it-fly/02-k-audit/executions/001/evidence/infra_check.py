#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reproduce the public pipeline-contract manifest-tree digest."""
    digest = hashlib.sha256()
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def require_direct_regular(path: Path) -> None:
    status = os.lstat(path)
    assert stat.S_ISREG(status.st_mode), f"not a direct regular file: {path}"


def compare_trees(candidate: Path, trusted: Path) -> tuple[int, int]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            status = os.lstat(path)
            if stat.S_ISLNK(status.st_mode):
                result[relative] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(status.st_mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(status.st_mode):
                result[relative] = ("file", sha256(path))
            else:
                result[relative] = (f"special:{stat.S_IFMT(status.st_mode)}", None)
        return result

    candidate_inventory = inventory(candidate)
    trusted_inventory = inventory(trusted)
    assert candidate_inventory == trusted_inventory, "supplied-semantics tree mismatch"
    assert all(kind != "symlink" for kind, _ in candidate_inventory.values())
    file_count = sum(kind == "file" for kind, _ in candidate_inventory.values())
    directory_count = sum(kind == "directory" for kind, _ in candidate_inventory.values())
    return file_count, directory_count


def main() -> None:
    audit_input = json.loads(AUDIT_INPUT.read_text())
    lock_path = Path(audit_input["container_paths"]["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())

    assert audit_input["record_layout"] == "pipeline-v3"
    assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert lock == audit_input["audit_campaign"]
    assert sha256(lock_path) == audit_input["hashes"]["audit_campaign_lock_sha256"]
    print("campaign_block_equal=true")
    print(f"audit_campaign_lock_sha256={sha256(lock_path)}")

    paths = audit_input["container_paths"]
    declared_mounts = {
        key: Path(value)
        for key, value in paths.items()
        if key not in {"generation_root", "generation_trace", "candidate"}
    }
    for key, path in sorted(declared_mounts.items()):
        require_direct_regular(path)
        print(f"direct_regular_mount[{key}]={path}")
    for key in ("generation_root", "generation_trace", "candidate"):
        path = Path(paths[key])
        status = os.lstat(path)
        assert stat.S_ISDIR(status.st_mode) and not stat.S_ISLNK(status.st_mode)
        print(f"direct_directory_mount[{key}]={path}")

    required_records = [
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
    for path in required_records:
        require_direct_regular(path)
        print(f"required_record={path} bytes={path.stat().st_size}")

    expected_hashes = {
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
    for path, key in expected_hashes.items():
        actual = sha256(path)
        expected = audit_input["hashes"][key]
        assert actual == expected, f"hash mismatch for {path}: {actual} != {expected}"
        print(f"recorded_hash_match[{key}]={actual}")

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("candidate_prompt_byte_equal=true")
    print("candidate_translator_byte_equal=true")

    assert Path("/reference/reference-semantics").is_dir()
    files, directories = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"supplied_semantics_tree_equal=true files={files} directories={directories}")
    trusted_semantics_manifest = pipeline_tree_sha256(
        Path("/reference/reference-semantics")
    )
    candidate_semantics_manifest = pipeline_tree_sha256(
        Path("/candidate/reference-semantics")
    )
    expected_semantics_manifest = audit_input["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    assert trusted_semantics_manifest == expected_semantics_manifest
    assert candidate_semantics_manifest == expected_semantics_manifest
    print(
        "pipeline_manifest_tree_hash_match[trusted_reference_semantics]="
        f"{trusted_semantics_manifest}"
    )
    print(
        "pipeline_manifest_tree_hash_match[candidate_reference_semantics]="
        f"{candidate_semantics_manifest}"
    )
    # These fresh extracted-tree hashes make the independent audit snapshot
    # identifiable.  The separate audit-input raw-bundle digests cover the
    # launcher-owned archives and are not hashes of this extracted namespace.
    print(
        "independent_extracted_tree_hash[candidate]="
        f"{pipeline_tree_sha256(Path('/candidate'))}"
    )
    print(
        "independent_extracted_tree_hash[generation_trace]="
        f"{pipeline_tree_sha256(Path('/generation-evidence/codex-trace'))}"
    )

    json_records = [
        AUDIT_INPUT,
        lock_path,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
    ]
    for path in json_records:
        json.loads(path.read_text())
        print(f"valid_json={path}")

    result = json.loads(Path("/generation-result.json").read_text())
    trace_outputs = {
        relative: expected
        for relative, expected in result["outputs"]["evidence"].items()
        if relative.startswith("codex-trace/")
    }
    actual_trace_files = {
        path.relative_to("/generation-evidence").as_posix(): path
        for path in Path("/generation-evidence/codex-trace").rglob("*")
        if path.is_file()
    }
    assert set(actual_trace_files) == set(trace_outputs)
    for relative, path in sorted(actual_trace_files.items()):
        require_direct_regular(path)
        actual = sha256(path)
        assert actual == trace_outputs[relative]
        print(f"trace_hash_match[{relative}]={actual}")

        event_types: Counter[str] = Counter()
        payload_types: Counter[str] = Counter()
        line_count = 0
        with path.open() as stream:
            for line_count, line in enumerate(stream, start=1):
                event = json.loads(line)
                event_types[str(event.get("type", "<missing>"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type", "<missing>"))] += 1
        print(f"trace_jsonl_valid=true lines={line_count}")
        print(f"trace_event_types={dict(sorted(event_types.items()))}")
        print(f"trace_payload_types={dict(sorted(payload_types.items()))}")

    output = Path("/generation-evidence/codex-output.log").read_text(errors="replace")
    print(f"codex_output_fully_read=true chars={len(output)} lines={output.count(chr(10))}")
    for marker in (
        "#Top",
        "WarnStuckClaimState",
        "RESULT: KPROVE_PASSED",
        "VALIDATED",
        "[Error]",
    ):
        print(f"codex_output_marker[{marker}]={output.count(marker)}")

    required_candidate_artifacts = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for name in required_candidate_artifacts:
        path = Path("/candidate") / name
        require_direct_regular(path)
        print(f"required_candidate_artifact={path} bytes={path.stat().st_size}")

    print("INFRASTRUCTURE_GATE=PASS")


if __name__ == "__main__":
    main()
