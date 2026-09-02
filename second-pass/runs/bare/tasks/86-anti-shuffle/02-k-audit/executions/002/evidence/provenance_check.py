#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inspect_tree(root: Path) -> list[str]:
    issues: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        for name in sorted(dirnames + filenames):
            path = base / name
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                issues.append(f"symlink: {path} -> {os.readlink(path)}")
            elif not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                issues.append(f"non-regular entry: {path} mode={oct(mode)}")
    return issues


def sha256_tree(root: Path) -> str:
    """Pipeline-v2 tree hash used by the recorded stage-one workspace."""
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
                raise RuntimeError(f"unsupported tree entry: {path}")
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


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    run = json.loads(Path("/run.json").read_text(encoding="utf-8"))
    task = json.loads(Path("/task.json").read_text(encoding="utf-8"))
    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    expected_hashes = data["hashes"]
    paths = data["container_paths"]

    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")
    print(f"campaign_object_matches_lock={data['audit_campaign'] == lock}")
    actual_lock_hash = sha256_file(LOCK)
    print(f"audit_campaign_lock_sha256={actual_lock_hash}")
    print(
        "audit_campaign_lock_hash_matches="
        f"{actual_lock_hash == expected_hashes['audit_campaign_lock_sha256']}"
    )

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path("/generation-evidence/usage.json"),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path("/generation-evidence/prompt.txt"),
        Path(paths["generation_trace"]),
        Path(paths["candidate"]),
        Path(paths["canonical"]),
        Path(paths["trusted_prompt"]),
        Path(paths["translator"]),
    ]
    for path in required:
        readable = path.exists() and os.access(path, os.R_OK)
        print(f"required_readable {path}={readable}")

    recorded_files = {
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
        "candidate_prompt_sha256": Path(paths["candidate"]) / "prompt.py",
        "candidate_translator_sha256": Path(paths["candidate"]) / "py2mpy.py",
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
    }
    mismatch = False
    for key, path in recorded_files.items():
        actual = sha256_file(path)
        expected = expected_hashes[key]
        match = actual == expected
        mismatch |= not match
        print(f"{key} actual={actual} expected={expected} match={match}")

    print(
        "candidate_prompt_byte_matches_trusted="
        f"{(Path(paths['candidate']) / 'prompt.py').read_bytes() == Path(paths['trusted_prompt']).read_bytes()}"
    )
    print(
        "candidate_translator_byte_matches_trusted="
        f"{(Path(paths['candidate']) / 'py2mpy.py').read_bytes() == Path(paths['translator']).read_bytes()}"
    )
    print(
        "task_manifest_fields_match_audit_manifest="
        f"{all(data['manifest'].get(key) == value for key, value in task.items())}"
    )
    print(f"problem_id_consistent={data['problem_id'] == task['problem_id'] == '86-anti-shuffle'}")
    print(
        "condition_consistent="
        f"{data['condition'] == task['condition']['name'] == run['condition']['name'] == 'bare'}"
    )
    reference_semantics = Path("/reference/reference-semantics")
    print(f"trusted_reference_semantics_absent={not reference_semantics.exists()}")
    print(
        "legacy_runtime_metrics_absent_allowed="
        f"{not Path('/generation-evidence/runtime-metrics.json').exists()}"
    )

    candidate_tree = sha256_tree(Path(paths["candidate"]))
    trace_tree = sha256_tree(Path(paths["generation_trace"]))
    print(f"candidate_pipeline_tree_sha256={candidate_tree}")
    print(
        "candidate_tree_matches_stage1_workspace="
        f"{candidate_tree == result['outputs']['workspace_sha256'] == invocation['outputs']['workspace_sha256'] == invocation['retained_workspace_sha256']}"
    )
    print(f"trace_pipeline_tree_sha256={trace_tree}")
    print(
        "trace_tree_matches_usage_source_trace="
        f"{trace_tree == usage['source_trace_sha256']}"
    )

    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / relative
        actual = sha256_file(path)
        match = actual == expected
        mismatch |= not match
        print(
            f"stage1_evidence {relative} actual={actual} "
            f"expected={expected} match={match}"
        )

    proof_artifacts = (
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    )
    for name in proof_artifacts:
        path = Path(paths["candidate"]) / name
        regular = path.is_file() and not path.is_symlink()
        print(f"candidate_proof_artifact_regular {name}={regular}")
        mismatch |= not regular

    tree_issues = []
    for root in (Path(paths["candidate"]), Path(paths["generation_root"]), Path("/reference")):
        tree_issues.extend(inspect_tree(root))
    print(f"special_tree_entry_count={len(tree_issues)}")
    for issue in tree_issues:
        print(issue)

    return 1 if mismatch or tree_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
