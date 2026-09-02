#!/usr/bin/env python3
"""Independent launcher/provenance integrity check for this audit mount."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({mode:o})"


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
failures: list[str] = []


def require(condition: bool, message: str) -> None:
    print(("OK " if condition else "FAIL ") + message)
    if not condition:
        failures.append(message)


require(kind(AUDIT) == "regular", "/audit-input.json is a regular non-symlink")
require(kind(LOCK) == "regular", "/audit-campaign-lock.json is a regular non-symlink")
require(audit["record_layout"] == "legacy-selected-stage1", "declared record layout")
require(audit["semantics_mode"] == "GENERATED_SEMANTICS", "declared semantics mode")
require(lock == audit["audit_campaign"], "campaign lock content equals audit campaign block")
require(
    sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"],
    "campaign lock SHA-256 matches",
)
require(
    not Path("/reference/reference-semantics").exists()
    and not Path("/reference/reference-semantics").is_symlink(),
    "generated-semantics boundary: no reference semantics is mounted",
)

container_paths = audit["container_paths"]
required_declared = [
    "audit_campaign_lock",
    "candidate",
    "canonical",
    "generation_last",
    "generation_manifest",
    "generation_metrics",
    "generation_output",
    "generation_root",
    "generation_trace",
    "run_manifest",
    "stage1_result",
    "task_manifest",
    "translator",
    "trusted_prompt",
]
for key in required_declared:
    path = Path(container_paths[key])
    require(path.exists() and kind(path) != "symlink", f"declared mount {key}: {path}")

required_layout_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_layout_records:
    require(path.exists() and kind(path) == "regular", f"required layout record: {path}")

usage = Path("/generation-evidence/usage.json")
require(usage.exists() and kind(usage) == "regular", "optional historical usage exists and is regular")

hash_checks = {
    LOCK: audit["hashes"]["audit_campaign_lock_sha256"],
    Path("/reference/canonical.py"): audit["hashes"]["canonical_sha256"],
    Path("/reference/prompt.py"): audit["hashes"]["trusted_prompt_sha256"],
    Path("/reference/py2mpy.py"): audit["hashes"]["trusted_translator_sha256"],
    Path("/candidate/prompt.py"): audit["hashes"]["candidate_prompt_sha256"],
    Path("/candidate/py2mpy.py"): audit["hashes"]["candidate_translator_sha256"],
    Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
    Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
    Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
    Path("/generation-evidence/invocation.json"): audit["hashes"]["stage1_invocation_sha256"],
    Path("/generation-evidence/metrics.json"): audit["hashes"]["generation_metrics_sha256"],
    usage: audit["hashes"]["generation_usage_sha256"],
    Path("/generation-evidence/codex-last.txt"): audit["hashes"]["generation_codex_last_sha256"],
    Path("/generation-evidence/codex-output.log"): audit["hashes"]["generation_codex_output_sha256"],
    Path("/generation-evidence/prompt.txt"): audit["hashes"]["generation_prompt_sha256"],
}
for path, expected in hash_checks.items():
    actual = sha256(path)
    require(actual == expected, f"SHA-256 {path}: {actual}")

require(
    Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes(),
    "candidate prompt is byte-identical to trusted prompt",
)
require(
    Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes(),
    "candidate translator is byte-identical to trusted translator",
)

run = json.loads(Path("/run.json").read_text())
task = json.loads(Path("/task.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
metrics = json.loads(Path("/generation-evidence/metrics.json").read_text())
manifest = audit["manifest"]
require(
    all(task.get(key) == manifest.get(key) for key in task),
    "all task-manifest fields equal the corresponding launcher manifest fields",
)
require(
    manifest.get("config") == audit["config"],
    "launcher manifest's additional config field matches audit config",
)
require(run["config"] == audit["config"], "run config matches audit config")
require(task["problem_id"] == audit["problem_id"], "task problem id matches")
require(result["invocation"] == invocation["name"], "selected result/invocation names match")
require(result["session_id"] == invocation["session_id"], "selected result/invocation sessions match")
require(metrics["exit_code"] == invocation["exit_code"] == 0, "historical invocation exit records agree")
require(
    Path("/generation-evidence/prompt.txt").read_bytes()
    and sha256(Path("/generation-evidence/prompt.txt"))
    == task["inputs"]["instruction_prompt_sha256"],
    "generation instruction prompt matches task manifest",
)
require(
    sha256(Path("/reference/prompt.py")) == task["inputs"]["problem_prompt_sha256"],
    "trusted problem prompt matches task manifest",
)
require(
    sha256(Path("/reference/py2mpy.py")) == task["inputs"]["translator_sha256"],
    "trusted translator matches task manifest",
)

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
trace_other = [
    path
    for path in trace_root.rglob("*")
    if kind(path) not in {"regular", "directory"}
]
require(not trace_other, "structured trace contains only regular files/directories")
expected_trace = result["outputs"]["evidence"]
for path in trace_files:
    relative = path.relative_to(Path("/generation-evidence")).as_posix()
    require(
        relative in expected_trace and sha256(path) == expected_trace[relative],
        f"structured trace file hash: {relative}",
    )

event_counts: Counter[str | None] = Counter()
payload_counts: Counter[str | None] = Counter()
trace_lines = 0
for path in trace_files:
    with path.open() as stream:
        for number, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                event = json.loads(line)
            except json.JSONDecodeError as error:
                failures.append(f"malformed trace line {path}:{number}: {error}")
                continue
            event_counts[event.get("type")] += 1
            payload = event.get("payload")
            payload_counts[payload.get("type") if isinstance(payload, dict) else None] += 1
print(f"TRACE lines={trace_lines} event_types={dict(event_counts)}")
print(f"TRACE payload_types={dict(payload_counts)}")
require(trace_lines == 273, "all 273 structured trace records parsed")
require(payload_counts["task_complete"] == 1, "trace has one terminal task record")

candidate_root = Path("/candidate")
candidate_manifest = []
unsupported = []
for path in sorted(candidate_root.rglob("*")):
    relative = path.relative_to(candidate_root).as_posix()
    path_kind = kind(path)
    if path_kind == "regular":
        candidate_manifest.append((relative, sha256(path)))
    elif path_kind != "directory":
        unsupported.append((relative, path_kind))
require(not unsupported, "candidate tree has no symlink or unsupported entry")
for relative, digest in candidate_manifest:
    print(f"CANDIDATE {digest}  {relative}")
manifest_bytes = json.dumps(candidate_manifest, separators=(",", ":")).encode()
print("candidate_reviewer_manifest_sha256=" + hashlib.sha256(manifest_bytes).hexdigest())
print("launcher_recorded_candidate_tree_sha256=" + audit["hashes"]["candidate_tree_sha256"])

print(f"failure_count={len(failures)}")
raise SystemExit(1 if failures else 0)
