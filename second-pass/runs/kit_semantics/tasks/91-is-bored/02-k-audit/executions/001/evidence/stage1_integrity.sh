#!/usr/bin/env bash
set -uo pipefail

status=0

check_hash() {
  local expected=$1
  local path=$2
  local actual
  actual=$(sha256sum "$path" | cut -d' ' -f1)
  printf 'HASH %s\n  expected=%s\n  actual=%s\n' "$path" "$expected" "$actual"
  if [[ "$actual" != "$expected" ]]; then
    printf '  RESULT=MISMATCH\n'
    status=1
  else
    printf '  RESULT=MATCH\n'
  fi
}

printf 'COMMAND: bash /audit-output/evidence/stage1_integrity.sh\n'
printf 'DATE_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

check_hash 053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01 /audit-campaign-lock.json
check_hash 548c1003a1ff2d2e435391d406ab52ba679e918888a979f82517f372f920c9b4 /reference/canonical.py
check_hash 9445e82177f062459a801e24909bc856435701d82f1d67a9dad1f9d6fd0f6362 /reference/prompt.py
check_hash 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /reference/py2mpy.py
check_hash 9445e82177f062459a801e24909bc856435701d82f1d67a9dad1f9d6fd0f6362 /candidate/prompt.py
check_hash 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /candidate/py2mpy.py
check_hash 16643b569eb6598c207c772df6ffda2bf619e446fe788464717ff54361b53e22 /run.json
check_hash d31d47b813adda4e39076c657d582142e54cc4bfb87db7f27d664c3254f449cd /task.json
check_hash 09f3dc6664af8dede81c13ffd63a636e8b2e625e78a68b14ce5cadcd6919c42f /generation-result.json
check_hash 3b5a72978c45e267223c09e05a1cb379f04c63e75839ca2ad331b7240e2ea34e /generation-evidence/invocation.json
check_hash a2ac8b1e7fa1412bae547ab2f5b4236a520a0baa7c0ecd070311794acb25b083 /generation-evidence/metrics.json
check_hash 2d40eb5ae891ba8071fd2b27d645fdbde3c0fa05a4338e83a069ab9310551f1d /generation-evidence/runtime-metrics.json
check_hash 0b541e5970bcb06f0b5a44ec9c00a2746fed26ae992150fae8300b01ef955dbb /generation-evidence/usage.json
check_hash b7c3da914fa7037301f29cfb01b47d4d90c84f606939361432a98bd51aa8a277 /generation-evidence/codex-last.txt
check_hash 646f9e1b9d5f1251cd193e0f359df5f7b526b54d2f0f490dc373548df1a10666 /generation-evidence/codex-output.log
check_hash b6a26e02e06727577af0efab0b2bd22c3eb20fe397b069271f4eb05184d671cd /generation-evidence/prompt.txt
check_hash 1b6245e2e36def99d74c0dd5931f9243d37b31ecc4cc3e25ac1f76a8532b27b6 /generation-evidence/codex-trace/2026/07/30/rollout-2026-07-30T08-01-04-019fb31d-3a31-7290-995c-21abd2384d5b.jsonl

printf '\nCAMPAIGN_LOCK_BYTE_COMPARISON:\n'
python3 - <<'PY'
import json
with open('/audit-input.json', encoding='utf-8') as f:
    audit = json.load(f)['audit_campaign']
with open('/audit-campaign-lock.json', encoding='utf-8') as f:
    lock = json.load(f)
print('JSON_EQUAL=' + str(audit == lock))
raise SystemExit(0 if audit == lock else 1)
PY
campaign_ec=$?
if [[ $campaign_ec -ne 0 ]]; then status=1; fi

printf '\nBYTE_IDENTITY:\n'
for pair in \
  '/candidate/prompt.py /reference/prompt.py' \
  '/candidate/py2mpy.py /reference/py2mpy.py'
do
  set -- $pair
  if cmp -s "$1" "$2"; then
    printf 'MATCH %s %s\n' "$1" "$2"
  else
    printf 'MISMATCH %s %s\n' "$1" "$2"
    status=1
  fi
done

printf '\nSEMANTICS_RECURSIVE_DIFF:\n'
if diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics; then
  printf 'RESULT=IDENTICAL\n'
else
  printf 'RESULT=MISMATCH\n'
  status=1
fi

printf '\nNON_REGULAR_OR_SYMLINKED_ENTRIES:\n'
bad_entries=$(find /reference/reference-semantics /candidate/reference-semantics \
  \( -type l -o \( ! -type d ! -type f \) \) -print)
if [[ -n "$bad_entries" ]]; then
  printf '%s\n' "$bad_entries"
  status=1
else
  printf 'NONE\n'
fi

printf '\nSEMANTICS_FILE_MANIFEST:\n'
(
  cd /reference/reference-semantics
  find . -type f -print0 | sort -z | while IFS= read -r -d '' file; do
    sha256sum "$file"
  done
)

printf '\nREQUIRED_RECORD_READABILITY:\n'
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
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
  /candidate
)
for path in "${required[@]}"; do
  if [[ -r "$path" ]]; then
    printf 'READABLE %s\n' "$path"
  else
    printf 'MISSING_OR_UNREADABLE %s\n' "$path"
    status=1
  fi
done

printf '\nREQUIRED_MOUNT_ENTRY_TYPES:\n'
find /candidate /reference/reference-semantics /generation-evidence/codex-trace \
  -printf '%y %p -> %l\n' | sort

printf '\nFINAL_STATUS=%d\n' "$status"
exit "$status"
