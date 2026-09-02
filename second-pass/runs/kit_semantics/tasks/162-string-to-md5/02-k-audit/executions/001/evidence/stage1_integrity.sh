#!/usr/bin/env bash
set -uo pipefail

audit_input=/audit-input.json
campaign_lock=/audit-campaign-lock.json
candidate=/candidate
reference=/reference
generation=/generation-evidence

echo 'COMMAND: bash /audit-output/evidence/stage1_integrity.sh'
echo
echo '== Required pipeline-v3 records: type, size, SHA-256 =='
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
missing=0
for path in "${required[@]}"; do
  if [[ ! -r "$path" ]]; then
    echo "MISSING_OR_UNREADABLE $path"
    missing=1
    continue
  fi
  if [[ -L "$path" ]]; then
    echo "SYMLINK $path -> $(readlink "$path")"
  elif [[ -f "$path" ]]; then
    stat -c 'FILE %n %s bytes' "$path"
    sha256sum "$path"
  elif [[ -d "$path" ]]; then
    stat -c 'DIRECTORY %n' "$path"
  else
    stat -c 'OTHER %F %n' "$path"
  fi
done
echo "REQUIRED_MISSING=$missing"

echo
echo '== Campaign block comparison =='
python3 - "$audit_input" "$campaign_lock" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    audit_input = json.load(handle)
with open(sys.argv[2], encoding="utf-8") as handle:
    campaign_lock = json.load(handle)
print("CAMPAIGN_BLOCK_MATCH=" + ("yes" if audit_input["audit_campaign"] == campaign_lock else "no"))
if audit_input["audit_campaign"] != campaign_lock:
    print("AUDIT_INPUT_CAMPAIGN=" + json.dumps(audit_input["audit_campaign"], sort_keys=True))
    print("CAMPAIGN_LOCK=" + json.dumps(campaign_lock, sort_keys=True))
PY
actual_lock=$(sha256sum "$campaign_lock" | cut -d' ' -f1)
recorded_lock=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["hashes"]["audit_campaign_lock_sha256"])' "$audit_input")
echo "CAMPAIGN_LOCK_SHA_ACTUAL=$actual_lock"
echo "CAMPAIGN_LOCK_SHA_RECORDED=$recorded_lock"
[[ "$actual_lock" == "$recorded_lock" ]] && echo 'CAMPAIGN_LOCK_SHA_MATCH=yes' || echo 'CAMPAIGN_LOCK_SHA_MATCH=no'

echo
echo '== Declared regular-file hash checks =='
check_hash() {
  local key=$1
  local path=$2
  local actual recorded
  actual=$(sha256sum "$path" | cut -d' ' -f1)
  recorded=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["hashes"][sys.argv[2]])' "$audit_input" "$key")
  printf '%s %s\n  actual=%s\n  recorded=%s\n' "$key" "$path" "$actual" "$recorded"
  [[ "$actual" == "$recorded" ]] && echo '  match=yes' || echo '  match=no'
}
check_hash canonical_sha256 /reference/canonical.py
check_hash trusted_prompt_sha256 /reference/prompt.py
check_hash trusted_translator_sha256 /reference/py2mpy.py
check_hash candidate_prompt_sha256 /candidate/prompt.py
check_hash candidate_translator_sha256 /candidate/py2mpy.py
check_hash run_manifest_sha256 /run.json
check_hash task_manifest_sha256 /task.json
check_hash stage1_result_sha256 /generation-result.json
check_hash stage1_invocation_sha256 /generation-evidence/invocation.json
check_hash generation_metrics_sha256 /generation-evidence/metrics.json
check_hash generation_runtime_metrics_sha256 /generation-evidence/runtime-metrics.json
check_hash generation_usage_sha256 /generation-evidence/usage.json
check_hash generation_codex_last_sha256 /generation-evidence/codex-last.txt
check_hash generation_codex_output_sha256 /generation-evidence/codex-output.log
check_hash generation_prompt_sha256 /generation-evidence/prompt.txt

echo
echo '== Candidate/trusted byte comparisons =='
cmp -s /candidate/prompt.py /reference/prompt.py
echo "PROMPT_CMP_EXIT=$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
echo "TRANSLATOR_CMP_EXIT=$?"

echo
echo '== Symlink checks =='
for root in /candidate /reference /generation-evidence; do
  count=$(find "$root" -type l -print | tee /dev/stderr | wc -l)
  echo "SYMLINK_COUNT $root $count"
done

echo
echo '== Supplied-semantics recursive comparison =='
diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
echo "SEMANTICS_DIFF_EXIT=$?"

echo
echo '== Trusted semantics independent file manifest =='
(
  cd /reference/reference-semantics
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)

echo
echo '== Candidate semantics independent file manifest =='
(
  cd /candidate/reference-semantics
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)

echo
echo '== Source candidate artifact manifest (compiled caches excluded) =='
find /candidate -maxdepth 1 -type f -print0 | sort -z | xargs -0 sha256sum

echo
echo '== Generation trace independent manifest =='
(
  cd /generation-evidence/codex-trace
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)

echo
echo '== Candidate and trusted semantics entry counts/types =='
for root in /candidate/reference-semantics /reference/reference-semantics; do
  printf '%s files=%s dirs=%s symlinks=%s other=%s\n' \
    "$root" \
    "$(find "$root" -type f | wc -l)" \
    "$(find "$root" -type d | wc -l)" \
    "$(find "$root" -type l | wc -l)" \
    "$(find "$root" ! -type f ! -type d ! -type l | wc -l)"
done

exit "$missing"
