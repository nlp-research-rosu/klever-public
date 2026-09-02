#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entries(root: Path) -> dict[str, tuple[str, str | None]]:
    found: dict[str, tuple[str, str | None]] = {}
    for base, dirnames, filenames in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirnames + filenames):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                found[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                found[rel] = ("directory", None)
            elif path.is_file():
                found[rel] = ("file", sha256_file(path))
            else:
                found[rel] = ("other", None)
    return found


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

print("record_layout:", audit.get("record_layout"))
print("semantics_mode:", audit.get("semantics_mode"))
print("campaign_block_equals_lock:", audit.get("audit_campaign") == lock)

recorded = audit["hashes"]
checks = {
    "audit_campaign_lock_sha256": LOCK,
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_runtime_metrics_sha256": Path(
        "/generation-evidence/runtime-metrics.json"
    ),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
}

all_hashes_ok = True
for key, path in checks.items():
    actual = sha256_file(path) if path.is_file() else "MISSING_OR_NOT_FILE"
    expected = recorded.get(key)
    ok = actual == expected
    all_hashes_ok &= ok
    print(f"{key}: ok={ok} actual={actual} expected={expected}")
print("all_declared_file_hashes_ok:", all_hashes_ok)

required_pipeline_v3 = [
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/runtime-metrics.json",
    "/generation-evidence/usage.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
]
for raw in required_pipeline_v3:
    path = Path(raw)
    print(
        f"required_record {raw}: exists={path.exists()} "
        f"is_file={path.is_file()} symlink={path.is_symlink()} readable={os.access(path, os.R_OK)}"
    )

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(p for p in trace_root.rglob("*") if p.is_file())
trace_symlinks = sorted(p for p in trace_root.rglob("*") if p.is_symlink())
print("trace_file_count:", len(trace_files))
for path in trace_files:
    print(
        "trace_file:",
        path.relative_to(trace_root).as_posix(),
        "sha256=" + sha256_file(path),
        "size=" + str(path.stat().st_size),
    )
print("trace_symlink_count:", len(trace_symlinks))

candidate_sem = entries(Path("/candidate/reference-semantics"))
trusted_sem = entries(Path("/reference/reference-semantics"))
missing = sorted(set(trusted_sem) - set(candidate_sem))
additional = sorted(set(candidate_sem) - set(trusted_sem))
changed = sorted(
    path
    for path in set(candidate_sem) & set(trusted_sem)
    if candidate_sem[path] != trusted_sem[path]
)
print("candidate_semantics_entry_count:", len(candidate_sem))
print("trusted_semantics_entry_count:", len(trusted_sem))
print("candidate_semantics_missing:", missing)
print("candidate_semantics_additional:", additional)
print("candidate_semantics_changed_or_mistyped:", changed)
print(
    "candidate_semantics_exact_recursive_match:",
    not missing and not additional and not changed,
)

for root in [
    Path("/candidate"),
    Path("/reference"),
    Path("/generation-evidence"),
]:
    symlinks = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_symlink())
    others = sorted(
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if not p.is_symlink() and not p.is_dir() and not p.is_file()
    )
    print(f"{root}_symlinks:", symlinks)
    print(f"{root}_other_types:", others)
