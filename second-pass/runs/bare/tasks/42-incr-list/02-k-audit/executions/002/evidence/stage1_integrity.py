#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks."""

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


failures = []


def check(condition, message):
    marker = "PASS" if condition else "FAIL"
    print(f"{marker}: {message}")
    if not condition:
        failures.append(message)


def load_json(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def check_regular(path, description):
    item = Path(path)
    check(item.exists(), f"{description} exists: {path}")
    if not item.exists():
        return
    check(not item.is_symlink(), f"{description} is not a symlink: {path}")
    check(item.is_file(), f"{description} is a regular file: {path}")
    check(os.access(item, os.R_OK), f"{description} is readable: {path}")


def tree_manifest(root):
    root_path = Path(root)
    digest = hashlib.sha256()
    rows = []
    for item in sorted(root_path.rglob("*"), key=lambda p: p.relative_to(root_path).as_posix()):
        rel = item.relative_to(root_path).as_posix()
        info = item.lstat()
        mode = stat.S_IMODE(info.st_mode)
        if item.is_symlink():
            kind = "symlink"
            value = os.readlink(item)
        elif item.is_dir():
            kind = "dir"
            value = "-"
        elif item.is_file():
            kind = "file"
            value = sha256_file(item)
        else:
            kind = "other"
            value = "-"
        row = f"{kind}\\0{mode:o}\\0{rel}\\0{value}\\n"
        digest.update(row.encode())
        rows.append((kind, mode, rel, value))
    return digest.hexdigest(), rows


def launcher_tree_digest(root):
    """Reimplement the launcher's documented path/kind/size/content scheme."""
    root_path = Path(root)
    digest = hashlib.sha256()
    entries = []
    for item in root_path.rglob("*"):
        relative = item.relative_to(root_path).as_posix()
        if item.is_symlink():
            raise ValueError(f"linked tree entry: {item}")
        if item.is_dir():
            entries.append((relative, "directory", item))
        elif item.is_file():
            entries.append((relative, "file", item))
        else:
            raise ValueError(f"unsupported tree entry: {item}")
    for relative, kind, item in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(item.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with open(item, "rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


audit_path = Path("/audit-input.json")
check(audit_path.exists(), "launcher audit input exists")
check(not audit_path.is_symlink(), "launcher audit input is not a symlink")
audit = load_json(audit_path)

check(audit.get("record_layout") == "legacy-selected-stage1", "declared record layout is legacy-selected-stage1")
check(audit.get("semantics_mode") == "GENERATED_SEMANTICS", "declared semantics mode is GENERATED_SEMANTICS")
check(not Path("/reference/reference-semantics").exists(), "trusted reference-semantics is absent in generated-semantics mode")

required_regular = [
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
]
for required in required_regular:
    check_regular(required, "required mounted record")

check(Path("/generation-evidence/codex-trace").is_dir(), "structured trace directory exists")
check(not Path("/generation-evidence/codex-trace").is_symlink(), "structured trace directory is not a symlink")
check(Path("/candidate").is_dir(), "candidate mount exists")
check(not Path("/candidate").is_symlink(), "candidate mount is not a symlink")

usage = Path("/generation-evidence/usage.json")
if usage.exists():
    check_regular(usage, "optional usage record")

recorded = audit["hashes"]
file_checks = {
    "/audit-campaign-lock.json": recorded["audit_campaign_lock_sha256"],
    "/run.json": recorded["run_manifest_sha256"],
    "/task.json": recorded["task_manifest_sha256"],
    "/generation-result.json": recorded["stage1_result_sha256"],
    "/generation-evidence/invocation.json": recorded["stage1_invocation_sha256"],
    "/generation-evidence/metrics.json": recorded["generation_metrics_sha256"],
    "/generation-evidence/codex-last.txt": recorded["generation_codex_last_sha256"],
    "/generation-evidence/codex-output.log": recorded["generation_codex_output_sha256"],
    "/generation-evidence/prompt.txt": recorded["generation_prompt_sha256"],
    "/reference/canonical.py": recorded["canonical_sha256"],
    "/reference/prompt.py": recorded["trusted_prompt_sha256"],
    "/reference/py2mpy.py": recorded["trusted_translator_sha256"],
    "/candidate/prompt.py": recorded["candidate_prompt_sha256"],
    "/candidate/py2mpy.py": recorded["candidate_translator_sha256"],
}
if usage.exists():
    file_checks[str(usage)] = recorded["generation_usage_sha256"]

for path, expected in file_checks.items():
    actual = sha256_file(path)
    check(actual == expected, f"SHA-256 {path}: actual={actual} expected={expected}")

campaign_lock = load_json("/audit-campaign-lock.json")
check(campaign_lock == audit["audit_campaign"], "campaign lock object exactly matches audit-input campaign block")
task = load_json("/task.json")
audit_manifest_without_config = dict(audit["manifest"])
injected_config = audit_manifest_without_config.pop("config", None)
check(
    task == audit_manifest_without_config,
    "task manifest matches audit-input manifest after removing launcher-injected config",
)
check(
    injected_config == audit.get("manifest_config") == audit.get("config"),
    "launcher-injected manifest config is internally consistent",
)

with open("/candidate/prompt.py", "rb") as left, open("/reference/prompt.py", "rb") as right:
    check(left.read() == right.read(), "candidate prompt is byte-identical to trusted prompt")
with open("/candidate/py2mpy.py", "rb") as left, open("/reference/py2mpy.py", "rb") as right:
    check(left.read() == right.read(), "candidate translator is byte-identical to trusted translator")

generation_result = load_json("/generation-result.json")
for relative, expected in generation_result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    check(path.exists(), f"generation-result evidence entry exists: {relative}")
    if path.exists():
        actual = sha256_file(path)
        check(actual == expected, f"generation-result SHA-256 {relative}: actual={actual} expected={expected}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
check(any(item.is_file() for item in trace_files), "structured trace contains a file")
for item in trace_files:
    check(not item.is_symlink(), f"generation trace entry is not a symlink: {item}")

candidate_digest, candidate_rows = tree_manifest("/candidate")
trace_digest, trace_rows = tree_manifest("/generation-evidence/codex-trace")
candidate_launcher_digest = launcher_tree_digest("/candidate")
trace_launcher_digest = launcher_tree_digest("/generation-evidence/codex-trace")
print(f"INDEPENDENT_CANDIDATE_TREE_SHA256: {candidate_digest}")
print(f"LAUNCHER_RECORDED_CANDIDATE_TREE_SHA256: {recorded['candidate_tree_sha256']}")
print(f"INDEPENDENT_TRACE_TREE_SHA256: {trace_digest}")
print(f"LAUNCHER_RECORDED_TRACE_TREE_SHA256: {recorded['generation_codex_trace_sha256']}")
check(
    candidate_launcher_digest == generation_result["outputs"]["workspace_sha256"],
    "independent pipeline-scheme candidate tree digest matches generation result: "
    f"actual={candidate_launcher_digest} "
    f"expected={generation_result['outputs']['workspace_sha256']}",
)
usage_document = load_json(usage) if usage.exists() else {}
check(
    trace_launcher_digest == usage_document.get("source_trace_sha256"),
    "independent pipeline-scheme trace tree digest matches usage record: "
    f"actual={trace_launcher_digest} "
    f"expected={usage_document.get('source_trace_sha256')}",
)
print(
    "NOTE: audit-input aggregate tree hashes use a distinct launcher encoding; "
    "the per-entry manifests above and pipeline-scheme digests independently "
    "bind all mounted bytes."
)
print("CANDIDATE_TREE_MANIFEST:")
for kind, mode, rel, value in candidate_rows:
    print(f"  {kind} {mode:o} {value} {rel}")
    check(kind != "symlink", f"candidate entry is not symlink: {rel}")
    check(kind in {"dir", "file"}, f"candidate entry has ordinary type: {rel}")
print("TRACE_TREE_MANIFEST:")
for kind, mode, rel, value in trace_rows:
    print(f"  {kind} {mode:o} {value} {rel}")

print(f"FAILURE_COUNT: {len(failures)}")
sys.exit(1 if failures else 0)
