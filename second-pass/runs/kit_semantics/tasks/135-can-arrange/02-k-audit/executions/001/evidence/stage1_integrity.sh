#!/usr/bin/env bash
set -u

trace=/generation-evidence/codex-trace/2026/07/30/rollout-2026-07-30T02-45-10-019fb1fb-ff7f-7180-8c06-e4a69188db77.jsonl

echo 'COMMAND: sha256sum launcher-owned records and trusted/candidate inputs'
sha256sum \
  /audit-input.json \
  /audit-campaign-lock.json \
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
  "$trace" \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py
hash_status=$?
echo "EXIT sha256sum: $hash_status"

echo 'COMMAND: compare campaign block, required record hashes, and trace JSON structure'
python3 - <<'PY'
import collections
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print("campaign_block_equals_lock", audit["audit_campaign"] == lock)

checks = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
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
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
}
for key, path in checks.items():
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    expected = audit["hashes"][key]
    print(key, "OK" if actual == expected else "MISMATCH", actual)

trace = Path("/generation-evidence/codex-trace/2026/07/30/"
             "rollout-2026-07-30T02-45-10-019fb1fb-ff7f-7180-8c06-e4a69188db77.jsonl")
counts = collections.Counter()
errors = []
for line_number, line in enumerate(trace.open(encoding="utf-8"), 1):
    try:
        event = json.loads(line)
    except Exception as err:
        errors.append((line_number, str(err)))
        continue
    counts[event.get("type", "<missing>")] += 1
print("trace_line_count", sum(counts.values()) + len(errors))
print("trace_type_counts", dict(sorted(counts.items())))
print("trace_json_errors", errors)
PY
json_status=$?
echo "EXIT provenance JSON check: $json_status"

echo 'COMMAND: require all pipeline-v3 records and declared mounts to be readable regular files/directories'
for path in \
  /audit-input.json \
  /audit-campaign-lock.json \
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
  "$trace" \
  /candidate \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/reference-semantics
do
  if test -r "$path" && ! test -L "$path"; then
    echo "OK $path"
  else
    echo "BAD $path"
  fi
done

echo 'COMMAND: cmp candidate prompt and translator against trusted mounts'
cmp /candidate/prompt.py /reference/prompt.py
prompt_status=$?
echo "EXIT prompt cmp: $prompt_status"
cmp /candidate/py2mpy.py /reference/py2mpy.py
translator_status=$?
echo "EXIT translator cmp: $translator_status"

echo 'COMMAND: recursively compare candidate supplied semantics against trusted tree'
diff -qr --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics
semantics_status=$?
echo "EXIT supplied-semantics diff: $semantics_status"

echo 'COMMAND: search candidate, generation, and trusted semantics for symlinks'
find \
  /candidate \
  /generation-evidence \
  /reference/reference-semantics \
  -type l -printf '%p -> %l\n'
symlink_status=$?
echo "EXIT symlink search: $symlink_status"

echo 'COMMAND: independent sorted file manifest for trusted semantics'
find /reference/reference-semantics -type f -print0 |
  sort -z |
  xargs -0 sha256sum
manifest_status=$?
echo "EXIT semantics manifest: $manifest_status"

if test "$hash_status" -eq 0 &&
   test "$json_status" -eq 0 &&
   test "$prompt_status" -eq 0 &&
   test "$translator_status" -eq 0 &&
   test "$semantics_status" -eq 0 &&
   test "$symlink_status" -eq 0 &&
   test "$manifest_status" -eq 0
then
  exit 0
fi
exit 1
