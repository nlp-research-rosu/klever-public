#!/usr/bin/env python3
"""Independent read-only integrity check for the mounted audit records."""

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


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement tools.pipeline_contract.sha256_tree independently."""
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
                raise RuntimeError(f"unsupported or linked entry: {path}")
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
        raise RuntimeError(f"not a regular non-symlink file: {path}")


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    paths = audit["container_paths"]
    hashes = audit["hashes"]
    lock_path = Path(paths["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())

    required = [
        AUDIT_INPUT,
        lock_path,
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path(paths["generation_root"]) / "prompt.txt",
        Path(paths["generation_root"]) / "usage.json",
    ]
    trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
    required.extend(p for p in trace_files if p.is_file())
    for path in required:
        require_regular(path)

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"required_regular_files={len(required)}")
    print(f"campaign_block_matches={audit['audit_campaign'] == lock}")
    print(
        "campaign_lock_hash="
        f"{sha256_file(lock_path)} expected={hashes['audit_campaign_lock_sha256']}"
    )
    print(
        "reference_semantics_absent="
        f"{not Path('/reference/reference-semantics').exists()}"
    )

    direct = {
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
    mismatches = 0
    for field, path in direct.items():
        actual = sha256_file(path)
        expected = hashes[field]
        match = actual == expected
        mismatches += not match
        print(f"{field} actual={actual} expected={expected} match={match}")

    prompt_same = (
        (Path(paths["candidate"]) / "prompt.py").read_bytes()
        == Path(paths["trusted_prompt"]).read_bytes()
    )
    translator_same = (
        (Path(paths["candidate"]) / "py2mpy.py").read_bytes()
        == Path(paths["translator"]).read_bytes()
    )
    print(f"candidate_prompt_byte_identical={prompt_same}")
    print(f"candidate_translator_byte_identical={translator_same}")

    candidate_hash = pipeline_tree_hash(Path(paths["candidate"]))
    trace_hash = pipeline_tree_hash(Path(paths["generation_trace"]))
    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    usage = json.loads((Path(paths["generation_root"]) / "usage.json").read_text())
    print(f"pipeline_tree_hash(candidate)={candidate_hash}")
    print(
        "candidate_matches_invocation_retained_workspace="
        f"{candidate_hash == invocation['retained_workspace_sha256']}"
    )
    print(f"pipeline_tree_hash(trace)={trace_hash}")
    print(
        "trace_matches_usage_source_trace="
        f"{trace_hash == usage['source_trace_sha256']}"
    )

    linked = []
    for root in [
        Path(paths["candidate"]),
        Path(paths["generation_root"]),
        Path("/reference"),
    ]:
        linked.extend(p for p in root.rglob("*") if p.is_symlink())
    print(f"symlink_count={len(linked)}")
    for path in linked:
        print(f"symlink={path}")

    return int(
        mismatches
        or audit["audit_campaign"] != lock
        or not prompt_same
        or not translator_same
        or linked
        or Path("/reference/reference-semantics").exists()
    )


if __name__ == "__main__":
    raise SystemExit(main())
