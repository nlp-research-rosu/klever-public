#!/usr/bin/env bash
set -u
set -o pipefail
set -x

sources=(
  /tmp/audit-work/semantic.k
  /tmp/audit-work/verification.k
  /tmp/audit-work/spec.k
  /tmp/audit-work/concrete-spec.k
)

for source in "${sources[@]}"; do
  printf '\nSOURCE=%s\n' "$source"
  sha256sum "$source"
  rg -n '^[[:space:]]*(syntax|configuration|rule|claim|requires|ensures)' "$source" || true
  printf 'rule_count=%s claim_count=%s syntax_line_count=%s\n' \
    "$(rg -c '^[[:space:]]*rule' "$source" || printf 0)" \
    "$(rg -c '^[[:space:]]*claim' "$source" || printf 0)" \
    "$(rg -c '^[[:space:]]*syntax' "$source" || printf 0)"
done

printf '\nSPECIAL_ATTRIBUTES\n'
rg -n '\[(function|total|functional|simplification|priority|macro|anywhere|opaque|concrete)(\(|,|\])' \
  "${sources[@]}" || true

printf '\nPROGRAM_CONSTRUCTORS\n'
rg -o \
  'Module|FuncDef|Params|Assign|Name|Int|Bool|While|If|Return|Compare|CmpOp|BinOp' \
  /tmp/audit-work/solution.mpy | sort | uniq -c

printf 'NO_GENERATED_HELPER_K_FILES_OUTSIDE_LIST=%s\n' \
  "$(find -P /tmp/audit-work -maxdepth 1 -type f -name '*.k' \
      ! -name semantic.k ! -name verification.k ! -name spec.k \
      ! -name concrete-spec.k -printf '%f\n' | wc -l)"
printf 'SCRIPT_EXIT=0\n'
