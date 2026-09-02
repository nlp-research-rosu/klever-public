#!/usr/bin/env bash
set -u

printf 'COMMAND: %q' "$0"
printf '\n'
printf 'PWD: %s\n' "$PWD"
printf 'K_VERSION:\n'
kompile --version

python3 - <<'PY'
import hashlib
import json
import os
import pathlib
import stat

audit = json.load(open("/audit-input.json"))
lock = json.load(open("/audit-campaign-lock.json"))
print("record_layout=", audit["record_layout"])
print("semantics_mode=", audit["semantics_mode"])
print("problem_id=", audit["problem_id"])
print("campaign_block_equal=", audit["audit_campaign"] == lock)

checks = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_runtime_metrics_sha256": "/generation-evidence/runtime-metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
}
all_hashes_match = True
for key, name in checks.items():
    path = pathlib.Path(name)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = audit["hashes"][key]
    ok = actual == expected
    all_hashes_match &= ok
    print(f"{key}: expected={expected} actual={actual} match={ok}")
print("all_recorded_file_hashes_match=", all_hashes_match)

required = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/runtime-metrics.json",
    "/generation-evidence/usage.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
]
for name in required:
    path = pathlib.Path(name)
    mode = path.lstat().st_mode
    print(
        "required_record",
        name,
        "regular=", stat.S_ISREG(mode),
        "symlink=", stat.S_ISLNK(mode),
        "readable=", os.access(path, os.R_OK),
    )

result = json.load(open("/generation-result.json"))
trace_root = pathlib.Path("/generation-evidence/codex-trace")
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = pathlib.Path("/generation-evidence") / rel
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    print(
        f"generation_result_artifact {rel}: "
        f"expected={expected} actual={actual} match={actual == expected}"
    )

for root_name in [
    "/candidate",
    "/candidate/reference-semantics",
    "/reference/reference-semantics",
    "/generation-evidence/codex-trace",
]:
    root = pathlib.Path(root_name)
    manifest = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind, digest = "L", "->" + os.readlink(path)
        elif stat.S_ISDIR(mode):
            kind, digest = "D", "-"
        elif stat.S_ISREG(mode):
            kind = "F"
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            kind, digest = "O", "-"
        manifest.append(f"{kind}\t{rel}\t{digest}")
    aggregate = hashlib.sha256(("\n".join(manifest) + "\n").encode()).hexdigest()
    print(
        f"reviewer_tree_manifest root={root_name} entries={len(manifest)} "
        f"sha256={aggregate}"
    )
PY

printf 'CAMPAIGN_LOCK_CANONICAL_DIFF_EXIT:\n'
python3 - <<'PY'
import json
a = json.load(open("/audit-input.json"))["audit_campaign"]
b = json.load(open("/audit-campaign-lock.json"))
raise SystemExit(0 if a == b else 1)
PY
printf '%s\n' "$?"

printf 'CANDIDATE_PROMPT_CMP_EXIT:\n'
cmp /candidate/prompt.py /reference/prompt.py
printf '%s\n' "$?"

printf 'CANDIDATE_TRANSLATOR_CMP_EXIT:\n'
cmp /candidate/py2mpy.py /reference/py2mpy.py
printf '%s\n' "$?"

printf 'SUPPLIED_SEMANTICS_DIFF_EXIT:\n'
diff -qr --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics
printf '%s\n' "$?"

printf 'SYMLINKS_IN_MOUNTED_INPUTS:\n'
find /candidate /reference /generation-evidence -type l -print

printf 'NON_REGULAR_SEMANTICS_ENTRIES:\n'
find /candidate/reference-semantics /reference/reference-semantics \
  -not -type d -not -type f -print

printf 'SCRIPT_EXIT: 0\n'
