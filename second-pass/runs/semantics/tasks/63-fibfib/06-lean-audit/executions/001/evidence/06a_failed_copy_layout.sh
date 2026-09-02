#!/usr/bin/env bash
set -uo pipefail

audit_dir=/tmp/audit-work/63-fibfib-stage5-audit
shim=/tmp/audit-work/toolchain_path_shim.so

printf 'audit_dir=%s\n' "$audit_dir"
printf 'shim=%s\n' "$shim"
if test -e "$audit_dir"; then
  printf '%s\n' "refusing non-fresh audit directory: $audit_dir" >&2
  exit 90
fi
mkdir "$audit_dir"
cp -a /candidate/. "$audit_dir/"
cp -a /reference/klean-generation/generated "$audit_dir/Base"

printf '%s\n' '--- copied source layout before clean/build ---'
find "$audit_dir" -maxdepth 4 -type f -print | sort
printf '%s\n' '--- target source hashes before clean/build ---'
sha256sum \
  /reference/klean-generation/generated/Klean63Fibfib/Lemmas.lean \
  "$audit_dir/Base/Klean63Fibfib/Lemmas.lean"
printf '%s\n' '--- forbidden candidate token scan (empty is required) ---'
rg -n '\b(sorry|admit|unsafe|axiom|opaque)\b' \
  "$audit_dir/Proof.lean" \
  "$audit_dir/lakefile.lean" \
  "$audit_dir/lean-toolchain" || true
printf '%s\n' '--- target declaration/shadow scan ---'
rg -n 'targetStatement|^\s*(def|theorem|axiom|opaque)\b' \
  "$audit_dir/Proof.lean" \
  "$audit_dir/lakefile.lean"

cd "$audit_dir"
printf '%s\n' '--- command: lake clean ---'
LD_PRELOAD="$shim" lake clean 2>&1
clean_status=$?
printf 'lake_clean_exit=%s\n' "$clean_status"

printf '%s\n' '--- command: lake build ---'
LD_PRELOAD="$shim" lake build 2>&1
build_status=$?
printf 'lake_build_exit=%s\n' "$build_status"

printf '%s\n' '--- target source hashes after clean/build ---'
sha256sum \
  /reference/klean-generation/generated/Klean63Fibfib/Lemmas.lean \
  "$audit_dir/Base/Klean63Fibfib/Lemmas.lean"
printf '%s\n' '--- candidate Proof.lean after clean/build ---'
nl -ba "$audit_dir/Proof.lean"

test "$clean_status" -eq 0 -a "$build_status" -eq 0
