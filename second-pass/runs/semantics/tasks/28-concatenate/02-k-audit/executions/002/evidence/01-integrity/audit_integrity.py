#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def print_check(name: str, ok: bool, detail: str = "") -> None:
    suffix = f" ({detail})" if detail else ""
    print(f"{name}: {'PASS' if ok else 'FAIL'}{suffix}")


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

print(f"record_layout: {audit['record_layout']}")
print(f"semantics_mode: {audit['semantics_mode']}")
print_check(
    "campaign_object_matches_lock",
    audit["audit_campaign"] == lock,
)
actual_lock_hash = digest(LOCK)
print_check(
    "campaign_lock_hash",
    actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"],
    actual_lock_hash,
)

required_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
    GENERATION / "codex-trace",
]
for path in required_records:
    ok = path.is_dir() and not path.is_symlink() if path.name == "codex-trace" else regular_nonsymlink(path)
    print_check(f"required_record:{path}", ok)

optional_usage = GENERATION / "usage.json"
print_check("optional_usage_present_and_regular", regular_nonsymlink(optional_usage))
print_check(
    "legacy_runtime_metrics_not_required_and_absent",
    not (GENERATION / "runtime-metrics.json").exists(),
)

direct_hashes = {
    LOCK: "audit_campaign_lock_sha256",
    REFERENCE / "canonical.py": "canonical_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "usage.json": "generation_usage_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
}
for path, key in direct_hashes.items():
    actual = digest(path)
    expected = audit["hashes"][key]
    print_check(f"sha256:{path}", actual == expected, actual)

for json_path in [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "usage.json",
]:
    json.loads(json_path.read_text())
    print_check(f"valid_json:{json_path}", True)

candidate_proof_files = [
    CANDIDATE / "solution.py",
    CANDIDATE / "solution.mpy",
    CANDIDATE / "verification.k",
    CANDIDATE / "spec.k",
    CANDIDATE / "prove.sh",
]
for path in candidate_proof_files:
    print_check(f"candidate_proof_artifact:{path}", regular_nonsymlink(path))

for candidate_path, trusted_path, label in [
    (CANDIDATE / "prompt.py", REFERENCE / "prompt.py", "candidate_prompt_exact"),
    (CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py", "candidate_translator_exact"),
]:
    print_check(label, candidate_path.read_bytes() == trusted_path.read_bytes())

trusted_semantics = REFERENCE / "reference-semantics"
candidate_semantics = CANDIDATE / "reference-semantics"
print_check("supplied_semantics_trusted_mount_present", trusted_semantics.is_dir() and not trusted_semantics.is_symlink())
print_check("supplied_semantics_candidate_tree_present", candidate_semantics.is_dir() and not candidate_semantics.is_symlink())


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries[rel] = ("symlink", str(path.readlink()))
        elif path.is_dir():
            entries[rel] = ("directory", None)
        elif path.is_file():
            entries[rel] = ("file", digest(path))
        else:
            entries[rel] = ("other", None)
    return entries


trusted_entries = tree_entries(trusted_semantics)
candidate_entries = tree_entries(candidate_semantics)
print_check("reference_semantics_recursive_identity", trusted_entries == candidate_entries)
print_check(
    "reference_semantics_no_symlinks",
    all(kind != "symlink" for kind, _ in trusted_entries.values())
    and all(kind != "symlink" for kind, _ in candidate_entries.values()),
)
print("reference_semantics_file_manifest:")
for rel, (kind, value) in trusted_entries.items():
    if kind == "file":
        print(f"  {value}  {rel}")

result = json.loads(Path("/generation-result.json").read_text())
output_hashes = result["outputs"]["evidence"]
print("generation_result_evidence_hashes:")
for rel, expected in sorted(output_hashes.items()):
    path = GENERATION / rel
    actual = digest(path)
    print_check(f"generation_output:{rel}", actual == expected, actual)

trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file() and not path.is_symlink()]
trace_counts: Counter[str] = Counter()
function_counts: Counter[str] = Counter()
trace_lines = 0
trace_final_messages = 0
for path in trace_files:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            trace_counts[record.get("type", "<missing>")] += 1
            payload = record.get("payload", {})
            if record.get("type") == "response_item" and payload.get("type") == "function_call":
                function_counts[payload.get("name", "<missing>")] += 1
            if record.get("type") == "event_msg" and payload.get("type") == "agent_message":
                if payload.get("phase") == "final_answer":
                    trace_final_messages += 1
    print(f"trace_file: {path} sha256={digest(path)}")
print(f"trace_json_lines: {trace_lines}")
print(f"trace_event_types: {dict(sorted(trace_counts.items()))}")
print(f"trace_function_calls: {dict(sorted(function_counts.items()))}")
print(f"trace_final_answer_events: {trace_final_messages}")

output_text = (GENERATION / "codex-output.log").read_text(errors="replace")
last_text = (GENERATION / "codex-last.txt").read_text(errors="replace")
prompt_text = (GENERATION / "prompt.txt").read_text(errors="replace")
print(f"codex_output_lines: {len(output_text.splitlines())}")
print(f"codex_output_kprove_passed_occurrences: {output_text.count('KPROVE_PASSED')}")
print(f"codex_output_top_occurrences: {output_text.count('#Top')}")
print(f"codex_output_failed_occurrences: {output_text.lower().count('failed')}")
print(f"codex_last_lines: {len(last_text.splitlines())}")
print(f"prompt_lines: {len(prompt_text.splitlines())}")
print_check("prompt_hash_matches_task_manifest", digest(GENERATION / "prompt.txt") == json.loads(Path("/task.json").read_text())["inputs"]["instruction_prompt_sha256"])

print("INTEGRITY_SCRIPT_COMPLETE")
