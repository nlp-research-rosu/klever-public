#!/usr/bin/env python3
"""Independent pipeline-v3 mount and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN_RESULT = Path("/generation-result.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({stat.S_IFMT(mode):o})"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            digest = sha256(path) if entry_kind == "file" else None
            result[rel] = (entry_kind, digest)
    return result


def reviewer_tree_digest(root: Path) -> tuple[str, int]:
    """Portable audit digest over relative path, type, mode, and file bytes."""
    h = hashlib.sha256()
    count = 0
    paths = [root, *sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix())]
    for path in paths:
        rel = "." if path == root else path.relative_to(root).as_posix()
        entry_kind = kind(path)
        mode = stat.S_IMODE(path.lstat().st_mode)
        line = f"{rel}\\0{entry_kind}\\0{mode:o}\\0".encode()
        h.update(line)
        if entry_kind == "file":
            h.update(bytes.fromhex(sha256(path)))
        elif entry_kind == "symlink":
            h.update(os.readlink(path).encode())
        h.update(b"\\0")
        count += 1
    return h.hexdigest(), count


def report_hash(label: str, path: Path, expected: str | None) -> bool:
    actual = sha256(path)
    ok = expected == actual if expected is not None else True
    print(f"HASH {label}: expected={expected or '(none)'} actual={actual} ok={ok}")
    return ok


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
result = json.loads(GEN_RESULT.read_text())
hashes = audit["hashes"]

print("COMMAND: python3 /audit-output/evidence/stage1_integrity.py")
print(f"record_layout={audit.get('record_layout')}")
print(f"semantics_mode={audit.get('semantics_mode')}")
print(f"campaign_block_equals_lock={audit.get('audit_campaign') == lock}")

required = [
    AUDIT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    GEN_RESULT,
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
    Path("/candidate"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/reference/reference-semantics"),
]
for path in required:
    readable = os.access(path, os.R_OK)
    print(f"REQUIRED {path}: exists={path.exists()} kind={kind(path) if path.exists() else 'missing'} readable={readable}")

checks = [
    ("audit_campaign_lock", LOCK, hashes["audit_campaign_lock_sha256"]),
    ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
    ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
    ("stage1_result", GEN_RESULT, hashes["stage1_result_sha256"]),
    ("generation_invocation", Path("/generation-evidence/invocation.json"), hashes["stage1_invocation_sha256"]),
    ("generation_metrics", Path("/generation-evidence/metrics.json"), hashes["generation_metrics_sha256"]),
    ("generation_runtime_metrics", Path("/generation-evidence/runtime-metrics.json"), hashes["generation_runtime_metrics_sha256"]),
    ("generation_usage", Path("/generation-evidence/usage.json"), hashes["generation_usage_sha256"]),
    ("generation_last", Path("/generation-evidence/codex-last.txt"), hashes["generation_codex_last_sha256"]),
    ("generation_output", Path("/generation-evidence/codex-output.log"), hashes["generation_codex_output_sha256"]),
    ("generation_prompt", Path("/generation-evidence/prompt.txt"), hashes["generation_prompt_sha256"]),
    ("canonical", Path("/reference/canonical.py"), hashes["canonical_sha256"]),
    ("trusted_prompt", Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"]),
    ("candidate_prompt", Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"]),
    ("trusted_translator", Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"]),
    ("candidate_translator", Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"]),
]
hash_ok = all(report_hash(*item) for item in checks)

print(f"BYTE candidate_prompt_vs_trusted={Path('/candidate/prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}")
print(f"BYTE candidate_translator_vs_trusted={Path('/candidate/py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}")
candidate_tree_digest, candidate_tree_count = reviewer_tree_digest(Path("/candidate"))
print(f"REVIEWER_TREE candidate entries={candidate_tree_count} sha256={candidate_tree_digest}")

candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
all_rel = sorted(candidate_semantics.keys() | trusted_semantics.keys())
semantics_differences: list[str] = []
for rel in all_rel:
    cand = candidate_semantics.get(rel)
    trusted = trusted_semantics.get(rel)
    if cand != trusted:
        semantics_differences.append(f"{rel}: candidate={cand} trusted={trusted}")
print(f"SEMANTICS candidate_entries={len(candidate_semantics)} trusted_entries={len(trusted_semantics)} differences={len(semantics_differences)}")
candidate_semantics_digest, candidate_semantics_count = reviewer_tree_digest(Path("/candidate/reference-semantics"))
trusted_semantics_digest, trusted_semantics_count = reviewer_tree_digest(Path("/reference/reference-semantics"))
print(
    "REVIEWER_TREE semantics "
    f"candidate_entries={candidate_semantics_count} candidate_sha256={candidate_semantics_digest} "
    f"trusted_entries={trusted_semantics_count} trusted_sha256={trusted_semantics_digest} "
    f"equal={candidate_semantics_digest == trusted_semantics_digest}"
)
for difference in semantics_differences:
    print(f"SEMANTICS_DIFF {difference}")

candidate_symlinks = []
for root, dirs, files in os.walk("/candidate", followlinks=False):
    for name in dirs + files:
        path = Path(root) / name
        if path.is_symlink():
            candidate_symlinks.append(str(path))
print(f"CANDIDATE_SYMLINKS count={len(candidate_symlinks)} paths={candidate_symlinks}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [p for p in trace_files if p.is_file()]
declared_trace = result["outputs"]["evidence"]
trace_hash_ok = True
for path in trace_files:
    rel = path.relative_to("/generation-evidence").as_posix()
    expected = declared_trace.get(rel)
    trace_hash_ok &= report_hash(rel, path, expected)
    counts: Counter[str] = Counter()
    invalid = 0
    lines = 0
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            lines += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                invalid += 1
                continue
            event_type = str(item.get("type", "(missing)"))
            payload_type = ""
            if isinstance(item.get("payload"), dict):
                payload_type = str(item["payload"].get("type", ""))
            counts[event_type + (f"/{payload_type}" if payload_type else "")] += 1
    print(f"TRACE {rel}: lines={lines} invalid_json={invalid} event_counts={dict(sorted(counts.items()))}")

declared_evidence_files = {
    key for key in declared_trace if key.startswith("codex-trace/")
}
actual_evidence_files = {
    path.relative_to("/generation-evidence").as_posix() for path in trace_files
}
print(f"TRACE inventory_matches_result={declared_evidence_files == actual_evidence_files}")

all_ok = (
    audit.get("record_layout") == "pipeline-v3"
    and audit.get("semantics_mode") == "SUPPLIED_SEMANTICS"
    and audit.get("audit_campaign") == lock
    and all(path.exists() and os.access(path, os.R_OK) for path in required)
    and hash_ok
    and not semantics_differences
    and not candidate_symlinks
    and trace_hash_ok
    and declared_evidence_files == actual_evidence_files
)
print(f"STAGE1_INTEGRITY_OK={all_ok}")
