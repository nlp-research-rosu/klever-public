#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'Declared record layout and semantics mode:\n'
run sed -n '/"record_layout"/p; /"semantics_mode"/p; /"mount_reference_semantics"/p' /audit-input.json

printf '\nRequired mount types (symlinks would be visible as type l):\n'
run find /candidate /reference /generation-evidence -maxdepth 6 \
  -printf '%y %m %u:%g %p -> %l\n'
run stat -c '%F %a %U:%G %n' \
  /audit-input.json /audit-campaign-lock.json /run.json /task.json \
  /generation-result.json

printf '\nRequired legacy-selected-stage1 record hashes:\n'
run sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T08-01-45-019f89ea-f6f2-71c1-85b5-d5ec0f90f188.jsonl

printf '\nCandidate prompt and translator integrity:\n'
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py

printf '\nGENERATED_SEMANTICS boundary (trusted reference semantics must be absent):\n'
run test ! -e /reference/reference-semantics

printf '\nCampaign block exact comparison and declared-hash checks:\n'
run python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print("campaign_block_equal:", audit["audit_campaign"] == lock)

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
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
}
all_ok = audit["audit_campaign"] == lock
for field, path in checks.items():
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    expected = audit["hashes"][field]
    ok = actual == expected
    all_ok &= ok
    print(f"{field}: ok={ok} expected={expected} actual={actual}")

stage1 = json.loads(Path("/generation-result.json").read_text())
trace_rel = next(
    key for key in stage1["outputs"]["evidence"] if key.startswith("codex-trace/")
)
trace_path = Path("/generation-evidence") / trace_rel
trace_actual = hashlib.sha256(trace_path.read_bytes()).hexdigest()
trace_expected = stage1["outputs"]["evidence"][trace_rel]
trace_ok = trace_actual == trace_expected
all_ok &= trace_ok
print(
    f"structured_trace_file: ok={trace_ok} "
    f"expected={trace_expected} actual={trace_actual}"
)

required = [
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    str(trace_path),
]
missing = [path for path in required if not Path(path).is_file()]
print("missing_required_records:", missing)
all_ok &= not missing
raise SystemExit(0 if all_ok else 1)
PY

printf '\nAll candidate source hashes (independent file-level manifest):\n'
run find /candidate -type f -print0
run sha256sum \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/__pycache__/solution.cpython-310.pyc
