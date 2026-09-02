#!/usr/bin/env python3
"""Independent read-only provenance and mount-integrity checks."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import pathlib
import stat


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest(root: pathlib.Path) -> list[dict[str, str | int]]:
    records: list[dict[str, str | int]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            records.append({"path": rel, "type": "symlink", "target": os.readlink(path)})
        elif stat.S_ISDIR(mode):
            records.append({"path": rel, "type": "directory"})
        elif stat.S_ISREG(mode):
            records.append(
                {
                    "path": rel,
                    "type": "file",
                    "size": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
        else:
            records.append({"path": rel, "type": f"other:{stat.S_IFMT(mode):o}"})
    return records


def manifest_sha(records: list[dict[str, str | int]]) -> str:
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


with pathlib.Path("/audit-input.json").open() as stream:
    audit_input = json.load(stream)
with pathlib.Path("/audit-campaign-lock.json").open() as stream:
    campaign_lock = json.load(stream)

print("record_layout", audit_input["record_layout"])
print("semantics_mode", audit_input["semantics_mode"])
print("campaign_exact_match", campaign_lock == audit_input["audit_campaign"])

direct_hash_checks = {
    "audit_campaign_lock_sha256": pathlib.Path("/audit-campaign-lock.json"),
    "canonical_sha256": pathlib.Path("/reference/canonical.py"),
    "trusted_prompt_sha256": pathlib.Path("/reference/prompt.py"),
    "trusted_translator_sha256": pathlib.Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": pathlib.Path("/candidate/prompt.py"),
    "candidate_translator_sha256": pathlib.Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": pathlib.Path("/run.json"),
    "task_manifest_sha256": pathlib.Path("/task.json"),
    "stage1_result_sha256": pathlib.Path("/generation-result.json"),
    "stage1_invocation_sha256": pathlib.Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": pathlib.Path("/generation-evidence/metrics.json"),
    "generation_runtime_metrics_sha256": pathlib.Path(
        "/generation-evidence/runtime-metrics.json"
    ),
    "generation_usage_sha256": pathlib.Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": pathlib.Path(
        "/generation-evidence/codex-last.txt"
    ),
    "generation_codex_output_sha256": pathlib.Path(
        "/generation-evidence/codex-output.log"
    ),
    "generation_prompt_sha256": pathlib.Path("/generation-evidence/prompt.txt"),
}
for key, path in direct_hash_checks.items():
    actual = sha256(path)
    expected = audit_input["hashes"][key]
    print("HASH", key, actual, "MATCH" if actual == expected else f"MISMATCH:{expected}")

required_pipeline_v3 = [
    pathlib.Path("/run.json"),
    pathlib.Path("/task.json"),
    pathlib.Path("/generation-result.json"),
    pathlib.Path("/generation-evidence/invocation.json"),
    pathlib.Path("/generation-evidence/metrics.json"),
    pathlib.Path("/generation-evidence/runtime-metrics.json"),
    pathlib.Path("/generation-evidence/usage.json"),
    pathlib.Path("/generation-evidence/codex-last.txt"),
    pathlib.Path("/generation-evidence/codex-output.log"),
    pathlib.Path("/generation-evidence/prompt.txt"),
]
for path in required_pipeline_v3:
    kind = "regular" if path.is_file() and not path.is_symlink() else "INVALID"
    print("REQUIRED", kind, path, path.stat().st_size if path.exists() else "missing")

trace_root = pathlib.Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*"))
trace_regular = [path for path in trace_files if path.is_file() and not path.is_symlink()]
print("TRACE_FILES", len(trace_regular))
with pathlib.Path("/generation-result.json").open() as stream:
    generation_result = json.load(stream)
expected_trace_hashes = {
    key.removeprefix("codex-trace/"): value
    for key, value in generation_result["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
}
for path in trace_regular:
    rel = path.relative_to(trace_root).as_posix()
    actual = sha256(path)
    expected = expected_trace_hashes.get(rel)
    print("TRACE_HASH", rel, actual, "MATCH" if actual == expected else f"MISMATCH:{expected}")

trace_types: collections.Counter[str | None] = collections.Counter()
event_types: collections.Counter[str | None] = collections.Counter()
parse_errors: list[str] = []
line_count = 0
for path in trace_regular:
    with path.open() as stream:
        for number, line in enumerate(stream, 1):
            line_count += 1
            try:
                event = json.loads(line)
            except Exception as error:  # pragma: no cover - audit diagnostic
                parse_errors.append(f"{path}:{number}:{error}")
                continue
            trace_types[event.get("type")] += 1
            if event.get("type") == "event_msg":
                event_types[event.get("payload", {}).get("type")] += 1
print("TRACE_LINES", line_count)
print("TRACE_TYPES", dict(trace_types))
print("TRACE_EVENT_TYPES", dict(event_types))
print("TRACE_PARSE_ERRORS", parse_errors)

candidate_prompt = pathlib.Path("/candidate/prompt.py").read_bytes()
trusted_prompt = pathlib.Path("/reference/prompt.py").read_bytes()
candidate_translator = pathlib.Path("/candidate/py2mpy.py").read_bytes()
trusted_translator = pathlib.Path("/reference/py2mpy.py").read_bytes()
print("PROMPT_BYTE_IDENTICAL", candidate_prompt == trusted_prompt)
print("TRANSLATOR_BYTE_IDENTICAL", candidate_translator == trusted_translator)

candidate_semantics = tree_manifest(pathlib.Path("/candidate/reference-semantics"))
trusted_semantics = tree_manifest(pathlib.Path("/reference/reference-semantics"))
print("SEMANTICS_ENTRY_COUNT", len(candidate_semantics), len(trusted_semantics))
print("SEMANTICS_EXACT_MANIFEST_MATCH", candidate_semantics == trusted_semantics)
print("SEMANTICS_AUDITOR_MANIFEST_SHA", manifest_sha(candidate_semantics))

candidate_manifest = tree_manifest(pathlib.Path("/candidate"))
generation_manifest = tree_manifest(pathlib.Path("/generation-evidence"))
print("CANDIDATE_AUDITOR_MANIFEST_SHA", manifest_sha(candidate_manifest))
print("GENERATION_AUDITOR_MANIFEST_SHA", manifest_sha(generation_manifest))
for label, records in [
    ("candidate", candidate_manifest),
    ("trusted-semantics", trusted_semantics),
    ("generation-evidence", generation_manifest),
]:
    links = [record for record in records if record["type"] == "symlink"]
    other = [record for record in records if str(record["type"]).startswith("other:")]
    print("SPECIAL_ENTRIES", label, "symlinks", links, "other", other)

required_candidate = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for rel in required_candidate:
    path = pathlib.Path("/candidate") / rel
    kind = "regular" if path.is_file() and not path.is_symlink() else "INVALID"
    print("CANDIDATE_ARTIFACT", kind, rel)
