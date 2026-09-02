#!/usr/bin/env python3
"""Independent lstat/hash checks for launcher records and mounted inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
data = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
recorded = data["hashes"]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


failures: list[str] = []


def require(path: Path, expected: str) -> None:
    if not path.exists() and not path.is_symlink():
        failures.append(f"MISSING {expected} {path}")
        print(f"FAIL missing expected={expected} path={path}")
        return
    actual = kind(path)
    print(f"ENTRY path={path} expected={expected} actual={actual} readable={os.access(path, os.R_OK)}")
    if actual != expected:
        failures.append(f"MISTYPED {path}: expected {expected}, got {actual}")
    if not os.access(path, os.R_OK):
        failures.append(f"UNREADABLE {path}")


print(f"record_layout={data['record_layout']}")
print(f"semantics_mode={data['semantics_mode']}")
print(f"audit_input_sha256={digest(AUDIT_INPUT)}")

required_files = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
required_dirs = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference/reference-semantics"),
]
for path in required_files:
    require(path, "file")
for path in required_dirs:
    require(path, "dir")

usage = Path("/generation-evidence/usage.json")
if usage.exists() or usage.is_symlink():
    require(usage, "file")
    print(f"optional_usage_present=true sha256={digest(usage)}")
else:
    print("optional_usage_present=false")

runtime_metrics = Path("/generation-evidence/runtime-metrics.json")
print(f"runtime_metrics_present={runtime_metrics.exists() or runtime_metrics.is_symlink()}")
print("runtime_metrics_required_for_layout=false")

direct_hashes = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
}
for path, field in direct_hashes.items():
    if not path.is_file() or path.is_symlink():
        continue
    actual = digest(path)
    expected = recorded[field]
    result = actual == expected
    print(f"HASH path={path} field={field} actual={actual} expected={expected} match={result}")
    if not result:
        failures.append(f"HASH MISMATCH {path}")

campaign = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
same_campaign = campaign == data["audit_campaign"]
print(f"campaign_block_equal={same_campaign}")
if not same_campaign:
    failures.append("CAMPAIGN BLOCK MISMATCH")

invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
for relative, expected in invocation["outputs"]["evidence"].items():
    mounted = Path("/generation-evidence") / relative
    require(mounted, "file")
    if mounted.is_file() and not mounted.is_symlink():
        actual = digest(mounted)
        result = actual == expected
        print(
            f"INVOCATION_HASH path={mounted} actual={actual} "
            f"expected={expected} match={result}"
        )
        if not result:
            failures.append(f"INVOCATION HASH MISMATCH {mounted}")


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    answer: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        entry_kind = kind(path)
        answer[relative] = (entry_kind, digest(path) if entry_kind == "file" else None)
    return answer


def manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    payload = "".join(
        f"{entry_kind}\t{relative}\t{entry_digest or ''}\n"
        for relative, (entry_kind, entry_digest) in entries.items()
    )
    return hashlib.sha256(payload.encode()).hexdigest()


trusted_tree = tree_entries(Path("/reference/reference-semantics"))
candidate_tree = tree_entries(Path("/candidate/reference-semantics"))
print(f"trusted_semantics_entries={len(trusted_tree)} manifest_sha256={manifest_digest(trusted_tree)}")
print(f"candidate_semantics_entries={len(candidate_tree)} manifest_sha256={manifest_digest(candidate_tree)}")
all_semantics_paths = sorted(set(trusted_tree) | set(candidate_tree))
semantics_diffs = []
for relative in all_semantics_paths:
    trusted_entry = trusted_tree.get(relative)
    candidate_entry = candidate_tree.get(relative)
    if trusted_entry != candidate_entry:
        semantics_diffs.append((relative, trusted_entry, candidate_entry))
        print(
            f"SEMANTICS_DIFF path={relative} trusted={trusted_entry} "
            f"candidate={candidate_entry}"
        )
print(f"semantics_recursive_exact={not semantics_diffs}")
if semantics_diffs:
    failures.append(f"SEMANTICS TREE HAS {len(semantics_diffs)} DIFFERENCES")

for root in (Path("/candidate"), Path("/generation-evidence")):
    bad = [(relative, entry) for relative, entry in tree_entries(root).items() if entry[0] == "symlink"]
    print(f"symlinks_below_{root.name}={bad}")

candidate_all = tree_entries(Path("/candidate"))
trace_all = tree_entries(Path("/generation-evidence/codex-trace"))
print(f"candidate_independent_manifest_sha256={manifest_digest(candidate_all)} entries={len(candidate_all)}")
print(f"trace_independent_manifest_sha256={manifest_digest(trace_all)} entries={len(trace_all)}")

for left, right, label in (
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
):
    identical = left.read_bytes() == right.read_bytes()
    print(f"{label}_byte_identical={identical}")
    if not identical:
        failures.append(f"{label.upper()} NOT BYTE IDENTICAL")

print(f"integrity_failure_count={len(failures)}")
for failure in failures:
    print(f"FAILURE {failure}")
raise SystemExit(1 if failures else 0)
