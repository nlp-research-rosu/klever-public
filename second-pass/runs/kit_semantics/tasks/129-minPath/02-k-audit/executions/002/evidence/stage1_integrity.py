#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from pathlib import Path

AUDIT = Path("/audit-input.json")
with AUDIT.open("rb") as stream:
    audit_bytes = stream.read()
audit = json.loads(audit_bytes)

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def path_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode): return "file"
    if stat.S_ISDIR(mode): return "directory"
    if stat.S_ISLNK(mode): return "symlink"
    return f"other:{mode:o}"

def file_manifest(root: Path):
    result = []
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs.sort()
        files.sort()
        for name in dirs + files:
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            kind = path_kind(path)
            entry = {"path": rel, "kind": kind}
            if kind == "file":
                entry.update(size=path.stat().st_size, sha256=digest(path))
            elif kind == "symlink":
                entry["target"] = os.readlink(path)
            result.append(entry)
    return result

def independent_tree_digest(entries) -> str:
    h = hashlib.sha256()
    for entry in entries:
        h.update(entry["path"].encode())
        h.update(b"\0")
        h.update(entry["kind"].encode())
        h.update(b"\0")
        if entry["kind"] == "file":
            h.update(entry["sha256"].encode())
            h.update(b"\0")
        elif entry["kind"] == "symlink":
            h.update(entry["target"].encode())
            h.update(b"\0")
    return h.hexdigest()

print(f"audit_input_sha256={hashlib.sha256(audit_bytes).hexdigest()}")
print(f"record_layout={audit.get('record_layout')}")
print(f"semantics_mode={audit.get('semantics_mode')}")

campaign_path = Path(audit["container_paths"]["audit_campaign_lock"])
campaign = json.loads(campaign_path.read_bytes())
print(f"campaign_kind={path_kind(campaign_path)}")
print(f"campaign_hash_actual={digest(campaign_path)}")
print(f"campaign_hash_recorded={audit['hashes']['audit_campaign_lock_sha256']}")
print(f"campaign_block_equal={campaign == audit['audit_campaign']}")

file_hash_checks = {
    "canonical": (Path(audit["container_paths"]["canonical"]), "canonical_sha256"),
    "trusted_prompt": (Path(audit["container_paths"]["trusted_prompt"]), "trusted_prompt_sha256"),
    "translator": (Path(audit["container_paths"]["translator"]), "trusted_translator_sha256"),
    "candidate_prompt": (Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
    "candidate_translator": (Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
    "run_manifest": (Path(audit["container_paths"]["run_manifest"]), "run_manifest_sha256"),
    "task_manifest": (Path(audit["container_paths"]["task_manifest"]), "task_manifest_sha256"),
    "stage1_result": (Path(audit["container_paths"]["stage1_result"]), "stage1_result_sha256"),
    "invocation": (Path(audit["container_paths"]["generation_manifest"]), "stage1_invocation_sha256"),
    "metrics": (Path(audit["container_paths"]["generation_metrics"]), "generation_metrics_sha256"),
    "runtime_metrics": (Path("/generation-evidence/runtime-metrics.json"), "generation_runtime_metrics_sha256"),
    "usage": (Path("/generation-evidence/usage.json"), "generation_usage_sha256"),
    "generation_last": (Path(audit["container_paths"]["generation_last"]), "generation_codex_last_sha256"),
    "generation_output": (Path(audit["container_paths"]["generation_output"]), "generation_codex_output_sha256"),
    "generation_prompt": (Path("/generation-evidence/prompt.txt"), "generation_prompt_sha256"),
}
for label, (path, key) in file_hash_checks.items():
    exists = path.exists()
    readable = os.access(path, os.R_OK)
    kind = path_kind(path) if exists or path.is_symlink() else "missing"
    actual = digest(path) if kind == "file" and readable else "UNAVAILABLE"
    recorded = audit["hashes"].get(key, "UNRECORDED")
    print(f"file={label} path={path} exists={exists} readable={readable} kind={kind} hash_match={actual == recorded} actual={actual} recorded={recorded}")

invocation = json.loads(Path("/generation-evidence/invocation.json").read_bytes())
for rel, recorded in sorted(invocation["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    actual = digest(path) if path.is_file() and not path.is_symlink() else "UNAVAILABLE"
    print(f"invocation_evidence={rel} kind={path_kind(path) if path.exists() or path.is_symlink() else 'missing'} hash_match={actual == recorded} actual={actual} recorded={recorded}")

trusted_sem = Path("/reference/reference-semantics")
candidate_sem = Path("/candidate/reference-semantics")
trusted_manifest = file_manifest(trusted_sem)
candidate_sem_manifest = file_manifest(candidate_sem)
print(f"trusted_semantics_entries={len(trusted_manifest)} candidate_semantics_entries={len(candidate_sem_manifest)}")
print(f"trusted_semantics_symlinks={sum(e['kind'] == 'symlink' for e in trusted_manifest)} candidate_semantics_symlinks={sum(e['kind'] == 'symlink' for e in candidate_sem_manifest)}")
print(f"semantics_manifest_equal={trusted_manifest == candidate_sem_manifest}")
print(f"trusted_semantics_independent_tree_sha256={independent_tree_digest(trusted_manifest)}")
print(f"candidate_semantics_independent_tree_sha256={independent_tree_digest(candidate_sem_manifest)}")

candidate_manifest = file_manifest(Path("/candidate"))
trace_manifest = file_manifest(Path("/generation-evidence/codex-trace"))
print(f"candidate_entries={len(candidate_manifest)} candidate_symlinks={sum(e['kind'] == 'symlink' for e in candidate_manifest)}")
print(f"candidate_independent_tree_sha256={independent_tree_digest(candidate_manifest)}")
print(f"trace_entries={len(trace_manifest)} trace_symlinks={sum(e['kind'] == 'symlink' for e in trace_manifest)}")
print(f"trace_independent_tree_sha256={independent_tree_digest(trace_manifest)}")

print(f"prompt_cmp={Path('/reference/prompt.py').read_bytes() == Path('/candidate/prompt.py').read_bytes()}")
print(f"translator_cmp={Path('/reference/py2mpy.py').read_bytes() == Path('/candidate/py2mpy.py').read_bytes()}")
