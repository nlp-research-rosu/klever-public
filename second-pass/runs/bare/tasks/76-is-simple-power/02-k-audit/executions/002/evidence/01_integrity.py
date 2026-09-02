#!/usr/bin/env python3
"""Independent mounted-input and provenance integrity audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def entry(path: Path) -> dict[str, object]:
    st = path.lstat()
    mode = st.st_mode
    return {
        "path": str(path),
        "kind": (
            "symlink"
            if stat.S_ISLNK(mode)
            else "file"
            if stat.S_ISREG(mode)
            else "directory"
            if stat.S_ISDIR(mode)
            else "other"
        ),
        "mode": oct(stat.S_IMODE(mode)),
        "size": st.st_size,
        "sha256": sha256(path) if stat.S_ISREG(mode) else None,
    }


def regular_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except FileNotFoundError:
        return False


def pipeline_tree_sha256(root: Path) -> str:
    """Reproduce the mounted pipeline's length-delimited tree hash."""
    h = hashlib.sha256()
    entries = []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((relative, "file", path))
        else:
            raise ValueError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
        h.update(kind.encode() + b"\0")
        if kind == "file":
            h.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(chunk)
    return h.hexdigest()


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())

required = [
    AUDIT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
if Path("/generation-evidence/usage.json").exists():
    required.append(Path("/generation-evidence/usage.json"))

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*.jsonl")) if trace_root.is_dir() else []
required.extend(trace_files)

all_required_regular = all(regular_file(path) for path in required)
all_required_readable = all(os.access(path, os.R_OK) for path in required)
no_required_symlinks = all(not path.is_symlink() for path in required)

hash_expectations = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}

checks: dict[str, object] = {}
for name, key in hash_expectations.items():
    path = Path(name)
    expected = audit["hashes"].get(key)
    actual = sha256(path) if regular_file(path) else None
    checks[name] = {"hash_key": key, "expected": expected, "actual": actual, "match": expected == actual}

invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
trace_hash_checks = {}
for path in trace_files:
    rel = path.relative_to("/generation-evidence").as_posix()
    expected = invocation["outputs"]["evidence"].get(rel)
    actual = sha256(path)
    trace_hash_checks[rel] = {"expected": expected, "actual": actual, "match": expected == actual}

trace_events = 0
trace_parse_errors = []
trace_types: dict[str, int] = {}
for path in trace_files:
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            trace_events += 1
            try:
                obj = json.loads(line)
                typ = str(obj.get("type"))
                trace_types[typ] = trace_types.get(typ, 0) + 1
            except Exception as err:  # evidence only
                trace_parse_errors.append(f"{path}:{line_number}: {err}")

candidate_entries = []
candidate_symlinks = []
for path in sorted(Path("/candidate").rglob("*")):
    info = entry(path)
    candidate_entries.append(info)
    if info["kind"] == "symlink":
        candidate_symlinks.append(str(path))

result = {
    "declared_record_layout": audit.get("record_layout"),
    "declared_semantics_mode": audit.get("semantics_mode"),
    "required_records": [entry(path) if path.exists() else {"path": str(path), "kind": "missing"} for path in required],
    "required_gate": {
        "all_regular": all_required_regular,
        "all_readable": all_required_readable,
        "no_symlinks": no_required_symlinks,
        "trace_file_count": len(trace_files),
    },
    "campaign": {
        "block_equals_lock": audit["audit_campaign"] == lock,
        "recorded_lock_hash": audit["hashes"]["audit_campaign_lock_sha256"],
        "mounted_lock_hash": sha256(LOCK),
        "hash_matches": audit["hashes"]["audit_campaign_lock_sha256"] == sha256(LOCK),
    },
    "hash_checks": checks,
    "trace_hash_checks": trace_hash_checks,
    "trace_read": {
        "events": trace_events,
        "top_level_types": trace_types,
        "json_parse_errors": trace_parse_errors,
    },
    "source_identity": {
        "candidate_prompt_byte_identical": Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes(),
        "candidate_translator_byte_identical": Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes(),
    },
    "semantics_boundary": {
        "trusted_reference_semantics_lexists": os.path.lexists("/reference/reference-semantics"),
        "candidate_reference_semantics_lexists": os.path.lexists("/candidate/reference-semantics"),
    },
    "candidate_mount": {
        "root_is_real_directory": Path("/candidate").is_dir() and not Path("/candidate").is_symlink(),
        "symlinks": candidate_symlinks,
        "entries": candidate_entries,
    },
    "independent_pipeline_tree_hashes": {
        "candidate": {
            "actual": pipeline_tree_sha256(Path("/candidate")),
            "invocation_retained_workspace": invocation["retained_workspace_sha256"],
            "generation_result_workspace": json.loads(
                Path("/generation-result.json").read_text()
            )["outputs"]["workspace_sha256"],
            "all_match": pipeline_tree_sha256(Path("/candidate"))
            == invocation["retained_workspace_sha256"]
            == json.loads(Path("/generation-result.json").read_text())["outputs"]["workspace_sha256"],
            "launcher_recorded_other_aggregate": audit["hashes"]["candidate_tree_sha256"],
        },
        "structured_trace": {
            "actual": pipeline_tree_sha256(trace_root),
            "usage_source_trace": usage["source_trace_sha256"],
            "match": pipeline_tree_sha256(trace_root) == usage["source_trace_sha256"],
            "launcher_recorded_other_aggregate": audit["hashes"]["generation_codex_trace_sha256"],
        },
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
