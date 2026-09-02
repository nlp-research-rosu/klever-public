#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as inp:
        for chunk in iter(lambda: inp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def type_name(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({mode:o})"


def walk_entries(root: Path):
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs.sort()
        files.sort()
        for name in dirs + files:
            p = Path(parent) / name
            yield p.relative_to(root).as_posix(), p


def compare_trees(left: Path, right: Path):
    left_items = {rel: path for rel, path in walk_entries(left)}
    right_items = {rel: path for rel, path in walk_entries(right)}
    diffs = []
    for rel in sorted(left_items.keys() | right_items.keys()):
        lp = left_items.get(rel)
        rp = right_items.get(rel)
        if lp is None:
            diffs.append((rel, "missing-left", None, type_name(rp)))
            continue
        if rp is None:
            diffs.append((rel, "additional-left", type_name(lp), None))
            continue
        lt = type_name(lp)
        rt = type_name(rp)
        if lt != rt:
            diffs.append((rel, "type", lt, rt))
        elif lt == "regular":
            lh = sha256_file(lp)
            rh = sha256_file(rp)
            if lh != rh:
                diffs.append((rel, "content", lh, rh))
        elif lt == "symlink":
            diffs.append((rel, "symlink-forbidden", os.readlink(lp), os.readlink(rp)))
    return diffs


with AUDIT.open() as inp:
    audit = json.load(inp)
with LOCK.open() as inp:
    lock = json.load(inp)

print("record_layout", audit.get("record_layout"))
print("semantics_mode", audit.get("semantics_mode"))
print("campaign_object_equal", audit["audit_campaign"] == lock)
print("lock_sha256", sha256_file(LOCK))
print("lock_sha256_declared", audit["hashes"]["audit_campaign_lock_sha256"])
print("lock_hash_match", sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"])

required = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
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
print("required_records")
for p in required:
    exists = p.exists()
    readable = os.access(p, os.R_OK)
    t = type_name(p) if os.path.lexists(p) else "absent"
    print(f"  {p}: exists={exists} readable={readable} type={t}")

hash_checks = [
    ("/reference/canonical.py", "canonical_sha256"),
    ("/reference/prompt.py", "trusted_prompt_sha256"),
    ("/reference/py2mpy.py", "trusted_translator_sha256"),
    ("/candidate/prompt.py", "candidate_prompt_sha256"),
    ("/candidate/py2mpy.py", "candidate_translator_sha256"),
    ("/run.json", "run_manifest_sha256"),
    ("/task.json", "task_manifest_sha256"),
    ("/generation-result.json", "stage1_result_sha256"),
    ("/generation-evidence/invocation.json", "stage1_invocation_sha256"),
    ("/generation-evidence/metrics.json", "generation_metrics_sha256"),
    ("/generation-evidence/runtime-metrics.json", "generation_runtime_metrics_sha256"),
    ("/generation-evidence/usage.json", "generation_usage_sha256"),
    ("/generation-evidence/codex-last.txt", "generation_codex_last_sha256"),
    ("/generation-evidence/codex-output.log", "generation_codex_output_sha256"),
    ("/generation-evidence/prompt.txt", "generation_prompt_sha256"),
]
print("declared_file_hashes")
for raw, key in hash_checks:
    p = Path(raw)
    actual = sha256_file(p)
    expected = audit["hashes"][key]
    print(f"  {raw}: {actual} declared={expected} match={actual == expected}")

with Path("/generation-result.json").open() as inp:
    result = json.load(inp)
print("generation_result_evidence_hashes")
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    p = Path("/generation-evidence") / rel
    actual = sha256_file(p)
    print(f"  {rel}: {actual} declared={expected} match={actual == expected}")

prompt_same = Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
translator_same = Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identical", prompt_same)
print("candidate_translator_byte_identical", translator_same)

tree_diffs = compare_trees(
    Path("/candidate/reference-semantics"),
    Path("/reference/reference-semantics"),
)
print("reference_semantics_tree_diff_count", len(tree_diffs))
for diff in tree_diffs:
    print("  tree_diff", diff)

symlinks = []
for root in (Path("/candidate"), Path("/reference"), Path("/generation-evidence")):
    for rel, p in walk_entries(root):
        if p.is_symlink():
            symlinks.append(str(root / rel))
print("symlink_count_all_mounted_inputs", len(symlinks))
for p in symlinks:
    print("  symlink", p)
