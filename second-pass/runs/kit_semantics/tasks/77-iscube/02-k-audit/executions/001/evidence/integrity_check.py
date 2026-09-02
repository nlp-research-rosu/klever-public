#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement tools.pipeline_contract.sha256_tree independently."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"not a real directory: {root}")
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise ValueError(f"required path is not a regular file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def compare_trees(left: Path, right: Path) -> tuple[int, list[str]]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            elif stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            else:
                result[relative] = ("unsupported", None)
        return result

    left_inv = inventory(left)
    right_inv = inventory(right)
    differences = []
    for relative in sorted(set(left_inv) | set(right_inv)):
        if left_inv.get(relative) != right_inv.get(relative):
            differences.append(
                f"{relative}: candidate={left_inv.get(relative)!r} "
                f"trusted={right_inv.get(relative)!r}"
            )
    return len(left_inv), differences


def main() -> None:
    document = json.loads(AUDIT.read_text())
    hashes = document["hashes"]
    campaign = json.loads(Path("/audit-campaign-lock.json").read_text())
    print(f"record_layout={document['record_layout']}")
    print(f"semantics_mode={document['semantics_mode']}")
    print(f"campaign_equal={campaign == document['audit_campaign']}")

    required = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
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
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
    ]
    for path in required:
        require_regular(path)
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    for path in trace_files:
        require_regular(path)
    print(f"required_regular_files={len(required)}")
    print(f"trace_regular_files={len(trace_files)}")

    checks = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_metrics_sha256": Path(
            "/generation-evidence/metrics.json"
        ),
        "stage1_invocation_sha256": Path(
            "/generation-evidence/invocation.json"
        ),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
    }
    mismatch_count = 0
    for key, path in checks.items():
        actual = sha256_file(path)
        expected = hashes[key]
        match = actual == expected
        mismatch_count += not match
        print(f"{key}: match={match} actual={actual} expected={expected}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    for relative, expected in generation_result["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        actual = sha256_file(path)
        match = actual == expected
        mismatch_count += not match
        print(
            f"generation-result evidence {relative}: match={match} "
            f"actual={actual} expected={expected}"
        )
    print(
        "invocation_outputs_equal_generation_result="
        f"{invocation['outputs'] == generation_result['outputs']}"
    )

    candidate_tree = pipeline_tree_hash(Path("/candidate"))
    trusted_semantics_tree = pipeline_tree_hash(
        Path("/reference/reference-semantics")
    )
    candidate_semantics_tree = pipeline_tree_hash(
        Path("/candidate/reference-semantics")
    )
    trace_tree = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
    print(f"candidate_pipeline_tree_sha256={candidate_tree}")
    print(
        "candidate_matches_generation_workspace="
        f"{candidate_tree == generation_result['outputs']['workspace_sha256']}"
    )
    print(f"trusted_semantics_pipeline_tree_sha256={trusted_semantics_tree}")
    print(f"candidate_semantics_pipeline_tree_sha256={candidate_semantics_tree}")
    print(
        "trusted_semantics_matches_manifest="
        f"{trusted_semantics_tree == hashes['trusted_reference_semantics_manifest_sha256']}"
    )
    print(
        "candidate_semantics_matches_manifest="
        f"{candidate_semantics_tree == document['manifest']['inputs']['reference_semantics_sha256']}"
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    print(f"trace_pipeline_tree_sha256={trace_tree}")
    print(
        "trace_matches_usage_source="
        f"{trace_tree == usage['source_trace_sha256']}"
    )

    entries, tree_differences = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"candidate_semantics_entries={entries}")
    print(f"candidate_semantics_difference_count={len(tree_differences)}")
    for difference in tree_differences:
        print(f"SEMANTICS_DIFFERENCE {difference}")

    prompt_equal = (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    print(f"declared_file_hash_mismatch_count={mismatch_count}")
    if (
        document["record_layout"] != "pipeline-v3"
        or document["semantics_mode"] != "SUPPLIED_SEMANTICS"
        or not campaign == document["audit_campaign"]
        or mismatch_count
        or tree_differences
        or not prompt_equal
        or not translator_equal
        or not candidate_tree
        == generation_result["outputs"]["workspace_sha256"]
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
