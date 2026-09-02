#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

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


def sha256_tree(root: Path) -> str:
    """Match the public pipeline_contract.sha256_tree representation."""
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
                raise RuntimeError(f"unsupported or linked tree entry: {path}")
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


def real_regular(path: Path) -> bool:
    mode = path.lstat().st_mode
    return stat.S_ISREG(mode) and not path.is_symlink()


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    hashes = audit["hashes"]

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_block_equal={audit['audit_campaign'] == lock}")

    checks = {
        "audit_campaign_lock_sha256": lock_path,
        "run_manifest_sha256": Path(audit["container_paths"]["run_manifest"]),
        "task_manifest_sha256": Path(audit["container_paths"]["task_manifest"]),
        "stage1_result_sha256": Path(audit["container_paths"]["stage1_result"]),
        "stage1_invocation_sha256": Path(
            audit["container_paths"]["generation_manifest"]
        ),
        "generation_metrics_sha256": Path(
            audit["container_paths"]["generation_metrics"]
        ),
        "generation_codex_last_sha256": Path(
            audit["container_paths"]["generation_last"]
        ),
        "generation_codex_output_sha256": Path(
            audit["container_paths"]["generation_output"]
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "canonical_sha256": Path(audit["container_paths"]["canonical"]),
        "trusted_prompt_sha256": Path(audit["container_paths"]["trusted_prompt"]),
        "trusted_translator_sha256": Path(audit["container_paths"]["translator"]),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    }
    all_hashes_match = True
    for field, path in checks.items():
        mounted = sha256_file(path)
        expected = hashes[field]
        matches = mounted == expected
        all_hashes_match &= matches
        print(
            f"{field}: regular={real_regular(path)} "
            f"mounted={mounted} declared={expected} match={matches}"
        )

    trace_tree = Path(audit["container_paths"]["generation_trace"])
    trace_digest = sha256_tree(trace_tree)
    trace_files = sorted(trace_tree.rglob("*.jsonl"))
    generation_result = json.loads(Path("/generation-result.json").read_text())
    trace_relative = trace_files[0].relative_to(Path("/generation-evidence")).as_posix()
    trace_file_declared = generation_result["outputs"]["evidence"][trace_relative]
    trace_file_mounted = sha256_file(trace_files[0])
    print(
        f"generation_trace_file_sha256={trace_file_mounted} "
        f"stage1_declared={trace_file_declared} "
        f"match={trace_file_mounted == trace_file_declared}"
    )
    print(
        "generation_trace_pipeline_digest="
        f"{trace_digest} declared_source_trace="
        f"{json.loads(Path('/generation-evidence/usage.json').read_text())['source_trace_sha256']} "
        f"match={trace_digest == json.loads(Path('/generation-evidence/usage.json').read_text())['source_trace_sha256']}"
    )

    candidate_tree_digest = sha256_tree(Path(audit["container_paths"]["candidate"]))
    stage1_workspace = json.loads(Path("/generation-result.json").read_text())[
        "outputs"
    ]["workspace_sha256"]
    print(
        f"candidate_pipeline_digest={candidate_tree_digest} "
        f"stage1_workspace_declared={stage1_workspace} "
        f"match={candidate_tree_digest == stage1_workspace}"
    )
    print(
        "audit_input_candidate_tree_digest="
        f"{hashes['candidate_tree_sha256']} "
        "(different launcher digest namespace; no algorithm is declared)"
    )
    print(
        "audit_input_generation_trace_digest="
        f"{hashes['generation_codex_trace_sha256']} "
        "(different launcher digest namespace; no algorithm is declared)"
    )

    required = [
        AUDIT_INPUT,
        lock_path,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        *trace_tree.rglob("*"),
    ]
    required = [path for path in required if path.is_file()]
    print(f"required_regular_file_count={len(required)}")
    print(f"all_required_regular={all(real_regular(path) for path in required)}")
    print(
        "candidate_prompt_byte_equal_trusted="
        f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
    )
    print(
        "candidate_translator_byte_equal_trusted="
        f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
    )
    print(
        "trusted_reference_semantics_absent="
        f"{not Path('/reference/reference-semantics').exists()}"
    )
    print(
        "candidate_reference_semantics_absent="
        f"{not Path('/candidate/reference-semantics').exists()}"
    )
    print(f"all_declared_file_hashes_match={all_hashes_match}")
    return 0 if all_hashes_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
