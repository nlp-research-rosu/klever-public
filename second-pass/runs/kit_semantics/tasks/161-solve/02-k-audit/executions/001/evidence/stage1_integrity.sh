#!/usr/bin/env bash
set -uo pipefail

failures=0

check_regular() {
  local path="$1"
  if [[ -f "$path" && -r "$path" && ! -L "$path" ]]; then
    printf 'REGULAR_READABLE PASS %s\n' "$path"
  else
    printf 'REGULAR_READABLE FAIL %s\n' "$path"
    failures=$((failures + 1))
  fi
}

check_directory() {
  local path="$1"
  if [[ -d "$path" && -r "$path" && ! -L "$path" ]]; then
    printf 'DIRECTORY_READABLE PASS %s\n' "$path"
  else
    printf 'DIRECTORY_READABLE FAIL %s\n' "$path"
    failures=$((failures + 1))
  fi
}

check_sha() {
  local expected="$1"
  local path="$2"
  local actual
  actual="$(sha256sum "$path" | cut -d' ' -f1)"
  if [[ "$actual" == "$expected" ]]; then
    printf 'SHA256 PASS %s %s\n' "$actual" "$path"
  else
    printf 'SHA256 FAIL expected=%s actual=%s %s\n' "$expected" "$actual" "$path"
    failures=$((failures + 1))
  fi
}

printf 'COMMAND: bash /audit-output/evidence/stage1_integrity.sh\n'
printf 'STAGE: launcher-declared mount and record presence\n'
for path in \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/30/rollout-2026-07-30T07-32-39-019fb303-33d0-7701-a917-4f90e9738805.jsonl; do
  check_regular "$path"
done
for path in \
  /candidate \
  /reference/reference-semantics \
  /generation-evidence \
  /generation-evidence/codex-trace; do
  check_directory "$path"
done

printf 'STAGE: exact hashes from audit-input.json\n'
check_sha 053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01 /audit-campaign-lock.json
check_sha fa29d7f413a74f20646e32cd02cb87cdd6766bf4f81745a92db8bcd19d9734d2 /candidate/prompt.py
check_sha fa29d7f413a74f20646e32cd02cb87cdd6766bf4f81745a92db8bcd19d9734d2 /reference/prompt.py
check_sha 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /candidate/py2mpy.py
check_sha 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /reference/py2mpy.py
check_sha b26b53cdaa887f05a2d6d811bfe015acbb1c50154dd70b12d59d9bbbc2e442b0 /reference/canonical.py
check_sha c849d5b57f1feba148f051043efa4a1b8234471f54c9603222436d60e092a610 /generation-evidence/codex-last.txt
check_sha 32c5b42dd79f9602baa32fe48da42403a133cfc35d0f380ec783e6bee405ddcb /generation-evidence/codex-output.log
check_sha b6a26e02e06727577af0efab0b2bd22c3eb20fe397b069271f4eb05184d671cd /generation-evidence/prompt.txt
check_sha 28c3832bd5c5eab8dbc256ea919d4fa39183b8f7cf814822bee318fa237b36a6 /generation-evidence/invocation.json
check_sha 0f7d05799d1b486a31d6052ad63b32e5763835b8194227f3d730bebaa3d3ccef /generation-evidence/metrics.json
check_sha 7587fffb57a4d20862f952f2dde16165d19be53477bbca7c05a4406ada636e3d /generation-evidence/runtime-metrics.json
check_sha 4bc41940bb8c226f358adc93bad87fa4b7969039fe8d4e8306db4fe0ee5ccb24 /generation-evidence/usage.json
check_sha 1cda25299b5927ac1ce27de69aa0d1cd6f6adcd21d777fbb00a5862b900ee496 /run.json
check_sha ad13d7f0c8d7308c9161f9cc0e743de7297562e4c6f2f2ed4ec188962c7a58a5 /task.json
check_sha f39390bfb45fba79426396e61228ebc69b508a16c876ef6986d874c43b2015d3 /generation-result.json
check_sha f2ae765cbc4c7603575f7244b552897fae0c13cdd7d5d2113a6e0432a16353aa \
  /generation-evidence/codex-trace/2026/07/30/rollout-2026-07-30T07-32-39-019fb303-33d0-7701-a917-4f90e9738805.jsonl

printf 'STAGE: campaign lock and declared mode\n'
python3 -c '
import json
with open("/audit-input.json", encoding="utf-8") as f:
    audit_input = json.load(f)
with open("/audit-campaign-lock.json", encoding="utf-8") as f:
    lock = json.load(f)
assert audit_input["audit_campaign"] == lock
assert audit_input["record_layout"] == "pipeline-v3"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit_input["mount_reference_semantics"] is True
assert audit_input["container_paths"]["candidate"] == "/candidate"
assert audit_input["container_paths"]["trusted_prompt"] == "/reference/prompt.py"
assert audit_input["container_paths"]["translator"] == "/reference/py2mpy.py"
print("CAMPAIGN_JSON_EQUAL PASS")
print("RECORD_LAYOUT pipeline-v3")
print("SEMANTICS_MODE SUPPLIED_SEMANTICS")
'
campaign_status=$?
printf 'CAMPAIGN_CHECK_EXIT: %d\n' "$campaign_status"
if [[ "$campaign_status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

printf 'STAGE: candidate/trusted prompt, translator, and supplied semantics\n'
if cmp -s /candidate/prompt.py /reference/prompt.py; then
  printf 'PROMPT_BYTE_IDENTITY PASS\n'
else
  printf 'PROMPT_BYTE_IDENTITY FAIL\n'
  failures=$((failures + 1))
fi
if cmp -s /candidate/py2mpy.py /reference/py2mpy.py; then
  printf 'TRANSLATOR_BYTE_IDENTITY PASS\n'
else
  printf 'TRANSLATOR_BYTE_IDENTITY FAIL\n'
  failures=$((failures + 1))
fi

candidate_semantics_links="$(find /candidate/reference-semantics -type l -print)"
trusted_semantics_links="$(find /reference/reference-semantics -type l -print)"
if [[ -z "$candidate_semantics_links" && -z "$trusted_semantics_links" ]]; then
  printf 'SEMANTICS_SYMLINK_CHECK PASS none\n'
else
  printf 'SEMANTICS_SYMLINK_CHECK FAIL candidate=[%s] trusted=[%s]\n' \
    "$candidate_semantics_links" "$trusted_semantics_links"
  failures=$((failures + 1))
fi
if diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics; then
  printf 'SEMANTICS_RECURSIVE_IDENTITY PASS\n'
else
  printf 'SEMANTICS_RECURSIVE_IDENTITY FAIL\n'
  failures=$((failures + 1))
fi

printf 'STAGE: required candidate proof artifact types\n'
for path in \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/PROOF.md; do
  check_regular "$path"
done

printf 'STAGE: independent bounded tree inventories\n'
printf 'CANDIDATE_COUNTS '
find /candidate -xdev -printf '%y\n' | sort | uniq -c | tr '\n' ' '
printf '\n'
printf 'TRUSTED_SEMANTICS_COUNTS '
find /reference/reference-semantics -xdev -printf '%y\n' | sort | uniq -c | tr '\n' ' '
printf '\n'
printf 'CANDIDATE_SOURCE_SHA256_BEGIN\n'
find /candidate -maxdepth 1 -type f -print0 |
  sort -z |
  xargs -0 sha256sum
printf 'CANDIDATE_SOURCE_SHA256_END\n'
printf 'TRUSTED_SEMANTICS_SHA256_BEGIN\n'
find /reference/reference-semantics -type f -print0 |
  sort -z |
  xargs -0 sha256sum
printf 'TRUSTED_SEMANTICS_SHA256_END\n'

printf 'STAGE: structured trace parse and record inventory\n'
python3 -c '
import collections
import json
from pathlib import Path
path = Path("/generation-evidence/codex-trace/2026/07/30/rollout-2026-07-30T07-32-39-019fb303-33d0-7701-a917-4f90e9738805.jsonl")
outer = collections.Counter()
payload = collections.Counter()
function_calls = collections.Counter()
lines = 0
with path.open(encoding="utf-8") as f:
    for lines, line in enumerate(f, 1):
        obj = json.loads(line)
        outer[obj.get("type")] += 1
        pl = obj.get("payload")
        if isinstance(pl, dict):
            payload[pl.get("type")] += 1
            if pl.get("type") == "function_call":
                function_calls[pl.get("name")] += 1
assert lines == 527
print("TRACE_JSON_PARSE PASS lines=527")
print("TRACE_OUTER_TYPES", sorted(outer.items(), key=lambda item: str(item[0])))
print("TRACE_PAYLOAD_TYPES", sorted(payload.items(), key=lambda item: str(item[0])))
print("TRACE_FUNCTION_CALLS", sorted(function_calls.items(), key=lambda item: str(item[0])))
'
trace_status=$?
printf 'TRACE_PARSE_EXIT: %d\n' "$trace_status"
if [[ "$trace_status" -ne 0 ]]; then
  failures=$((failures + 1))
fi

printf 'OVERALL_FAILURES: %d\n' "$failures"
if [[ "$failures" -eq 0 ]]; then
  printf 'STAGE1_INTEGRITY PASS\n'
  printf 'EXIT_STATUS: 0\n'
  exit 0
fi
printf 'STAGE1_INTEGRITY FAIL\n'
printf 'EXIT_STATUS: 1\n'
exit 1
