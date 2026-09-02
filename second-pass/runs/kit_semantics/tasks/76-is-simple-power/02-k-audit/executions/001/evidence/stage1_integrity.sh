#!/usr/bin/env bash
set -uo pipefail

status=0

record() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

printf '## Required artifact types\n'
required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/runtime-metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace
  /candidate
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
)
for path in "${required[@]}"; do
  if [ ! -r "$path" ]; then
    printf 'MISSING_OR_UNREADABLE %s\n' "$path"
    status=1
  else
    stat -c '%F %a %s %n' "$path"
  fi
done

printf '\n## Symlink and unsupported-entry scan\n'
links=$(find /candidate /reference /generation-evidence -type l -print)
if [ -n "$links" ]; then
  printf '%s\n' "$links"
  status=1
else
  printf 'No symlinks under /candidate, /reference, or /generation-evidence.\n'
fi

printf '\n## Recorded-file SHA-256 values\n'
record sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T00-54-30-019f97d6-e477-7890-8ba7-e9c389a968a2.jsonl

printf '\n## JSON cross-checks and trace inspection\n'
python3 - <<'PY'
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
run = json.loads(Path("/run.json").read_text())
task = json.loads(Path("/task.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())

checks = {
    "record_layout_pipeline_v3": audit.get("record_layout") == "pipeline-v3",
    "semantics_mode_supplied": audit.get("semantics_mode") == "SUPPLIED_SEMANTICS",
    "campaign_block_equals_lock": audit.get("audit_campaign") == lock,
    "task_manifest_fields_match_embedded_manifest": all(
        audit.get("manifest", {}).get(key) == value for key, value in task.items()
    ),
    "embedded_manifest_only_adds_expected_config": (
        set(audit.get("manifest", {})) - set(task) == {"config"}
        and audit.get("manifest", {}).get("config") == audit.get("config")
    ),
    "run_id_matches": audit.get("run_id") == run.get("run_id"),
    "problem_id_matches": audit.get("problem_id") == task.get("problem_id"),
    "result_invocation_matches": result.get("invocation") == invocation.get("name"),
    "result_status_matches": result.get("status") == invocation.get("status"),
    "result_workspace_hash_matches": (
        result.get("outputs", {}).get("workspace_sha256")
        == invocation.get("outputs", {}).get("workspace_sha256")
    ),
}
for name, passed in checks.items():
    print(f"{name}: {passed}")
if not all(checks.values()):
    sys.exit(1)

declared = audit["hashes"]
file_checks = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_runtime_metrics_sha256": "/generation-evidence/runtime-metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
}
for field, filename in file_checks.items():
    actual = sha256(Path(filename).read_bytes()).hexdigest()
    ok = declared.get(field) == actual
    print(f"{field}: declared={declared.get(field)} actual={actual} match={ok}")
    if not ok:
        sys.exit(1)

trace_path = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T00-54-30-019f97d6-e477-7890-8ba7-e9c389a968a2.jsonl"
)
rows = []
for number, line in enumerate(trace_path.read_text().splitlines(), 1):
    try:
        rows.append(json.loads(line))
    except json.JSONDecodeError as error:
        print(f"trace JSON error at line {number}: {error}")
        sys.exit(1)
print(f"trace_json_lines={len(rows)}")
print("trace_top_types=" + json.dumps(Counter(row.get("type") for row in rows), sort_keys=True))
payload_types = Counter()
roles = Counter()
function_calls = []
for row in rows:
    payload = row.get("payload")
    if isinstance(payload, dict):
        payload_types[payload.get("type", "<none>")] += 1
        if "role" in payload:
            roles[payload["role"]] += 1
        if payload.get("type") == "function_call":
            function_calls.append(
                (payload.get("name"), payload.get("arguments", "")[:500])
            )
print("trace_payload_types=" + json.dumps(payload_types, sort_keys=True))
print("trace_roles=" + json.dumps(roles, sort_keys=True))
print(f"trace_function_call_count={len(function_calls)}")
for index, (name, arguments) in enumerate(function_calls, 1):
    compact = " ".join(str(arguments).split())
    print(f"trace_call[{index}] name={name} args={compact}")
PY
py_rc=$?
printf '[trace/json exit %d]\n' "$py_rc"
if [ "$py_rc" -ne 0 ]; then
  status=1
fi

printf '\n## Candidate/trusted prompt and translator byte comparisons\n'
record cmp -s /candidate/prompt.py /reference/prompt.py
record cmp -s /candidate/py2mpy.py /reference/py2mpy.py

printf '\n## Supplied-semantics entry/type/content comparison\n'
record diff -ru --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics

candidate_types=$(
  cd /candidate/reference-semantics &&
    find . -mindepth 1 -printf '%y %m %p\n' |
    sort
)
trusted_types=$(
  cd /reference/reference-semantics &&
    find . -mindepth 1 -printf '%y %m %p\n' |
    sort
)
if [ "$candidate_types" = "$trusted_types" ]; then
  printf 'Semantics entry names, types, and modes match exactly.\n'
else
  printf 'Semantics entry/type/mode mismatch.\n'
  diff -u <(printf '%s\n' "$trusted_types") <(printf '%s\n' "$candidate_types")
  status=1
fi

printf '\n## Launcher pipeline tree digests independently recomputed\n'
PYTHONPATH=/opt/humaneval/tools python3 - <<'PY'
from pathlib import Path
from pipeline_contract import sha256_tree

for path in (
    "/candidate",
    "/candidate/reference-semantics",
    "/reference/reference-semantics",
    "/generation-evidence/codex-trace",
):
    print(f"{sha256_tree(Path(path))}  {path}")
PY
tree_rc=$?
printf '[tree digest exit %d]\n' "$tree_rc"
if [ "$tree_rc" -ne 0 ]; then
  status=1
fi

printf '\n## Required candidate proof artifacts\n'
candidate_required=(
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
  /candidate/PROOF.md
)
for path in "${candidate_required[@]}"; do
  if [ -f "$path" ] && [ ! -L "$path" ] && [ -r "$path" ]; then
    stat -c 'OK %F %a %s %n' "$path"
  else
    printf 'BAD_REQUIRED_CANDIDATE_ARTIFACT %s\n' "$path"
    status=1
  fi
done

printf '\nSTAGE1_STATUS=%d\n' "$status"
exit "$status"
