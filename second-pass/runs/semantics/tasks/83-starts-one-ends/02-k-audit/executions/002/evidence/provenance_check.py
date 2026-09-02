#!/usr/bin/env python3
"""Independent launcher-record and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    mode = path.lstat().st_mode
    return stat.S_ISREG(mode) and not path.is_symlink()


def tree_manifest(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root))
        if path.is_symlink():
            result[relative] = ("symlink", str(path.readlink()))
        elif path.is_dir():
            result[relative] = ("directory", "")
        elif path.is_file():
            result[relative] = ("file", digest(path))
        else:
            result[relative] = ("other", "")
    return result


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))
    expected = data["hashes"]
    paths = data["container_paths"]
    failures: list[str] = []

    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")
    print(f"input_provenance={data['manifest']['input_provenance']}")

    campaign_equal = lock == data["audit_campaign"]
    campaign_hash = digest(CAMPAIGN_LOCK)
    print(f"campaign_block_equal={campaign_equal}")
    print(f"audit_campaign_lock_sha256={campaign_hash}")
    print(
        "audit_campaign_lock_hash_matches="
        f"{campaign_hash == expected['audit_campaign_lock_sha256']}"
    )
    if not campaign_equal or campaign_hash != expected["audit_campaign_lock_sha256"]:
        failures.append("campaign lock mismatch")

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
    ]
    usage = Path("/generation-evidence/usage.json")
    print(f"usage_present={usage.exists()}")
    required.append(usage)
    for path in required:
        exists = path.exists()
        readable = path.is_dir() or regular_nonsymlink(path)
        print(f"required_record={path} exists={exists} regular_or_dir={readable}")
        if not exists or not readable:
            failures.append(f"missing or mistyped required record: {path}")

    hash_map = {
        "audit_campaign_lock_sha256": CAMPAIGN_LOCK,
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "canonical_sha256": Path(paths["canonical"]),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": usage,
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
    }
    for key, path in hash_map.items():
        actual = digest(path)
        matches = actual == expected[key]
        print(f"{key} path={path} actual={actual} matches={matches}")
        if not matches:
            failures.append(f"hash mismatch: {key}")

    # generation-result.json records the exact trace member hash, while
    # audit-input records an aggregate directory hash whose launcher algorithm
    # is not assumed here.
    stage_result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    evidence_hashes = stage_result["outputs"]["evidence"]
    for relative, recorded in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        actual = digest(path)
        matches = actual == recorded
        print(
            f"generation_member={relative} actual={actual} "
            f"recorded={recorded} matches={matches}"
        )
        if not matches:
            failures.append(f"generation member mismatch: {relative}")

    candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
    semantics_equal = candidate_semantics == trusted_semantics
    symlinks = [
        name
        for name, (kind, _) in candidate_semantics.items()
        if kind == "symlink"
    ]
    print(f"candidate_semantics_entries={len(candidate_semantics)}")
    print(f"trusted_semantics_entries={len(trusted_semantics)}")
    print(f"semantics_manifests_equal={semantics_equal}")
    print(f"candidate_semantics_symlinks={symlinks}")
    if not semantics_equal or symlinks:
        failures.append("supplied semantics tree mismatch")
    for relative, (kind, value) in candidate_semantics.items():
        if kind == "file":
            print(f"semantics_file={relative} sha256={value}")

    prompt_equal = (
        Path("/candidate/prompt.py").read_bytes()
        == Path(paths["trusted_prompt"]).read_bytes()
    )
    translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path(paths["translator"]).read_bytes()
    )
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not prompt_equal or not translator_equal:
        failures.append("candidate prompt or translator mismatch")

    proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in proof_artifacts:
        path = Path("/candidate") / name
        valid = path.exists() and regular_nonsymlink(path)
        print(f"proof_artifact={name} regular_nonsymlink={valid}")
        if not valid:
            failures.append(f"missing or mistyped proof artifact: {name}")

    trace_files = sorted(Path(paths["generation_trace"]).rglob("*.jsonl"))
    trace_lines = 0
    trace_types: dict[str, int] = {}
    for trace_file in trace_files:
        for raw in trace_file.read_text(encoding="utf-8").splitlines():
            record = json.loads(raw)
            trace_lines += 1
            trace_type = record.get("type", "<missing>")
            trace_types[trace_type] = trace_types.get(trace_type, 0) + 1
    print(f"structured_trace_files={[str(path) for path in trace_files]}")
    print(f"structured_trace_lines={trace_lines}")
    print(f"structured_trace_types={dict(sorted(trace_types.items()))}")

    declared_container_paths_exist = {
        key: Path(value).exists()
        for key, value in paths.items()
        if value.startswith("/")
    }
    print(f"declared_container_paths_exist={declared_container_paths_exist}")
    if not all(declared_container_paths_exist.values()):
        failures.append("launcher-declared container path absent")

    print(f"failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
