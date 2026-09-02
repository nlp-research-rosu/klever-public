#!/usr/bin/env python3
"""Independent integrity and generation-record inspection for this audit."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def tree_entries(root: Path):
    result = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs.sort()
        files.sort()
        base_path = Path(base)
        for name in dirs + files:
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                result[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                result[rel] = ("dir", None)
            elif path.is_file():
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = ("other", None)
    return result


audit = load_json(AUDIT_INPUT)
lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
lock = load_json(lock_path)
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_equal={audit['audit_campaign'] == lock}")
lock_hash = sha256(lock_path)
print(f"audit_campaign_lock_sha256={lock_hash}")
print(
    "audit_campaign_lock_hash_matches="
    f"{lock_hash == audit['hashes']['audit_campaign_lock_sha256']}"
)

required = [
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
print("required_records:")
for path in required:
    status = "directory" if path.is_dir() else "file" if path.is_file() else "MISSING"
    print(f"  {status} {path}")

hash_checks = {
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
}
print("recorded_hash_checks:")
for raw_path, key in hash_checks.items():
    path = Path(raw_path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"  {'OK' if actual == expected else 'MISMATCH'} {raw_path} {actual}")

candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
print(f"candidate_semantics_entries={len(candidate_semantics)}")
print(f"trusted_semantics_entries={len(trusted_semantics)}")
print(f"semantics_trees_exact={candidate_semantics == trusted_semantics}")
for rel in sorted(set(candidate_semantics) | set(trusted_semantics)):
    if candidate_semantics.get(rel) != trusted_semantics.get(rel):
        print(
            f"  SEMANTICS_DIFF {rel}: "
            f"candidate={candidate_semantics.get(rel)} trusted={trusted_semantics.get(rel)}"
        )

candidate_all = tree_entries(Path("/candidate"))
candidate_symlinks = [name for name, value in candidate_all.items() if value[0] == "symlink"]
print(f"candidate_symlinks={candidate_symlinks}")
proof_artifacts = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for artifact in proof_artifacts:
    print(f"proof_artifact_{artifact}={candidate_all.get(artifact)}")

result = load_json(Path("/generation-result.json"))
trace_expected = result["outputs"]["evidence"]
trace_root = Path("/generation-evidence/codex-trace")
print("generation_result_evidence_hashes:")
for rel, expected in sorted(trace_expected.items()):
    path = Path("/generation-evidence") / rel
    actual = sha256(path)
    print(f"  {'OK' if actual == expected else 'MISMATCH'} {rel} {actual}")

trace_files = sorted(trace_root.rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
print(f"trace_file_count={len(trace_files)}")
top_types = collections.Counter()
payload_types = collections.Counter()
response_roles = collections.Counter()
trace_lines = 0
invalid_trace_lines = []
tool_commands = []
for path in trace_files:
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                event = json.loads(line)
            except json.JSONDecodeError as error:
                invalid_trace_lines.append((str(path), line_number, str(error)))
                continue
            top_types[event.get("type")] += 1
            payload = event.get("payload") or {}
            payload_types[payload.get("type")] += 1
            if event.get("type") == "response_item":
                response_roles[payload.get("role")] += 1
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    tool_commands.append(
                        (
                            payload.get("name"),
                            payload.get("arguments") or payload.get("input"),
                        )
                    )
print(f"trace_lines={trace_lines}")
print(f"invalid_trace_lines={invalid_trace_lines}")
print(f"trace_top_types={dict(sorted(top_types.items(), key=lambda x: str(x[0])))}")
print(f"trace_payload_types={dict(sorted(payload_types.items(), key=lambda x: str(x[0])))}")
print(f"trace_response_roles={dict(sorted(response_roles.items(), key=lambda x: str(x[0])))}")
print(f"trace_tool_call_count={len(tool_commands)}")
for index, (name, arguments) in enumerate(tool_commands, 1):
    rendered = str(arguments).replace("\n", "\\n")
    if len(rendered) > 500:
        rendered = rendered[:500] + "...<bounded>"
    print(f"  trace_tool_call[{index}] name={name} args={rendered}")

output_log = Path("/generation-evidence/codex-output.log")
with output_log.open("r", encoding="utf-8", errors="replace") as stream:
    output_lines = list(stream)
print(f"codex_output_lines={len(output_lines)}")
print(f"codex_output_bytes={output_log.stat().st_size}")
markers = [
    "#Top",
    "WarnStuckClaimState",
    "VALIDATED",
    "KPROVE_PASSED",
    "apply_patch",
    "kompile",
    "kprove",
    "krun",
]
for marker in markers:
    count = sum(line.count(marker) for line in output_lines)
    print(f"codex_output_marker[{marker}]={count}")
