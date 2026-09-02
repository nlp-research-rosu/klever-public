#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n\n' "$rc"
  return 0
}

check_sha() {
  local expected="$1"
  local path="$2"
  local actual
  printf '$ sha256sum %q\n' "$path"
  actual="$(sha256sum "$path" | awk '{print $1}')"
  printf '%s  %s\n' "$actual" "$path"
  if [[ "$actual" == "$expected" ]]; then
    printf 'MATCH expected=%s\n[exit 0]\n\n' "$expected"
  else
    printf 'MISMATCH expected=%s\n[exit 1]\n\n' "$expected"
  fi
}

printf '## Required mounts and records\n'
required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/usage.json
  /generation-evidence/codex-trace
  /candidate
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
)
for path in "${required[@]}"; do
  if [[ -r "$path" ]]; then
    printf 'READABLE %s\n' "$path"
  else
    printf 'MISSING_OR_UNREADABLE %s\n' "$path"
  fi
done
printf '\n'

printf '## Symlink scan of provenance and proof mounts\n'
run find /candidate /reference /generation-evidence -type l -printf '%p -> %l\n'

printf '## Campaign lock equality\n'
run python3 -c 'import json,sys; a=json.load(open("/audit-input.json")); b=json.load(open("/audit-campaign-lock.json")); print("MATCH" if a["audit_campaign"] == b else "MISMATCH"); sys.exit(0 if a["audit_campaign"] == b else 1)'

printf '## Launcher-recorded single-file hashes\n'
check_sha ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745 /audit-campaign-lock.json
check_sha 321818dc4f5c9795e25ea800ab12c1b1e5cf0bcc70b308443b9f08339a122db0 /run.json
check_sha fa6603a1fb6153b5f7f353000278bf21677c39d3da358c086680e0b63c2c67f6 /task.json
check_sha 9b8fe4085060d981dfb8e3de99260fa029ae3b08ad5c568dbbcccc378ab39e5b /generation-result.json
check_sha 8435fca255dfd78df63727cf0256b7c4d98d3a8a8f307a99f59943453a5ae2bd /generation-evidence/invocation.json
check_sha 535c646727d8f05b1f0fe2e6eb7a4793770af02237714114cca983b36322a2f9 /generation-evidence/metrics.json
check_sha 6ef4c67df66147f77ddbf9889a7bd14451553265273a371ba0de25529ce2be86 /generation-evidence/codex-last.txt
check_sha f27ba9692c0000d47e4a59a73ca346e95b18f0f18f4023753cbd890a93192cea /generation-evidence/codex-output.log
check_sha 3ccfe05a1e1620ec7e34cf354de6eeb973da0fe27a12a04f4ac62b0a78eeec09 /generation-evidence/prompt.txt
check_sha 940d44926efe249b39d0adec3cc7716f8979c306edbc537ae344608385c0d2d9 /generation-evidence/usage.json
check_sha 6abcbf35f335983494a8082c549aa68ad05845ecd65ff051850129bf1d2cd4f7 /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T00-51-43-019f8d87-a172-7f52-8300-3fbac7774c34.jsonl
check_sha 4c9f9c06eddb1f9fbca571269b1808728446c320e95a419f040afc4de00b4d9b /reference/canonical.py
check_sha 864d47767142cb4e635dfefba79f1d7ce448f7cb99dac09c2695a5c96619994e /reference/prompt.py
check_sha 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /reference/py2mpy.py

printf '## Candidate prompt and translator byte equality\n'
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py

printf '## Supplied-semantics recursive type/name/content equality\n'
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
run bash -c 'cd /candidate/reference-semantics && find . -printf "%y %P\n" | LC_ALL=C sort'
run bash -c 'cd /reference/reference-semantics && find . -printf "%y %P\n" | LC_ALL=C sort'

printf '## Independent mounted-input manifests\n'
run bash -c 'find /candidate -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum'
run bash -c 'find /reference -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum'
run bash -c 'find /generation-evidence -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum'
