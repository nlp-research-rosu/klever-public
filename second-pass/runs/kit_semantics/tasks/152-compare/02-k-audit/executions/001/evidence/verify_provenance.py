#!/usr/bin/env python3
import collections
import hashlib
import json
import os
from pathlib import Path

AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def inventory(root: Path):
    result = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()
        base = Path(directory)
        for name in dirnames + filenames:
            path = base / name
            rel = str(path.relative_to(root))
            if path.is_symlink():
                result[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                result[rel] = ("directory", None)
            elif path.is_file():
                result[rel] = ("file", sha256_file(path))
            else:
                result[rel] = ("other", None)
    return result


audit = load_json(AUDIT_INPUT)
lock = load_json(Path("/audit-campaign-lock.json"))
print("record_layout:", audit.get("record_layout"))
print("semantics_mode:", audit.get("semantics_mode"))
print("campaign_block_equal:", audit.get("audit_campaign") == lock)
actual_lock_hash = sha256_file(Path("/audit-campaign-lock.json"))
expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print("campaign_lock_hash:", actual_lock_hash, expected_lock_hash, actual_lock_hash == expected_lock_hash)

direct_hashes = [
    ("audit_campaign_lock_sha256", "/audit-campaign-lock.json"),
    ("canonical_sha256", "/reference/canonical.py"),
    ("candidate_prompt_sha256", "/candidate/prompt.py"),
    ("trusted_prompt_sha256", "/reference/prompt.py"),
    ("candidate_translator_sha256", "/candidate/py2mpy.py"),
    ("trusted_translator_sha256", "/reference/py2mpy.py"),
    ("run_manifest_sha256", "/run.json"),
    ("task_manifest_sha256", "/task.json"),
    ("stage1_result_sha256", "/generation-result.json"),
    ("stage1_invocation_sha256", "/generation-evidence/invocation.json"),
    ("generation_metrics_sha256", "/generation-evidence/metrics.json"),
    ("generation_runtime_metrics_sha256", "/generation-evidence/runtime-metrics.json"),
    ("generation_usage_sha256", "/generation-evidence/usage.json"),
    ("generation_codex_last_sha256", "/generation-evidence/codex-last.txt"),
    ("generation_codex_output_sha256", "/generation-evidence/codex-output.log"),
    ("generation_prompt_sha256", "/generation-evidence/prompt.txt"),
]
for field, raw_path in direct_hashes:
    path = Path(raw_path)
    actual = sha256_file(path) if path.is_file() else "MISSING_OR_NOT_FILE"
    expected = audit["hashes"].get(field, "UNDECLARED")
    print(f"hash {field}: actual={actual} expected={expected} match={actual == expected}")

required_json = [
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/runtime-metrics.json",
    "/generation-evidence/usage.json",
]
for raw_path in required_json:
    value = load_json(Path(raw_path))
    print(f"json {raw_path}: readable=yes top_type={type(value).__name__} keys={sorted(value) if isinstance(value, dict) else 'n/a'}")

for label, candidate_path, trusted_path in [
    ("prompt", Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
    ("translator", Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
]:
    candidate_hash = sha256_file(candidate_path)
    trusted_hash = sha256_file(trusted_path)
    print(f"{label}_byte_identity:", candidate_hash == trusted_hash, candidate_hash, trusted_hash)

candidate_semantics = inventory(Path("/candidate/reference-semantics"))
trusted_semantics = inventory(Path("/reference/reference-semantics"))
print("candidate_semantics_entries:", len(candidate_semantics))
print("trusted_semantics_entries:", len(trusted_semantics))
print("semantics_inventory_equal:", candidate_semantics == trusted_semantics)
for rel in sorted(set(candidate_semantics) | set(trusted_semantics)):
    if candidate_semantics.get(rel) != trusted_semantics.get(rel):
        print("semantics_difference:", rel, candidate_semantics.get(rel), trusted_semantics.get(rel))
for root in ["/candidate", "/reference", "/generation-evidence"]:
    links = [rel for rel, value in inventory(Path(root)).items() if value[0] == "symlink"]
    print(f"symlinks {root}:", links)

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
print("trace_files:", [str(path.relative_to(trace_root)) for path in trace_files])
line_count = 0
type_counts = collections.Counter()
parse_errors = []
for path in trace_files:
    with path.open("r", encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            line_count += 1
            try:
                item = json.loads(line)
            except Exception as error:
                parse_errors.append((str(path), number, repr(error)))
                continue
            if isinstance(item, dict):
                type_counts[str(item.get("type", "<none>"))] += 1
            else:
                type_counts[type(item).__name__] += 1
print("trace_line_count:", line_count)
print("trace_type_counts:", dict(sorted(type_counts.items())))
print("trace_parse_errors:", parse_errors)
