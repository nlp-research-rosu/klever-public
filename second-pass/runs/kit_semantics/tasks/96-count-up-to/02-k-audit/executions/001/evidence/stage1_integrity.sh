#!/usr/bin/env bash
set -u
set -o pipefail
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

sha256sum \
  /audit-campaign-lock.json \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/canonical.py \
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
  /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T01-30-39-019f97f7-fd2b-7d23-9c10-a2fa3527fded.jsonl

python3 -c 'import json; a=json.load(open("/audit-input.json")); b=json.load(open("/audit-campaign-lock.json")); print("campaign_lock_equals_audit_campaign:", b == a["audit_campaign"]); print("record_layout:", a["record_layout"]); print("semantics_mode:", a["semantics_mode"]); print("container_paths:", json.dumps(a["container_paths"], sort_keys=True))'

cmp /candidate/prompt.py /reference/prompt.py
echo "candidate_prompt_cmp_exit=$?"
cmp /candidate/py2mpy.py /reference/py2mpy.py
echo "candidate_translator_cmp_exit=$?"
diff --no-dereference --recursive --brief \
  /candidate/reference-semantics /reference/reference-semantics
echo "reference_semantics_recursive_diff_exit=$?"

diff -u \
  <(cd /candidate/reference-semantics && find . -printf '%P %y\n' | LC_ALL=C sort) \
  <(cd /reference/reference-semantics && find . -printf '%P %y\n' | LC_ALL=C sort)
echo "reference_semantics_type_manifest_diff_exit=$?"

find /candidate/reference-semantics /reference/reference-semantics \
  -type l -printf 'SYMLINK %p -> %l\n'
echo "reference_semantics_symlink_scan_exit=$?"

python3 -c 'from pathlib import Path; from hashlib import sha256
for root in (Path("/candidate/reference-semantics"), Path("/reference/reference-semantics")):
 h=sha256()
 files=sorted(p for p in root.rglob("*") if p.is_file() and not p.is_symlink())
 for p in files:
  rel=p.relative_to(root).as_posix().encode()
  body=p.read_bytes()
  h.update(len(rel).to_bytes(8,"big")); h.update(rel)
  h.update(len(body).to_bytes(8,"big")); h.update(body)
 print(root, "reviewer_tree_sha256="+h.hexdigest(), "files="+str(len(files)))'

for required in \
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
  /generation-evidence/codex-trace
do
  stat -c '%F mode=%a size=%s %n' "$required"
done

find \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/reference-semantics \
  /reference \
  -type l -printf 'REQUIRED_ARTIFACT_SYMLINK %p -> %l\n'
echo "all_required_symlink_scan_exit=$?"

python3 -c 'import json
paths=["/audit-input.json","/audit-campaign-lock.json","/run.json","/task.json","/generation-result.json","/generation-evidence/invocation.json","/generation-evidence/metrics.json","/generation-evidence/runtime-metrics.json","/generation-evidence/usage.json"]
for p in paths:
 with open(p, encoding="utf-8") as f: json.load(f)
 print("VALID_JSON", p)'

python3 -c 'import hashlib,json,pathlib
a=json.load(open("/audit-input.json"))["hashes"]
mapping={
"audit_campaign_lock_sha256":"/audit-campaign-lock.json",
"candidate_prompt_sha256":"/candidate/prompt.py",
"candidate_translator_sha256":"/candidate/py2mpy.py",
"canonical_sha256":"/reference/canonical.py",
"generation_codex_last_sha256":"/generation-evidence/codex-last.txt",
"generation_codex_output_sha256":"/generation-evidence/codex-output.log",
"generation_metrics_sha256":"/generation-evidence/metrics.json",
"generation_prompt_sha256":"/generation-evidence/prompt.txt",
"generation_runtime_metrics_sha256":"/generation-evidence/runtime-metrics.json",
"generation_usage_sha256":"/generation-evidence/usage.json",
"run_manifest_sha256":"/run.json",
"stage1_invocation_sha256":"/generation-evidence/invocation.json",
"stage1_result_sha256":"/generation-result.json",
"task_manifest_sha256":"/task.json",
"trusted_prompt_sha256":"/reference/prompt.py",
"trusted_translator_sha256":"/reference/py2mpy.py"}
for key,path in mapping.items():
 actual=hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
 print(key, "MATCH" if actual==a[key] else "MISMATCH", "recorded="+a[key], "actual="+actual)'

python3 -c 'import hashlib,json,pathlib
r=json.load(open("/generation-result.json"))["outputs"]["evidence"]
i=json.load(open("/generation-evidence/invocation.json"))["outputs"]["evidence"]
root=pathlib.Path("/generation-evidence")
for rel,expected in sorted(r.items()):
 actual=hashlib.sha256((root/rel).read_bytes()).hexdigest()
 print("generation-result", rel, "MATCH" if actual==expected else "MISMATCH", expected, actual)
for rel,expected in sorted(i.items()):
 actual=hashlib.sha256((root/rel).read_bytes()).hexdigest()
 print("invocation", rel, "MATCH" if actual==expected else "MISMATCH", expected, actual)'
