#!/usr/bin/env python3
"""Independent hash/type checks for launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def report_file(label: str, path: Path, expected: str | None = None) -> bool:
    exists = path.exists()
    regular = path.is_file()
    symlink = path.is_symlink()
    print(f"{label}: path={path} exists={exists} regular={regular} symlink={symlink}")
    if not exists or not regular or symlink:
        return False
    actual = sha256_file(path)
    print(f"  sha256={actual}")
    if expected is not None:
        print(f"  expected={expected} match={actual == expected}")
        return actual == expected
    return True


def sha256_tree(path: Path) -> str:
    """Pipeline-contract tree digest, independently implemented here."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [path]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            child_path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = child_path.relative_to(path).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", child_path))
                pending.append(child_path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", child_path))
            else:
                raise RuntimeError(f"unsupported tree entry: {child_path}")
    for relative, kind, child_path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = child_path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


with AUDIT_INPUT.open(encoding="utf-8") as stream:
    record = json.load(stream)
hashes = record["hashes"]

ok = True
ok &= report_file("audit_input", AUDIT_INPUT)
ok &= report_file(
    "campaign_lock",
    Path(record["container_paths"]["audit_campaign_lock"]),
    hashes["audit_campaign_lock_sha256"],
)
with Path(record["container_paths"]["audit_campaign_lock"]).open(encoding="utf-8") as stream:
    lock = json.load(stream)
campaign_equal = lock == record["audit_campaign"]
print(f"campaign_lock_equals_audit_campaign={campaign_equal}")
ok &= campaign_equal

checks = [
    ("run_manifest", "/run.json", "run_manifest_sha256"),
    ("task_manifest", "/task.json", "task_manifest_sha256"),
    ("stage1_result", "/generation-result.json", "stage1_result_sha256"),
    (
        "generation_invocation",
        "/generation-evidence/invocation.json",
        "stage1_invocation_sha256",
    ),
    ("generation_metrics", "/generation-evidence/metrics.json", "generation_metrics_sha256"),
    ("generation_usage", "/generation-evidence/usage.json", "generation_usage_sha256"),
    ("generation_last", "/generation-evidence/codex-last.txt", "generation_codex_last_sha256"),
    (
        "generation_output",
        "/generation-evidence/codex-output.log",
        "generation_codex_output_sha256",
    ),
    ("generation_prompt", "/generation-evidence/prompt.txt", "generation_prompt_sha256"),
    ("canonical", "/reference/canonical.py", "canonical_sha256"),
    ("trusted_prompt", "/reference/prompt.py", "trusted_prompt_sha256"),
    ("trusted_translator", "/reference/py2mpy.py", "trusted_translator_sha256"),
    ("candidate_prompt", "/candidate/prompt.py", "candidate_prompt_sha256"),
    ("candidate_translator", "/candidate/py2mpy.py", "candidate_translator_sha256"),
]
for label, name, key in checks:
    ok &= report_file(label, Path(name), hashes[key])

with Path("/generation-result.json").open(encoding="utf-8") as stream:
    generation_result = json.load(stream)
for relative, expected in generation_result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    if path.is_file():
        ok &= report_file(f"generation_result_evidence:{relative}", path, expected)

candidate_pipeline_digest = sha256_tree(Path("/candidate"))
recorded_workspace_digest = generation_result["outputs"]["workspace_sha256"]
print(
    f"candidate_pipeline_tree_sha256={candidate_pipeline_digest}"
    f" generation_result_workspace_sha256={recorded_workspace_digest}"
    f" match={candidate_pipeline_digest == recorded_workspace_digest}"
)
ok &= candidate_pipeline_digest == recorded_workspace_digest

with Path("/generation-evidence/usage.json").open(encoding="utf-8") as stream:
    usage = json.load(stream)
trace_pipeline_digest = sha256_tree(Path("/generation-evidence/codex-trace"))
usage_trace_digest = usage["source_trace_sha256"]
print(
    f"trace_pipeline_tree_sha256={trace_pipeline_digest}"
    f" usage_source_trace_sha256={usage_trace_digest}"
    f" match={trace_pipeline_digest == usage_trace_digest}"
)
ok &= trace_pipeline_digest == usage_trace_digest
print(
    "launcher_additional_aggregate_digests:"
    f" candidate_tree_sha256={hashes['candidate_tree_sha256']}"
    f" generation_codex_trace_sha256={hashes['generation_codex_trace_sha256']}"
)

with Path("/task.json").open(encoding="utf-8") as stream:
    task = json.load(stream)
embedded_manifest = record["manifest"]
manifest_overlap_equal = all(embedded_manifest.get(key) == value for key, value in task.items())
embedded_extra = sorted(set(embedded_manifest) - set(task))
print(
    "task_manifest_matches_embedded_fields="
    f"{manifest_overlap_equal} embedded_extra_keys={embedded_extra}"
)
ok &= manifest_overlap_equal

print("candidate_entries:")
for path in sorted(Path("/candidate").rglob("*"), key=lambda item: item.as_posix()):
    kind = (
        "symlink"
        if path.is_symlink()
        else "file"
        if path.is_file()
        else "dir"
        if path.is_dir()
        else "other"
    )
    suffix = f" sha256={sha256_file(path)}" if kind == "file" else ""
    print(f"  {kind} {path.relative_to('/candidate')}{suffix}")
    if kind in {"symlink", "other"}:
        ok = False

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
trace_nonfiles = sorted(
    path for path in trace_root.rglob("*") if not path.is_file() and not path.is_dir()
)
print(f"trace_file_count={len(trace_files)} trace_nonfile_count={len(trace_nonfiles)}")
for path in trace_files:
    print(f"  trace {path.relative_to(trace_root)} sha256={sha256_file(path)}")
if not trace_files or trace_nonfiles:
    ok = False

trusted_semantics = Path("/reference/reference-semantics")
candidate_reference_semantics = Path("/candidate/reference-semantics")
print(
    "generated_semantics_boundary:"
    f" trusted_reference_semantics_exists={trusted_semantics.exists()}"
    f" candidate_reference_semantics_exists={candidate_reference_semantics.exists()}"
)
ok &= not trusted_semantics.exists()

required_candidate = [
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
]
for name in required_candidate:
    path = Path("/candidate") / name
    present = path.is_file() and not path.is_symlink()
    print(f"candidate_required {name}: {present}")
    ok &= present

print(f"OVERALL_OK={bool(ok)}")
raise SystemExit(0 if ok else 1)
