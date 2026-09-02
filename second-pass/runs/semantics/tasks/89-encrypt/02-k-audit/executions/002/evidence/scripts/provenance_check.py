#!/usr/bin/env python3
"""Independent checks over the launcher-owned provenance mounts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def tree_manifest(root: Path):
    result = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            result.append((rel, "symlink", os.readlink(path)))
        elif path.is_dir():
            result.append((rel, "directory", None))
        elif path.is_file():
            result.append((rel, "file", sha256(path)))
        else:
            result.append((rel, "other", None))
    return result


audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
hashes = audit_input["hashes"]

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_json_exact_match={lock == audit_input['audit_campaign']}")
print(
    "campaign_hash_match="
    f"{sha256(LOCK) == hashes['audit_campaign_lock_sha256']}"
)

required_layout_paths = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    required_layout_paths.append(usage)

for path in required_layout_paths:
    print(
        f"required_record path={path} regular_nonsymlink="
        f"{regular_nonsymlink(path)} readable={os.access(path, os.R_OK)}"
    )

recorded_file_hashes = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
for path_text, hash_key in recorded_file_hashes.items():
    path = Path(path_text)
    actual = sha256(path)
    expected = hashes[hash_key]
    print(
        f"recorded_hash path={path} key={hash_key} "
        f"match={actual == expected} actual={actual} expected={expected}"
    )

stage_result = json.loads(
    Path("/generation-result.json").read_text(encoding="utf-8")
)
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
for owner, record in [("stage_result", stage_result), ("invocation", invocation)]:
    for relative, expected in sorted(record["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / relative
        actual = sha256(path)
        print(
            f"{owner}_evidence_hash path={path} match={actual == expected} "
            f"actual={actual} expected={expected}"
        )

trace_paths = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_paths if path.is_file()]
trace_symlinks = [path for path in trace_paths if path.is_symlink()]
jsonl_lines = 0
jsonl_valid = True
for path in trace_files:
    if path.suffix == ".jsonl":
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                json.loads(line)
                jsonl_lines += 1
print(f"trace_file_count={len(trace_files)}")
print(f"trace_symlink_count={len(trace_symlinks)}")
print(f"trace_jsonl_valid={jsonl_valid}")
print(f"trace_jsonl_lines={jsonl_lines}")

candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
print(
    "recursive_semantics_manifest_exact_match="
    f"{candidate_semantics == trusted_semantics}"
)
print(
    "candidate_semantics_symlink_count="
    f"{sum(kind == 'symlink' for _, kind, _ in candidate_semantics)}"
)
print(
    "trusted_semantics_symlink_count="
    f"{sum(kind == 'symlink' for _, kind, _ in trusted_semantics)}"
)
print(
    "candidate_prompt_byte_match="
    f"{Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
)
print(
    "candidate_translator_byte_match="
    f"{Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
)

proof_artifacts = [
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/spec.k"),
    Path("/candidate/verification.k"),
    Path("/candidate/prove.sh"),
]
for path in proof_artifacts:
    print(
        f"proof_artifact path={path} regular_nonsymlink="
        f"{regular_nonsymlink(path)} sha256={sha256(path)}"
    )
