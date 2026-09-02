#!/usr/bin/env bash
set -u

status=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

printf 'STAGE 1 INPUT AND PROVENANCE INTEGRITY\n'
run sha256sum /audit-input.json /audit-campaign-lock.json /run.json /task.json /generation-result.json \
  /generation-evidence/invocation.json /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/30/rollout-2026-07-30T02-20-25-019fb1e5-56e1-7352-925d-65ad37bb1077.jsonl \
  /reference/canonical.py /reference/prompt.py /reference/py2mpy.py \
  /candidate/prompt.py /candidate/py2mpy.py

run python3 -c '
import hashlib, json, pathlib, sys
a = json.loads(pathlib.Path("/audit-input.json").read_text())
lraw = pathlib.Path("/audit-campaign-lock.json").read_bytes()
lock = json.loads(lraw)
checks = {
  "record_layout_pipeline_v3": a.get("record_layout") == "pipeline-v3",
  "semantics_mode_supplied": a.get("semantics_mode") == "SUPPLIED_SEMANTICS",
  "reference_semantics_mounted": pathlib.Path("/reference/reference-semantics").is_dir(),
  "campaign_object_exact_match": a.get("audit_campaign") == lock,
  "campaign_lock_sha256": hashlib.sha256(lraw).hexdigest() == a["hashes"]["audit_campaign_lock_sha256"],
}
for name, ok in checks.items():
    print(f"{name}: {ok}")
if not all(checks.values()):
    sys.exit(1)
'

run python3 -c '
import hashlib, json, pathlib, sys
a = json.loads(pathlib.Path("/audit-input.json").read_text())
mapping = {
 "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
 "canonical_sha256": "/reference/canonical.py",
 "trusted_prompt_sha256": "/reference/prompt.py",
 "trusted_translator_sha256": "/reference/py2mpy.py",
 "candidate_prompt_sha256": "/candidate/prompt.py",
 "candidate_translator_sha256": "/candidate/py2mpy.py",
 "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
 "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
 "generation_metrics_sha256": "/generation-evidence/metrics.json",
 "generation_prompt_sha256": "/generation-evidence/prompt.txt",
 "generation_runtime_metrics_sha256": "/generation-evidence/runtime-metrics.json",
 "generation_usage_sha256": "/generation-evidence/usage.json",
 "run_manifest_sha256": "/run.json",
 "stage1_invocation_sha256": "/generation-evidence/invocation.json",
 "stage1_result_sha256": "/generation-result.json",
 "task_manifest_sha256": "/task.json",
}
bad = []
for key, path in mapping.items():
    actual = hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
    expected = a["hashes"][key]
    ok = actual == expected
    print(f"{key}: {ok} expected={expected} actual={actual} path={path}")
    if not ok:
        bad.append(key)
if bad:
    sys.exit(1)
'

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics

run python3 -c '
from pathlib import Path
import sys
roots = [Path("/candidate"), Path("/reference"), Path("/generation-evidence")]
bad = []
for root in roots:
    for p in root.rglob("*"):
        if p.is_symlink():
            bad.append(str(p))
print("symlinks:", bad)
if bad:
    sys.exit(1)
'

run python3 -c '
import json, pathlib, collections, sys
p = pathlib.Path("/generation-evidence/codex-trace/2026/07/30/rollout-2026-07-30T02-20-25-019fb1e5-56e1-7352-925d-65ad37bb1077.jsonl")
counts = collections.Counter()
bad = []
for i, line in enumerate(p.open(), 1):
    try:
        event = json.loads(line)
    except Exception as e:
        bad.append((i, str(e)))
        continue
    counts[event.get("type", "<missing>")] += 1
print("jsonl_lines:", sum(counts.values()) + len(bad))
print("event_type_counts:", dict(counts))
print("malformed_lines:", bad)
if bad:
    sys.exit(1)
'

printf '\nREQUIRED PIPELINE-V3 RECORD TYPES\n'
run find /audit-input.json /audit-campaign-lock.json /run.json /task.json /generation-result.json \
  /generation-evidence/invocation.json /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt /generation-evidence/codex-trace \
  -maxdepth 0 -printf '%y %m %s %p -> %l\n'

printf '\nCANDIDATE TOP-LEVEL TYPE INVENTORY\n'
run find /candidate -mindepth 1 -maxdepth 1 -printf '%y %m %s %f -> %l\n'

printf '\nTRUSTED/CANDIDATE SEMANTICS TYPE AND HASH MANIFESTS\n'
(cd /reference/reference-semantics && find . -printf '%y %P\n' | LC_ALL=C sort) \
  > /audit-output/evidence/trusted-semantics-types.txt
(cd /candidate/reference-semantics && find . -printf '%y %P\n' | LC_ALL=C sort) \
  > /audit-output/evidence/candidate-semantics-types.txt
(cd /reference/reference-semantics && find . -type f -printf '%P\n' | LC_ALL=C sort | while IFS= read -r f; do sha256sum "$f"; done) \
  > /audit-output/evidence/trusted-semantics-sha256.txt
(cd /candidate/reference-semantics && find . -type f -printf '%P\n' | LC_ALL=C sort | while IFS= read -r f; do sha256sum "$f"; done) \
  > /audit-output/evidence/candidate-semantics-sha256.txt
run cmp -s /audit-output/evidence/trusted-semantics-types.txt /audit-output/evidence/candidate-semantics-types.txt
run cmp -s /audit-output/evidence/trusted-semantics-sha256.txt /audit-output/evidence/candidate-semantics-sha256.txt
run sha256sum /audit-output/evidence/trusted-semantics-types.txt \
  /audit-output/evidence/trusted-semantics-sha256.txt \
  /audit-output/evidence/candidate-semantics-types.txt \
  /audit-output/evidence/candidate-semantics-sha256.txt

printf '\nGENERATION CLAIM SURFACES (UNTRUSTED)\n'
run sed -n 1,220p /generation-evidence/codex-last.txt
run sed -n 1,140p /generation-evidence/prompt.txt
run sed -n 1,100p /generation-evidence/codex-output.log
run tail -n 120 /generation-evidence/codex-output.log
run rg -n -i '(^|[^[:alpha:]])(#Top|kprove|kompile|proof|fail|error|timeout|vacu|bridge|connection)' \
  /generation-evidence/codex-last.txt /generation-evidence/codex-output.log

exit "$status"
