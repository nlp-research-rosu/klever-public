#!/usr/bin/env python3
"""Independent checks of launcher records and mounted provenance inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def regular_readable(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    return stat.S_ISREG(mode) and not stat.S_ISLNK(mode) and os.access(path, os.R_OK)


def tree_manifest(root: Path) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            result.append((relative, "symlink", os.readlink(path)))
        elif stat.S_ISDIR(mode):
            result.append((relative, "directory", ""))
        elif stat.S_ISREG(mode):
            result.append((relative, "file", digest(path)))
        else:
            result.append((relative, f"other:{stat.S_IFMT(mode):o}", ""))
    return result


def reviewer_tree_digest(manifest: list[tuple[str, str, str]]) -> str:
    # This reviewer-defined digest is supplementary. Exact entry/type/content
    # equality below is the integrity decision, independent of launcher hashing.
    encoded = json.dumps(manifest, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(encoded).hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(CAMPAIGN_LOCK.read_text())
print(f"record_layout={audit.get('record_layout')}")
print(f"semantics_mode={audit.get('semantics_mode')}")
print(f"campaign_structural_equal={audit.get('audit_campaign') == lock}")

expected_file_hashes = {
    CAMPAIGN_LOCK: audit["hashes"]["audit_campaign_lock_sha256"],
    REFERENCE / "canonical.py": audit["hashes"]["canonical_sha256"],
    REFERENCE / "prompt.py": audit["hashes"]["trusted_prompt_sha256"],
    REFERENCE / "py2mpy.py": audit["hashes"]["trusted_translator_sha256"],
    CANDIDATE / "prompt.py": audit["hashes"]["candidate_prompt_sha256"],
    CANDIDATE / "py2mpy.py": audit["hashes"]["candidate_translator_sha256"],
    Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
    Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
    Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
    GENERATION / "invocation.json": audit["hashes"]["stage1_invocation_sha256"],
    GENERATION / "metrics.json": audit["hashes"]["generation_metrics_sha256"],
    GENERATION / "runtime-metrics.json": audit["hashes"]["generation_runtime_metrics_sha256"],
    GENERATION / "usage.json": audit["hashes"]["generation_usage_sha256"],
    GENERATION / "codex-last.txt": audit["hashes"]["generation_codex_last_sha256"],
    GENERATION / "codex-output.log": audit["hashes"]["generation_codex_output_sha256"],
    GENERATION / "prompt.txt": audit["hashes"]["generation_prompt_sha256"],
}

all_files_ok = True
for path, expected in expected_file_hashes.items():
    is_regular = regular_readable(path)
    actual = digest(path) if is_regular else "UNAVAILABLE"
    match = is_regular and actual == expected
    all_files_ok &= match
    print(
        f"FILE path={path} regular_readable={is_regular} "
        f"sha256={actual} expected={expected} match={match}"
    )

trace_result = json.loads(Path("/generation-result.json").read_text())
trace_expected = {
    key: value
    for key, value in trace_result["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
}
trace_ok = True
for relative, expected in sorted(trace_expected.items()):
    path = GENERATION / relative
    is_regular = regular_readable(path)
    actual = digest(path) if is_regular else "UNAVAILABLE"
    match = is_regular and actual == expected
    trace_ok &= match
    print(
        f"TRACE path={path} regular_readable={is_regular} "
        f"sha256={actual} expected={expected} match={match}"
    )

prompt_equal = (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
translator_equal = (
    (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()
)
candidate_semantics = tree_manifest(CANDIDATE / "reference-semantics")
trusted_semantics = tree_manifest(REFERENCE / "reference-semantics")
semantics_equal = candidate_semantics == trusted_semantics
print(f"candidate_prompt_byte_equal={prompt_equal}")
print(f"candidate_translator_byte_equal={translator_equal}")
print(f"supplied_semantics_exact_manifest_equal={semantics_equal}")
print(f"candidate_semantics_entries={len(candidate_semantics)}")
print(f"trusted_semantics_entries={len(trusted_semantics)}")
print(f"candidate_semantics_reviewer_sha256={reviewer_tree_digest(candidate_semantics)}")
print(f"trusted_semantics_reviewer_sha256={reviewer_tree_digest(trusted_semantics)}")
for item in trusted_semantics:
    print(f"SEMANTICS_ENTRY type={item[1]} path={item[0]} sha256_or_target={item[2]}")

required_candidate = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
candidate_required_ok = True
for relative in required_candidate:
    path = CANDIDATE / relative
    ok = regular_readable(path)
    candidate_required_ok &= ok
    print(f"CANDIDATE_REQUIRED path={path} regular_readable={ok}")

overall = (
    audit.get("record_layout") == "pipeline-v3"
    and audit.get("semantics_mode") == "SUPPLIED_SEMANTICS"
    and audit.get("mount_reference_semantics") is True
    and audit.get("audit_campaign") == lock
    and all_files_ok
    and trace_ok
    and prompt_equal
    and translator_equal
    and semantics_equal
    and candidate_required_ok
)
print(f"PROVENANCE_GATE_OK={overall}")
raise SystemExit(0 if overall else 1)
