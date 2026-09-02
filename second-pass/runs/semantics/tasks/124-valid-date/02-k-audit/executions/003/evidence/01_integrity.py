#!/usr/bin/env python3
"""Independent integrity checks for audit 124-valid-date."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def regular(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def inventory(root: Path) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries.append(("symlink", rel, os.readlink(path)))
        elif stat.S_ISDIR(mode):
            entries.append(("directory", rel, ""))
        elif stat.S_ISREG(mode):
            entries.append(("file", rel, sha256(path)))
        else:
            entries.append(("other", rel, oct(mode)))
    return entries


def independent_tree_digest(entries: list[tuple[str, str, str]]) -> str:
    """Reviewer-local canonical digest; not assumed to be launcher's algorithm."""
    h = hashlib.sha256()
    for kind, rel, value in entries:
        h.update(kind.encode())
        h.update(b"\0")
        h.update(rel.encode())
        h.update(b"\0")
        h.update(value.encode())
        h.update(b"\n")
    return h.hexdigest()


with AUDIT_INPUT.open() as stream:
    audit = json.load(stream)
with Path("/audit-campaign-lock.json").open() as stream:
    lock = json.load(stream)

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_equal={lock == audit['audit_campaign']}")

required_regular = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
for path in required_regular:
    print(f"required_regular {path}={regular(path)}")

required_dirs = [
    Path("/candidate"),
    Path("/reference/reference-semantics"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_dirs:
    ok = path.is_dir() and not path.is_symlink()
    print(f"required_directory {path}={ok}")

recorded_file_hashes = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/reference/canonical.py": "canonical_sha256",
}
for name, key in recorded_file_hashes.items():
    actual = sha256(Path(name))
    expected = audit["hashes"][key]
    print(f"hash {name} actual={actual} expected={expected} match={actual == expected}")

with Path("/generation-result.json").open() as stream:
    generation_result = json.load(stream)
declared_trace = {
    rel: digest
    for rel, digest in generation_result["outputs"]["evidence"].items()
    if rel.startswith("codex-trace/")
}
actual_trace_files = sorted(
    p for p in Path("/generation-evidence/codex-trace").rglob("*") if p.is_file()
)
actual_trace_rel = {
    "codex-trace/" + p.relative_to("/generation-evidence/codex-trace").as_posix()
    for p in actual_trace_files
}
print(f"trace_declared_files={sorted(declared_trace)}")
print(f"trace_actual_files={sorted(actual_trace_rel)}")
print(f"trace_file_set_equal={set(declared_trace) == actual_trace_rel}")

trace_type_counts: Counter[str] = Counter()
payload_type_counts: Counter[str] = Counter()
trace_lines = 0
for path in actual_trace_files:
    rel = "codex-trace/" + path.relative_to("/generation-evidence/codex-trace").as_posix()
    digest = sha256(path)
    print(
        f"trace_hash {rel} actual={digest} "
        f"expected={declared_trace.get(rel)} match={digest == declared_trace.get(rel)}"
    )
    with path.open() as stream:
        for line_no, line in enumerate(stream, 1):
            obj = json.loads(line)
            trace_lines += 1
            trace_type_counts[obj.get("type", "<missing>")] += 1
            payload = obj.get("payload")
            if isinstance(payload, dict):
                payload_type_counts[payload.get("type", "<missing>")] += 1
print(f"trace_json_lines={trace_lines}")
print(f"trace_top_level_types={dict(sorted(trace_type_counts.items()))}")
print(f"trace_payload_types={dict(sorted(payload_type_counts.items()))}")

candidate_prompt_match = Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
candidate_translator_match = Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print(f"candidate_prompt_byte_equal={candidate_prompt_match}")
print(f"candidate_translator_byte_equal={candidate_translator_match}")

candidate_semantics = inventory(Path("/candidate/reference-semantics"))
trusted_semantics = inventory(Path("/reference/reference-semantics"))
print(f"candidate_semantics_entries={len(candidate_semantics)}")
print(f"trusted_semantics_entries={len(trusted_semantics)}")
print(f"semantics_inventories_equal={candidate_semantics == trusted_semantics}")
print(
    "candidate_semantics_reviewer_digest="
    + independent_tree_digest(candidate_semantics)
)
print(
    "trusted_semantics_reviewer_digest="
    + independent_tree_digest(trusted_semantics)
)
for entry in trusted_semantics:
    print("trusted_semantics_entry " + " ".join(entry))

for root in [
    Path("/candidate"),
    Path("/reference"),
    Path("/generation-evidence"),
]:
    bad = [entry for entry in inventory(root) if entry[0] in {"symlink", "other"}]
    print(f"special_entries {root} count={len(bad)} entries={bad}")

assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert lock == audit["audit_campaign"]
assert all(regular(path) for path in required_regular)
assert all(path.is_dir() and not path.is_symlink() for path in required_dirs)
assert candidate_prompt_match
assert candidate_translator_match
assert candidate_semantics == trusted_semantics
assert set(declared_trace) == actual_trace_rel
print("INTEGRITY_CHECK=PASS")
