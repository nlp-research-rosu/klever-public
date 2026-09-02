#!/usr/bin/env bash
set -u

echo '$ sha256sum /audit-input.json /audit-campaign-lock.json /run.json /task.json /generation-result.json /generation-evidence/{invocation.json,metrics.json,runtime-metrics.json,usage.json,codex-last.txt,codex-output.log,prompt.txt} /reference/{canonical.py,prompt.py,py2mpy.py} /candidate/{prompt.py,py2mpy.py}'
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
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py
echo "exit=$?"

echo '$ python3: compare audit_input.audit_campaign with campaign lock'
python3 - <<'PY'
import json
from pathlib import Path
audit_input = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print(f"campaign_block_equal={audit_input['audit_campaign'] == lock}")
raise SystemExit(0 if audit_input["audit_campaign"] == lock else 1)
PY
echo "campaign_block_compare_exit=$?"

echo '$ required pipeline-v3 records: type, symlink status, and readability'
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
  /generation-evidence/codex-trace \
  /candidate \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/reference-semantics
do
  if [[ -L "$path" ]]; then
    kind=symlink
  elif [[ -f "$path" ]]; then
    kind=file
  elif [[ -d "$path" ]]; then
    kind=directory
  else
    kind=missing-or-other
  fi
  if [[ -r "$path" ]]; then readable=yes; else readable=no; fi
  printf '%s type=%s readable=%s\n' "$path" "$kind" "$readable"
done

echo '$ find provenance trees for symlinks and non-regular entries'
find /candidate /reference/reference-semantics /generation-evidence/codex-trace \
  \( -type l -o \( ! -type f ! -type d \) \) -printf '%y %p -> %l\n'
echo "exit=$?"

echo '$ cmp candidate prompt and translator against trusted mounts'
cmp -l /candidate/prompt.py /reference/prompt.py
echo "prompt_cmp_exit=$?"
cmp -l /candidate/py2mpy.py /reference/py2mpy.py
echo "translator_cmp_exit=$?"

echo '$ recursively compare candidate reference-semantics against trusted tree'
diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics
echo "semantics_diff_exit=$?"

echo '$ sorted entry/type/mode inventories for both semantics trees'
for root in /candidate/reference-semantics /reference/reference-semantics
do
  echo "ROOT $root"
  find "$root" -printf '%P|%y|%m\n' | LC_ALL=C sort
done

echo '$ sha256sum all semantics files, relative paths'
for root in /candidate/reference-semantics /reference/reference-semantics
do
  echo "ROOT $root"
  find "$root" -type f -print0 |
    LC_ALL=C sort -z |
    xargs -0 sha256sum |
    sed "s#  $root/#  #"
done

echo '$ trace inventory and hashes'
find /generation-evidence/codex-trace -type f -printf '%P\n' | LC_ALL=C sort
find /generation-evidence/codex-trace -type f -print0 |
  LC_ALL=C sort -z |
xargs -0 sha256sum
echo "exit=$?"

echo '$ pipeline-v3 tree digests for candidate, supplied semantics, and trace'
PYTHONPATH=/opt/humaneval/tools python3 - <<'PY'
import json
from pathlib import Path
from pipeline_contract import sha256_tree

audit_input = json.loads(Path("/audit-input.json").read_text())
generation = json.loads(Path("/generation-result.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
task = json.loads(Path("/task.json").read_text())
values = {
    "candidate": sha256_tree(Path("/candidate")),
    "candidate_reference_semantics": sha256_tree(
        Path("/candidate/reference-semantics")
    ),
    "trusted_reference_semantics": sha256_tree(
        Path("/reference/reference-semantics")
    ),
    "generation_trace": sha256_tree(Path("/generation-evidence/codex-trace")),
}
for name, value in values.items():
    print(f"{name}={value}")
print(
    "candidate_matches_generation_workspace="
    f"{values['candidate'] == generation['outputs']['workspace_sha256']}"
)
print(
    "semantics_matches_task_manifest="
    f"{values['trusted_reference_semantics'] == task['inputs']['reference_semantics_sha256']}"
)
print(
    "trace_matches_usage_source="
    f"{values['generation_trace'] == usage['source_trace_sha256']}"
)
PY
echo "tree_digest_checks_exit=$?"
