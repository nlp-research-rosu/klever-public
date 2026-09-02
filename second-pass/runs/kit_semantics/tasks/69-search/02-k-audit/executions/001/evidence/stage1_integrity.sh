#!/usr/bin/env bash
set -uo pipefail
set -x

required_files=(
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
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /candidate/prompt.py
  /candidate/py2mpy.py
)

status=0
for path in "${required_files[@]}"; do
  if [[ ! -f "$path" || ! -r "$path" || -L "$path" ]]; then
    printf 'BAD_REQUIRED_FILE %s\n' "$path"
    status=1
  fi
done

trace_count="$(find /generation-evidence/codex-trace -type f -name '*.jsonl' | wc -l)"
printf 'trace_file_count=%s\n' "$trace_count"
if [[ "$trace_count" != 1 ]]; then
  status=1
fi
if find /candidate /reference /generation-evidence -type l -print -quit | grep -q .; then
  printf '%s\n' 'SYMLINK_FOUND'
  find /candidate /reference /generation-evidence -type l -printf '%p -> %l\n'
  status=1
else
  printf '%s\n' 'no_symlinks_in_declared_mounts'
fi

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
  /generation-evidence/codex-trace/2026/07/29/rollout-2026-07-29T09-44-19-019fae55-62af-7462-8e3f-80f8dd36c52f.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

python3 -c 'import json; a=json.load(open("/audit-input.json")); b=json.load(open("/audit-campaign-lock.json")); assert a["audit_campaign"] == b; print("campaign_block_equal=true")'
campaign_compare=$?
printf 'campaign_block_compare_exit=%s\n' "$campaign_compare"
if [[ "$campaign_compare" != 0 ]]; then
  status=1
fi

cmp -s /candidate/prompt.py /reference/prompt.py
prompt_compare=$?
printf 'prompt_cmp_exit=%s\n' "$prompt_compare"
if [[ "$prompt_compare" != 0 ]]; then
  status=1
fi

cmp -s /candidate/py2mpy.py /reference/py2mpy.py
translator_compare=$?
printf 'translator_cmp_exit=%s\n' "$translator_compare"
if [[ "$translator_compare" != 0 ]]; then
  status=1
fi

diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
semantics_compare=$?
printf 'semantics_recursive_diff_exit=%s\n' "$semantics_compare"
if [[ "$semantics_compare" != 0 ]]; then
  status=1
fi

comm -3 \
  <(cd /candidate/reference-semantics && find . -printf '%y %p\n' | sort) \
  <(cd /reference/reference-semantics && find . -printf '%y %p\n' | sort)
type_compare=$?
printf 'semantics_type_inventory_exit=%s\n' "$type_compare"
if [[ "$type_compare" != 0 ]]; then
  status=1
fi

printf '%s\n' 'reference_semantics_manifest_begin'
(
  cd /reference/reference-semantics
  find . -type f -print0 |
    sort -z |
    xargs -0 sha256sum
)
printf '%s\n' 'reference_semantics_manifest_end'

for tree in /candidate /reference/reference-semantics /generation-evidence/codex-trace; do
  printf 'independent_tree_manifest_sha256 tree=%s ' "$tree"
  (
    cd "$tree"
    find . -type f -print0 |
      sort -z |
      xargs -0 sha256sum |
      sha256sum
  )
done

python3 -c 'import json,collections,glob; p=glob.glob("/generation-evidence/codex-trace/**/*.jsonl",recursive=True)[0]; rows=[json.loads(x) for x in open(p)]; print("trace_lines="+str(len(rows))); print("trace_top_types="+repr(dict(collections.Counter(r.get("type") for r in rows)))); print("trace_payload_types="+repr(dict(collections.Counter(r.get("payload",{}).get("type") for r in rows))))'
trace_parse=$?
printf 'trace_parse_exit=%s\n' "$trace_parse"
if [[ "$trace_parse" != 0 ]]; then
  status=1
fi

printf 'stage1_integrity_exit=%s\n' "$status"
exit "$status"
