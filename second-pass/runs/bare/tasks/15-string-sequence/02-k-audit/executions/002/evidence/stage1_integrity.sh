#!/usr/bin/env bash
set -u

printf 'COMMAND: bash /audit-output/evidence/stage1_integrity.sh\n'
printf 'Required launcher records and mounted source types\n'
required_files=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /candidate/prompt.py
  /candidate/py2mpy.py
)
status=0
for path in "${required_files[@]}"; do
  if [[ -f "$path" && ! -L "$path" ]]; then
    stat -Lc 'OK regular|%n|mode=%a|size=%s' "$path"
  else
    printf 'BAD required file|%s\n' "$path"
    status=1
  fi
done

for path in /candidate /generation-evidence /generation-evidence/codex-trace /reference; do
  if [[ -d "$path" && ! -L "$path" ]]; then
    stat -Lc 'OK directory|%n|mode=%a' "$path"
  else
    printf 'BAD required directory|%s\n' "$path"
    status=1
  fi
done

printf '\nSymlinks or unsupported nodes in mounted trees\n'
special_count="$(
  find /candidate /generation-evidence /reference \
    ! -type f ! -type d -printf '%y|%p\n' | wc -l
)"
printf 'special-node-count=%s\n' "$special_count"
find /candidate /generation-evidence /reference \
  ! -type f ! -type d -printf '%y|%p\n' | LC_ALL=C sort
if [[ "$special_count" != 0 ]]; then
  status=1
fi

printf '\nFile SHA-256 values\n'
sha256sum "${required_files[@]}"

printf '\nCandidate/trusted byte comparisons\n'
cmp -s /candidate/prompt.py /reference/prompt.py
cmp_prompt=$?
printf 'prompt_cmp_exit=%s\n' "$cmp_prompt"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
cmp_translator=$?
printf 'translator_cmp_exit=%s\n' "$cmp_translator"
if [[ "$cmp_prompt" != 0 || "$cmp_translator" != 0 ]]; then
  status=1
fi

printf '\nGenerated-semantics boundary\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'BAD trusted reference semantics unexpectedly present\n'
  status=1
else
  printf 'OK /reference/reference-semantics absent\n'
fi

printf '\nRead-only mount observations\n'
for path in \
  /candidate \
  /generation-evidence \
  /run.json \
  /task.json \
  /generation-result.json \
  /audit-input.json \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py
do
  findmnt -T "$path" -n -o TARGET,OPTIONS
done

printf '\nStructured comparisons and independent tree digests\n'
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/opt/humaneval/tools python3 - <<'PY'
import json
from pathlib import Path
import pipeline_contract

audit_input = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_block_equal_lock={audit_input['audit_campaign'] == lock}")
print(
    "recorded_launcher_candidate_tree_sha256="
    f"{audit_input['hashes']['candidate_tree_sha256']}"
)
print(
    "recorded_launcher_trace_tree_sha256="
    f"{audit_input['hashes']['generation_codex_trace_sha256']}"
)
print(
    "campaign_lock_file_sha256_recorded="
    f"{audit_input['hashes']['audit_campaign_lock_sha256']}"
)
for label, path in (
    ("candidate", Path("/candidate")),
    ("trace", Path("/generation-evidence/codex-trace")),
):
    print(
        f"{label}_pipeline_contract_sha256_tree="
        f"{pipeline_contract.sha256_tree(path)}"
    )
print(
    "candidate_generation_workspace_sha256="
    f"{json.loads(Path('/generation-result.json').read_text())['outputs']['workspace_sha256']}"
)
print(
    "trace_usage_source_sha256="
    f"{json.loads(Path('/generation-evidence/usage.json').read_text())['source_trace_sha256']}"
)
PY
python_status=$?
if [[ "$python_status" != 0 ]]; then
  status=1
fi

printf '\nSCRIPT_EXIT=%s\n' "$status"
exit "$status"
