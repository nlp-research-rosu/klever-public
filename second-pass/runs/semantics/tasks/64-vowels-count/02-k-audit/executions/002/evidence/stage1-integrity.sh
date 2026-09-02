#!/usr/bin/env bash
set -u

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
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /candidate/prompt.py
  /candidate/py2mpy.py
)

failed=0
printf 'REQUIRED ARTIFACT TYPES AND READABILITY\n'
for path in "${required[@]}"; do
  if [[ ! -e $path ]]; then
    printf 'MISSING %s\n' "$path"
    failed=1
  elif [[ -L $path ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
    failed=1
  elif [[ ! -f $path || ! -r $path ]]; then
    printf 'BAD_TYPE_OR_UNREADABLE %s\n' "$path"
    failed=1
  else
    stat -c 'OK %F mode=%a size=%s %n' "$path"
  fi
done

printf '\nRECORDED FILE HASHES RECOMPUTED FROM MOUNTS\n'
sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/23/*.jsonl

printf '\nCANDIDATE PROMPT AND TRANSLATOR BYTE COMPARISONS\n'
cmp -s /candidate/prompt.py /reference/prompt.py
printf 'prompt_cmp_exit=%d\n' "$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'translator_cmp_exit=%d\n' "$?"

printf '\nSUPPLIED SEMANTICS TYPE CHECK\n'
for root in /reference/reference-semantics /candidate/reference-semantics; do
  if [[ ! -d $root || -L $root ]]; then
    printf 'BAD_SEMANTICS_ROOT %s\n' "$root"
    failed=1
  fi
  while IFS= read -r -d '' path; do
    if [[ -L $path ]]; then
      printf 'SYMLINKED_SEMANTICS_ENTRY %s -> %s\n' "$path" "$(readlink "$path")"
      failed=1
    elif [[ ! -d $path && ! -f $path ]]; then
      printf 'MISTYPED_SEMANTICS_ENTRY %s\n' "$path"
      failed=1
    fi
  done < <(find "$root" -mindepth 1 -print0)
done

printf '\nSUPPLIED SEMANTICS RECURSIVE COMPARISON\n'
diff --recursive --no-dereference --brief \
  /reference/reference-semantics /candidate/reference-semantics
semantics_diff_status=$?
printf 'semantics_diff_exit=%d\n' "$semantics_diff_status"
if (( semantics_diff_status != 0 )); then
  failed=1
fi

printf '\nINDEPENDENT TREE MANIFESTS\n'
for root in /candidate /reference/reference-semantics; do
  label=${root#/}
  label=${label//\//_}
  manifest="/tmp/audit-work/${label}.tree-manifest"
  (
    cd "$root" || exit
    find . -mindepth 1 -printf '%y %m %p -> %l\n' | LC_ALL=C sort
    find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
  ) > "$manifest"
  printf '%s  %s\n' "$(sha256sum "$manifest" | cut -d' ' -f1)" "$root"
done

printf '\nCAMPAIGN BLOCK STRUCTURAL EQUALITY\n'
python3 - <<'PY'
import json

with open("/audit-input.json", encoding="utf-8") as f:
    audit_input = json.load(f)
with open("/audit-campaign-lock.json", encoding="utf-8") as f:
    lock = json.load(f)
print("campaign_blocks_equal=" + str(audit_input["audit_campaign"] == lock).lower())
raise SystemExit(0 if audit_input["audit_campaign"] == lock else 1)
PY
campaign_status=$?
printf 'campaign_comparison_exit=%d\n' "$campaign_status"
if (( campaign_status != 0 )); then
  failed=1
fi

printf '\nJSON READABILITY\n'
for path in "${required[@]:0:11}"; do
  if [[ $path == *.json ]]; then
    python3 -m json.tool "$path" >/dev/null
    printf 'json_parse_exit=%d %s\n' "$?" "$path"
  fi
done

exit "$failed"
