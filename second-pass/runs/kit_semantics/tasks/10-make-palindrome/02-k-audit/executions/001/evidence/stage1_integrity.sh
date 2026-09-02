#!/usr/bin/env bash
set -euo pipefail

echo 'AUDIT COMMAND: bash /audit-output/evidence/stage1_integrity.sh'
echo 'CHECK: required launcher and pipeline-v3 records are real regular files/directories'
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
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/PROOF.md
do
  stat -c '%F %s %n' "$path"
done
stat -c '%F %n' \
  /candidate \
  /reference/reference-semantics \
  /candidate/reference-semantics \
  /generation-evidence/codex-trace

echo 'CHECK: no linked or unsupported entries in provenance, trusted, or supplied-semantics trees'
linked_count="$(
  find \
    /generation-evidence \
    /reference \
    /candidate/reference-semantics \
    -type l -print | wc -l
)"
echo "linked_entry_count=$linked_count"
test "$linked_count" -eq 0

echo 'CHECK: campaign lock content equals audit-input audit_campaign and its SHA-256 matches'
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
lock_path = Path("/audit-campaign-lock.json")
lock = json.loads(lock_path.read_text())
actual = hashlib.sha256(lock_path.read_bytes()).hexdigest()
expected = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"campaign_json_equal={lock == audit['audit_campaign']}")
print(f"campaign_lock_actual={actual}")
print(f"campaign_lock_expected={expected}")
assert lock == audit["audit_campaign"]
assert actual == expected
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["mount_reference_semantics"] is True
PY

echo 'CHECK: independently hash all mounted regular-file provenance records'
sha256sum \
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
  /generation-evidence/codex-trace/2026/07/29/*.jsonl

echo 'CHECK: declared individual file hashes and generation-result evidence hashes'
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

audit = json.loads(Path("/audit-input.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
checks = {
    "/audit-campaign-lock.json": audit["hashes"]["audit_campaign_lock_sha256"],
    "/reference/canonical.py": audit["hashes"]["canonical_sha256"],
    "/reference/prompt.py": audit["hashes"]["trusted_prompt_sha256"],
    "/reference/py2mpy.py": audit["hashes"]["trusted_translator_sha256"],
    "/candidate/prompt.py": audit["hashes"]["candidate_prompt_sha256"],
    "/candidate/py2mpy.py": audit["hashes"]["candidate_translator_sha256"],
    "/run.json": audit["hashes"]["run_manifest_sha256"],
    "/task.json": audit["hashes"]["task_manifest_sha256"],
    "/generation-result.json": audit["hashes"]["stage1_result_sha256"],
    "/generation-evidence/invocation.json": audit["hashes"]["stage1_invocation_sha256"],
    "/generation-evidence/metrics.json": audit["hashes"]["generation_metrics_sha256"],
    "/generation-evidence/runtime-metrics.json": audit["hashes"]["generation_runtime_metrics_sha256"],
    "/generation-evidence/usage.json": audit["hashes"]["generation_usage_sha256"],
    "/generation-evidence/codex-last.txt": audit["hashes"]["generation_codex_last_sha256"],
    "/generation-evidence/codex-output.log": audit["hashes"]["generation_codex_output_sha256"],
    "/generation-evidence/prompt.txt": audit["hashes"]["generation_prompt_sha256"],
}
for path, expected in checks.items():
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    ok = actual == expected
    print(f"{path}: match={ok} actual={actual}")
    assert ok
for relative, expected in result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    ok = actual == expected
    print(f"result-evidence {relative}: match={ok} actual={actual}")
    assert ok
PY

echo 'CHECK: launcher-compatible tree hashes for mounted candidate, semantics, and trace'
PYTHONPATH=/opt/humaneval/tools python3 - <<'PY'
import json
from pathlib import Path
from pipeline_contract import sha256_tree

audit = json.loads(Path("/audit-input.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
trees = {
    "/candidate": sha256_tree(Path("/candidate")),
    "/candidate/reference-semantics": sha256_tree(Path("/candidate/reference-semantics")),
    "/reference/reference-semantics": sha256_tree(Path("/reference/reference-semantics")),
    "/generation-evidence/codex-trace": sha256_tree(Path("/generation-evidence/codex-trace")),
}
for path, digest in trees.items():
    print(f"{digest}  {path}")
assert trees["/candidate"] == result["outputs"]["workspace_sha256"]
assert trees["/candidate/reference-semantics"] == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
assert trees["/reference/reference-semantics"] == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
assert trees["/generation-evidence/codex-trace"] == json.loads(
    Path("/generation-evidence/usage.json").read_text()
)["source_trace_sha256"]
PY

echo 'CHECK: candidate prompt and translator are byte-identical to trusted mounts'
cmp /candidate/prompt.py /reference/prompt.py
echo "prompt_cmp_exit=$?"
cmp /candidate/py2mpy.py /reference/py2mpy.py
echo "translator_cmp_exit=$?"

echo 'CHECK: supplied candidate semantics recursively equal the trusted tree'
diff -r --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics
echo "semantics_recursive_diff_exit=$?"

echo 'CHECK: all generation JSON and JSONL records parse'
python3 /audit-output/evidence/inspect_generation_trace.py

echo 'STAGE1_INTEGRITY_EXIT=0'
