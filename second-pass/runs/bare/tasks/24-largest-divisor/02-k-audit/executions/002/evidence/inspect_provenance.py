#!/usr/bin/env python3
"""Independent checks over launcher-mounted provenance and required records."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


data = json.loads(AUDIT_INPUT.read_text())
paths = {key: Path(value) for key, value in data["container_paths"].items()}
lock = json.loads(paths["audit_campaign_lock"].read_text())

print(f"record_layout={data['record_layout']}")
print(f"semantics_mode={data['semantics_mode']}")
print(f"campaign_lock_equal={lock == data['audit_campaign']}")

checks = {
    "audit_campaign_lock_sha256": paths["audit_campaign_lock"],
    "candidate_prompt_sha256": paths["candidate"] / "prompt.py",
    "candidate_translator_sha256": paths["candidate"] / "py2mpy.py",
    "canonical_sha256": paths["canonical"],
    "generation_codex_last_sha256": paths["generation_last"],
    "generation_codex_output_sha256": paths["generation_output"],
    "generation_metrics_sha256": paths["generation_metrics"],
    "generation_prompt_sha256": paths["generation_root"] / "prompt.txt",
    "generation_usage_sha256": paths["generation_root"] / "usage.json",
    "run_manifest_sha256": paths["run_manifest"],
    "stage1_invocation_sha256": paths["generation_manifest"],
    "stage1_result_sha256": paths["stage1_result"],
    "task_manifest_sha256": paths["task_manifest"],
    "trusted_prompt_sha256": paths["trusted_prompt"],
    "trusted_translator_sha256": paths["translator"],
}

all_match = True
for field, path in checks.items():
    expected = data["hashes"][field]
    actual = digest(path)
    regular = path.is_file() and not path.is_symlink()
    match = actual == expected
    all_match &= regular and match
    print(
        f"{field}: regular_nonsymlink={regular} expected={expected} "
        f"actual={actual} match={match}"
    )

required_legacy_selected = [
    paths["run_manifest"],
    paths["task_manifest"],
    paths["stage1_result"],
    paths["generation_manifest"],
    paths["generation_metrics"],
    paths["generation_root"] / "codex-last.txt",
    paths["generation_root"] / "codex-output.log",
    paths["generation_root"] / "prompt.txt",
    paths["generation_trace"],
]
for path in required_legacy_selected:
    present = path.exists()
    nonsymlink = present and not path.is_symlink()
    readable = present and os.access(path, os.R_OK)
    print(
        f"required={path} present={present} nonsymlink={nonsymlink} "
        f"readable={readable}"
    )
    all_match &= present and nonsymlink and readable

reference_semantics = Path("/reference/reference-semantics")
print(f"reference_semantics_absent={not reference_semantics.exists()}")
all_match &= not reference_semantics.exists()

prompt_equal = (
    (paths["candidate"] / "prompt.py").read_bytes()
    == paths["trusted_prompt"].read_bytes()
)
translator_equal = (
    (paths["candidate"] / "py2mpy.py").read_bytes()
    == paths["translator"].read_bytes()
)
print(f"candidate_prompt_byte_equal={prompt_equal}")
print(f"candidate_translator_byte_equal={translator_equal}")
all_match &= prompt_equal and translator_equal

print("candidate_files:")
for path in sorted(paths["candidate"].iterdir()):
    if path.is_file() and not path.is_symlink():
        print(f"  {path.name} sha256={digest(path)} mode={path.stat().st_mode & 0o777:o}")
    else:
        print(f"  INVALID_TYPE {path}")
        all_match = False

print(f"OVERALL_OK={all_match}")
raise SystemExit(0 if all_match else 1)
