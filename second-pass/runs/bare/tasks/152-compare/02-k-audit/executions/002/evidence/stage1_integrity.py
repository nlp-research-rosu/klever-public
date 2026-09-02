#!/usr/bin/env python3
"""Independent integrity and provenance checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE_ROOT = Path("/generation-evidence/codex-trace")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as inp:
        for block in iter(lambda: inp.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
task_manifest = json.loads(Path("/task.json").read_text())
embedded_manifest_without_normalized_config = dict(audit["manifest"])
embedded_config = embedded_manifest_without_normalized_config.pop("config", None)
task_manifest_normalized_match = (
    embedded_manifest_without_normalized_config == task_manifest
    and embedded_config == audit["manifest_config"] == audit["config"]
)

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"audit_campaign_exact_match={audit['audit_campaign'] == lock}")
print(
    "audit_campaign_lock_hash="
    f"{digest(LOCK)} recorded={audit['hashes']['audit_campaign_lock_sha256']}"
)
print(
    "task_manifest_normalized_match="
    f"{task_manifest_normalized_match} "
    "(audit-input embeds its separately recorded config into the manifest view)"
)
print(f"reference_semantics_present={Path('/reference/reference-semantics').exists()}")

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
    TRACE_ROOT,
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/candidate"),
]

print("required_mount_types:")
for path in required:
    kind_ok = (
        path.is_dir() and not path.is_symlink()
        if path in (TRACE_ROOT, Path("/candidate"))
        else regular_nonsymlink(path)
    )
    print(f"  {path}: exists={path.exists()} nonsymlink_expected_type={kind_ok}")

declared_hashes = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
}

print("declared_file_hash_checks:")
all_hashes_match = True
for path, key in declared_hashes.items():
    actual = digest(path) if regular_nonsymlink(path) else "MISSING_OR_BAD_TYPE"
    expected = audit["hashes"][key]
    match = actual == expected
    all_hashes_match &= match
    print(f"  {path}: actual={actual} recorded={expected} match={match}")
print(f"all_declared_file_hashes_match={all_hashes_match}")

candidate_prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
candidate_translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print(f"candidate_prompt_byte_equal_trusted={candidate_prompt_equal}")
print(f"candidate_translator_byte_equal_trusted={candidate_translator_equal}")

print("candidate_tree_inventory:")
for path in sorted(Path("/candidate").rglob("*")):
    rel = path.relative_to("/candidate")
    if path.is_symlink():
        print(f"  SYMLINK {rel} -> {os.readlink(path)}")
    elif path.is_dir():
        print(f"  DIR {rel}")
    elif path.is_file():
        print(f"  FILE {rel} size={path.stat().st_size} sha256={digest(path)}")
    else:
        print(f"  OTHER {rel}")

print("generation_tree_inventory:")
for path in sorted(Path("/generation-evidence").rglob("*")):
    rel = path.relative_to("/generation-evidence")
    if path.is_symlink():
        print(f"  SYMLINK {rel} -> {os.readlink(path)}")
    elif path.is_dir():
        print(f"  DIR {rel}")
    elif path.is_file():
        print(f"  FILE {rel} size={path.stat().st_size} sha256={digest(path)}")
    else:
        print(f"  OTHER {rel}")

stage1_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
print(
    "stage1_result_and_invocation_evidence_maps_equal="
    f"{stage1_result['outputs']['evidence'] == invocation['outputs']['evidence']}"
)
print("stage1_declared_evidence_hash_checks:")
for rel, expected in sorted(invocation["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    actual = digest(path) if regular_nonsymlink(path) else "MISSING_OR_BAD_TYPE"
    print(f"  {rel}: actual={actual} recorded={expected} match={actual == expected}")

trace_paths = sorted(TRACE_ROOT.rglob("*"))
trace_files = [p for p in trace_paths if p.is_file() and not p.is_symlink()]
print(f"trace_regular_file_count={len(trace_files)}")

event_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_calls: list[tuple[int, str, str]] = []
event_count = 0
parse_errors: list[str] = []
for trace_path in trace_files:
    with trace_path.open() as inp:
        for lineno, raw in enumerate(inp, 1):
            try:
                event = json.loads(raw)
            except Exception as err:
                parse_errors.append(f"{trace_path}:{lineno}: {err}")
                continue
            event_count += 1
            typ = str(event.get("type", "<missing>"))
            event_types[typ] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[f"{typ}/{payload.get('type', '<missing>')}"] += 1
                if payload.get("type") in ("function_call", "custom_tool_call"):
                    name = str(payload.get("name", "<missing>"))
                    args = payload.get("arguments", payload.get("input", ""))
                    tool_calls.append((lineno, name, str(args)))

print(f"trace_event_count={event_count}")
print(f"trace_parse_errors={len(parse_errors)}")
for err in parse_errors:
    print(f"  {err}")
print("trace_event_types:")
for typ, count in sorted(event_types.items()):
    print(f"  {typ}: {count}")
print("trace_payload_types:")
for typ, count in sorted(payload_types.items()):
    print(f"  {typ}: {count}")
print("trace_tool_calls:")
for lineno, name, args in tool_calls:
    one_line = " ".join(args.split())
    print(f"  line={lineno} name={name} args={one_line[:1200]}")

# Read the complete output log as bytes and summarize its structure without
# trusting it as an instruction or emitting hundreds of kilobytes verbatim.
log_path = Path("/generation-evidence/codex-output.log")
log = log_path.read_bytes()
print(
    "codex_output_full_read="
    f"bytes={len(log)} lines={log.count(bytes([10]))} nul_bytes={log.count(bytes([0]))}"
)
for needle in (
    b"KPROVE_PASSED",
    b"#Top",
    b"WarnStuckClaimState",
    b"semantic.k",
    b"verification.k",
    b"spec.k",
):
    print(f"codex_output_occurrences[{needle.decode()}]={log.count(needle)}")

if not (
    audit["audit_campaign"] == lock
    and task_manifest_normalized_match
    and all_hashes_match
    and candidate_prompt_equal
    and candidate_translator_equal
    and not Path("/reference/reference-semantics").exists()
    and not parse_errors
):
    raise SystemExit(1)
