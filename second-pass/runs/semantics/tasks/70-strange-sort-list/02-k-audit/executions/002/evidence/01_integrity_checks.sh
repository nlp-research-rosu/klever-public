#!/usr/bin/env bash
set -u

status=0

check_regular() {
  local path="$1"
  if [[ -f "$path" && ! -L "$path" ]]; then
    echo "OK regular file: $path"
  else
    echo "ERROR required regular file missing, unreadable, mistyped, or symlinked: $path"
    status=1
  fi
}

check_directory() {
  local path="$1"
  if [[ -d "$path" && ! -L "$path" ]]; then
    echo "OK directory: $path"
  else
    echo "ERROR required directory missing, unreadable, mistyped, or symlinked: $path"
    status=1
  fi
}

for path in \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py; do
  check_regular "$path"
done

for path in \
  /candidate \
  /reference/reference-semantics \
  /candidate/reference-semantics \
  /generation-evidence/codex-trace; do
  check_directory "$path"
done

echo "SHA-256 values for launcher-declared records and mounts:"
sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T01-38-03-019f8db2-0cdc-7f62-9c44-0e3c14e1d18d.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

echo "Candidate symlinks (must be empty):"
find /candidate -type l -printf '%p -> %l\n' | sort
echo "Trusted semantics symlinks (must be empty):"
find /reference/reference-semantics -type l -printf '%p -> %l\n' | sort

echo "Candidate versus trusted prompt:"
if cmp -s /candidate/prompt.py /reference/prompt.py; then
  echo "IDENTICAL"
else
  echo "DIFFERENT"
  status=1
fi

echo "Candidate versus trusted translator:"
if cmp -s /candidate/py2mpy.py /reference/py2mpy.py; then
  echo "IDENTICAL"
else
  echo "DIFFERENT"
  status=1
fi

echo "Candidate versus trusted supplied-semantics tree:"
if diff --no-dereference --recursive --brief \
    /candidate/reference-semantics /reference/reference-semantics; then
  echo "IDENTICAL"
else
  echo "DIFFERENT"
  status=1
fi

echo "Deterministic supplied-semantics file manifests:"
(
  cd /candidate/reference-semantics
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)
(
  cd /reference/reference-semantics
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)

echo "Campaign block semantic comparison:"
python3 -c 'import json; a=json.load(open("/audit-input.json")); b=json.load(open("/audit-campaign-lock.json")); print("MATCH" if a["audit_campaign"] == b else "MISMATCH"); raise SystemExit(0 if a["audit_campaign"] == b else 1)' || status=1

echo "Declared SHA-256 comparison:"
python3 - <<'PY' || status=1
import hashlib
import json

audit = json.load(open("/audit-input.json"))
declared = audit["hashes"]
checks = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_usage_sha256": "/generation-evidence/usage.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
}
ok = True
for key, path in checks.items():
    actual = hashlib.sha256(open(path, "rb").read()).hexdigest()
    expected = declared[key]
    match = actual == expected
    ok &= match
    print(f"{key}: {'MATCH' if match else 'MISMATCH'} expected={expected} actual={actual}")
raise SystemExit(0 if ok else 1)
PY

exit "$status"
