#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

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
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_tree_hash(root: Path) -> str:
    """Reproduce the pipeline-v3 path/kind/size/content tree manifest digest."""
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise AssertionError(f"tree root is not a real directory: {root}")

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
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required regular file is mistyped or linked: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"required directory is mistyped or linked: {path}")


def same_tree(left: Path, right: Path) -> tuple[bool, list[str]]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        pending = [root]
        while pending:
            directory = pending.pop()
            for child in os.scandir(directory):
                path = Path(child.path)
                relative = path.relative_to(root).as_posix()
                mode = child.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    result[relative] = ("directory", None)
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    result[relative] = ("file", sha256_file(path))
                else:
                    result[relative] = ("unsupported", None)
        return result

    left_inventory = inventory(left)
    right_inventory = inventory(right)
    differences = []
    for name in sorted(set(left_inventory) | set(right_inventory)):
        if left_inventory.get(name) != right_inventory.get(name):
            differences.append(
                f"{name}: candidate={left_inventory.get(name)!r} "
                f"trusted={right_inventory.get(name)!r}"
            )
    return not differences, differences


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

    campaign = Path(audit["container_paths"]["audit_campaign_lock"])
    require_regular(campaign)
    campaign_data = json.loads(campaign.read_text(encoding="utf-8"))
    assert campaign_data == audit["audit_campaign"]
    assert sha256_file(campaign) == audit["hashes"]["audit_campaign_lock_sha256"]
    print("campaign_lock_equal=true")
    print(f"campaign_lock_sha256={sha256_file(campaign)}")

    files_and_hash_keys = [
        (Path("/reference/canonical.py"), "canonical_sha256"),
        (Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        (Path("/reference/py2mpy.py"), "trusted_translator_sha256"),
        (Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        (Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
        (Path("/run.json"), "run_manifest_sha256"),
        (Path("/task.json"), "task_manifest_sha256"),
        (Path("/generation-result.json"), "stage1_result_sha256"),
        (Path("/generation-evidence/invocation.json"), "stage1_invocation_sha256"),
        (Path("/generation-evidence/metrics.json"), "generation_metrics_sha256"),
        (
            Path("/generation-evidence/runtime-metrics.json"),
            "generation_runtime_metrics_sha256",
        ),
        (Path("/generation-evidence/usage.json"), "generation_usage_sha256"),
        (
            Path("/generation-evidence/codex-last.txt"),
            "generation_codex_last_sha256",
        ),
        (
            Path("/generation-evidence/codex-output.log"),
            "generation_codex_output_sha256",
        ),
        (Path("/generation-evidence/prompt.txt"), "generation_prompt_sha256"),
    ]
    for path, hash_key in files_and_hash_keys:
        require_regular(path)
        actual = sha256_file(path)
        expected = audit["hashes"][hash_key]
        assert actual == expected, (path, actual, expected)
        print(f"{hash_key}={actual}")

    trace_root = Path("/generation-evidence/codex-trace")
    candidate_root = Path("/candidate")
    candidate_semantics = candidate_root / "reference-semantics"
    trusted_semantics = Path("/reference/reference-semantics")
    for directory in (
        Path("/generation-evidence"),
        trace_root,
        candidate_root,
        candidate_semantics,
        trusted_semantics,
    ):
        require_directory(directory)

    generation_result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    for relative, expected in generation_result["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, (path, actual, expected)
        assert invocation["outputs"]["evidence"][relative] == expected
        print(f"generation_output[{relative}]={actual}")

    candidate_tree_hash = manifest_tree_hash(candidate_root)
    trace_tree_hash = manifest_tree_hash(trace_root)
    candidate_semantics_hash = manifest_tree_hash(candidate_semantics)
    trusted_semantics_hash = manifest_tree_hash(trusted_semantics)
    assert candidate_tree_hash == generation_result["outputs"]["workspace_sha256"]
    assert candidate_tree_hash == invocation["outputs"]["workspace_sha256"]
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    assert trace_tree_hash == usage["source_trace_sha256"]
    expected_semantics_manifest = audit["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    assert candidate_semantics_hash == expected_semantics_manifest
    assert trusted_semantics_hash == expected_semantics_manifest
    print(f"candidate_manifest_tree_sha256={candidate_tree_hash}")
    print(f"trace_manifest_tree_sha256={trace_tree_hash}")
    print(
        "launcher_recorded_trace_mount_sha256="
        f"{audit['hashes']['generation_codex_trace_sha256']}"
    )
    print(f"candidate_semantics_manifest_sha256={candidate_semantics_hash}")
    print(f"trusted_semantics_manifest_sha256={trusted_semantics_hash}")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    trees_equal, differences = same_tree(candidate_semantics, trusted_semantics)
    assert trees_equal, "\n".join(differences)
    print("candidate_prompt_byte_identity=true")
    print("candidate_translator_byte_identity=true")
    print("candidate_vs_trusted_semantics_recursive_identity=true")
    print("unsupported_or_symlinked_semantics_entries=0")

    print("PROVENANCE_CHECK=PASS")


if __name__ == "__main__":
    main()
