#!/usr/bin/env python3
import hashlib
import json
import os
import stat


def digest(path: str) -> str:
    value = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


with open("/audit-input.json", encoding="utf-8") as stream:
    audit_input = json.load(stream)
with open("/audit-campaign-lock.json", encoding="utf-8") as stream:
    campaign_lock = json.load(stream)

ok = True
campaign_match = audit_input["audit_campaign"] == campaign_lock
print(f"campaign_block_equals_lock={campaign_match}")
ok &= campaign_match

paths = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_runtime_metrics_sha256": (
        "/generation-evidence/runtime-metrics.json"
    ),
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
}
for key, path in paths.items():
    expected = audit_input["hashes"][key]
    actual = digest(path)
    match = actual == expected
    print(f"{key} expected={expected} actual={actual} match={match}")
    ok &= match

declared_paths = audit_input["container_paths"]
for name, path in sorted(declared_paths.items()):
    exists = os.path.lexists(path)
    is_link = os.path.islink(path) if exists else False
    mode = stat.S_IFMT(os.lstat(path).st_mode) if exists else None
    print(
        f"container_path {name} path={path} exists={exists} "
        f"symlink={is_link} mode_type={mode}"
    )
    ok &= exists and not is_link

with open("/generation-result.json", encoding="utf-8") as stream:
    result = json.load(stream)
for relative_path, expected in sorted(
    result["outputs"]["evidence"].items()
):
    path = os.path.join("/generation-evidence", relative_path)
    actual = digest(path)
    match = actual == expected
    print(
        f"generation_result_hash path={relative_path} "
        f"expected={expected} actual={actual} match={match}"
    )
    ok &= match

print(f"EXIT_STATUS: {0 if ok else 1}")
raise SystemExit(0 if ok else 1)
