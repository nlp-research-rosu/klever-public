#!/usr/bin/env bash
set -uo pipefail

status=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then status=1; fi
}

printf 'Declared layout and mode:\n'
run python3 -c 'import json; d=json.load(open("/audit-input.json")); print(d["record_layout"], d["semantics_mode"], d["problem_id"], d["condition"], sep="\n")'

printf '\nRequired record path types:\n'
run stat -c '%F %n' \
  /audit-input.json /audit-campaign-lock.json /run.json /task.json \
  /generation-result.json /generation-evidence/invocation.json \
  /generation-evidence/metrics.json /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt

run find /generation-evidence/codex-trace -type l -print
run find /generation-evidence/codex-trace -type f -name '*.jsonl' -print

printf '\nCampaign lock must equal audit_campaign and recorded hash:\n'
run python3 -c 'import json; a=json.load(open("/audit-input.json")); b=json.load(open("/audit-campaign-lock.json")); assert a["audit_campaign"] == b'
run python3 -c 'import hashlib,json; a=json.load(open("/audit-input.json")); actual=hashlib.sha256(open("/audit-campaign-lock.json","rb").read()).hexdigest(); print("expected="+a["hashes"]["audit_campaign_lock_sha256"]); print("actual="+actual); assert actual == a["hashes"]["audit_campaign_lock_sha256"]'

printf '\nLauncher-recorded regular-file hashes:\n'
run sha256sum \
  /audit-campaign-lock.json /run.json /task.json /generation-result.json \
  /reference/canonical.py /reference/prompt.py /reference/py2mpy.py \
  /generation-evidence/invocation.json /generation-evidence/metrics.json \
  /generation-evidence/usage.json /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log /generation-evidence/prompt.txt

run bash -c '
  set -e
  python3 -c "import json; d=json.load(open('\''/generation-result.json'\'')); [print(k, v, sep='\''\\t'\'') for k,v in d['\''outputs'\'']['\''evidence'\''].items()]" |
  while IFS=$'\''\t'\'' read -r rel expected; do
    actual=$(sha256sum "/generation-evidence/$rel" | cut -d" " -f1)
    printf "%s expected=%s actual=%s\n" "$rel" "$expected" "$actual"
    test "$actual" = "$expected"
  done
'

printf '\nPrompt/translator/supplied-semantics integrity:\n'
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run find /candidate/reference-semantics /reference/reference-semantics -type l -print
run diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics

printf '\nIndependent per-entry manifests (path, type, size, SHA-256):\n'
run bash -c '
  for root in /candidate/reference-semantics /reference/reference-semantics; do
    printf "ROOT %s\n" "$root"
    find "$root" -mindepth 1 -printf "%P\0" | sort -z |
    while IFS= read -r -d "" rel; do
      path="$root/$rel"
      type=$(stat -c %F "$path")
      size=$(stat -c %s "$path")
      if test -f "$path"; then
        digest=$(sha256sum "$path" | cut -d" " -f1)
      else
        digest=-
      fi
      printf "%s\t%s\t%s\t%s\n" "$rel" "$type" "$size" "$digest"
    done
  done
'

printf '\nStructured trace validation and complete event inventory:\n'
run python3 -c '
import collections, glob, json
paths=glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True)
events=[]
for path in paths:
    with open(path, encoding="utf-8") as src:
        events.extend(json.loads(line) for line in src)
print("valid_json_events="+str(len(events)))
print("top_types="+json.dumps(collections.Counter(e["type"] for e in events), sort_keys=True))
items=[e["payload"] for e in events if e["type"] == "response_item"]
print("response_item_types="+json.dumps(collections.Counter(i["type"] for i in items), sort_keys=True))
for item in items:
    if item["type"] == "function_call":
        print("function_call", item.get("name"), item.get("arguments"), sep="\t")
'

printf '\nGeneration-text records were scanned in full; salient proof claims:\n'
run wc -l -c \
  /generation-evidence/codex-last.txt /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt /generation-evidence/codex-trace/2026/07/23/*.jsonl
run rg -n -e KPROVE_PASSED -e '#Top' -e maximumBody -e 'vsLen\(sortVS' -e RESULT: \
  /generation-evidence/codex-last.txt /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt

exit "$status"
