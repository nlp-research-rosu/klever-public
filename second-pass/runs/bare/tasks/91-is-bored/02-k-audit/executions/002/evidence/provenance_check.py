#!/usr/bin/env python3
"""Independent integrity checks over the launcher-mounted audit inputs."""

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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce tools.pipeline_contract.sha256_tree without importing it."""
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError(f"not a real directory: {root}")
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
                raise RuntimeError(f"linked/unsupported entry: {path}")

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


def assert_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required regular file is mistyped: {path}")


def main() -> None:
    document = json.loads(AUDIT_INPUT.read_text())
    hashes = document["hashes"]
    paths = document["container_paths"]

    checks = {
        "audit_campaign_lock_sha256": Path(paths["audit_campaign_lock"]),
        "candidate_prompt_sha256": Path(paths["candidate"]) / "prompt.py",
        "candidate_translator_sha256": Path(paths["candidate"]) / "py2mpy.py",
        "canonical_sha256": Path(paths["canonical"]),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
        "generation_usage_sha256": Path(paths["generation_root"]) / "usage.json",
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
    }
    for key, path in checks.items():
        assert_regular(path)
        actual = sha256_file(path)
        expected = hashes[key]
        print(f"{key}: expected={expected} actual={actual} match={actual == expected}")
        if actual != expected:
            raise AssertionError(key)

    lock = json.loads(Path(paths["audit_campaign_lock"]).read_text())
    print(f"campaign_block_matches_lock={lock == document['audit_campaign']}")
    if lock != document["audit_campaign"]:
        raise AssertionError("campaign lock content mismatch")

    prompt_equal = (
        (Path(paths["candidate"]) / "prompt.py").read_bytes()
        == Path(paths["trusted_prompt"]).read_bytes()
    )
    translator_equal = (
        (Path(paths["candidate"]) / "py2mpy.py").read_bytes()
        == Path(paths["translator"]).read_bytes()
    )
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not prompt_equal or not translator_equal:
        raise AssertionError("trusted input byte mismatch")

    reference_semantics = Path("/reference/reference-semantics")
    print(f"reference_semantics_absent={not reference_semantics.exists()}")
    if reference_semantics.exists() or reference_semantics.is_symlink():
        raise AssertionError("GENERATED_SEMANTICS mount contradiction")

    candidate_digest = pipeline_tree_digest(Path(paths["candidate"]))
    trace_digest = pipeline_tree_digest(Path(paths["generation_trace"]))
    result = json.loads(Path(paths["stage1_result"]).read_text())
    usage = json.loads((Path(paths["generation_root"]) / "usage.json").read_text())
    print(f"candidate_pipeline_tree_digest={candidate_digest}")
    print(f"stage1_workspace_digest={result['outputs']['workspace_sha256']}")
    print(
        "candidate_matches_stage1_workspace="
        f"{candidate_digest == result['outputs']['workspace_sha256']}"
    )
    print(f"trace_pipeline_tree_digest={trace_digest}")
    print(f"usage_source_trace_digest={usage['source_trace_sha256']}")
    print(
        "trace_matches_usage_source="
        f"{trace_digest == usage['source_trace_sha256']}"
    )
    if candidate_digest != result["outputs"]["workspace_sha256"]:
        raise AssertionError("mounted candidate differs from stage-1 workspace")
    if trace_digest != usage["source_trace_sha256"]:
        raise AssertionError("mounted trace differs from usage source")

    for root in [
        Path(paths["candidate"]),
        Path(paths["generation_root"]),
        Path("/reference"),
    ]:
        unsupported = []
        for path in root.rglob("*"):
            mode = path.lstat().st_mode
            if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                unsupported.append(str(path))
        print(f"unsupported_entries[{root}]={unsupported}")
        if unsupported:
            raise AssertionError(f"unsupported entries under {root}")


if __name__ == "__main__":
    main()
