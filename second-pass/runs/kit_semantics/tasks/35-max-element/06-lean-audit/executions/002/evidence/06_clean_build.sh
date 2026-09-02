#!/usr/bin/env bash
set -euo pipefail
set -x

audit_project=/tmp/audit-work/35-max-element-proof-audit
test ! -e "$audit_project"
mkdir -p "$audit_project/Base"
cp /candidate/Proof.lean /candidate/lakefile.lean /candidate/lean-toolchain "$audit_project/"
cp -a /reference/klean-generation/generated/. "$audit_project/Base/"

find "$audit_project" -type l -o -type p -o -type s -o -type b -o -type c
sha256sum \
  /candidate/Proof.lean \
  "$audit_project/Proof.lean" \
  /reference/klean-generation/generated/Klean35MaxElement/Lemmas.lean \
  "$audit_project/Base/Klean35MaxElement/Lemmas.lean"

if rg -n '\b(sorry|admit|unsafe|axiom|opaque)\b' \
    "$audit_project/Proof.lean" "$audit_project/lakefile.lean"; then
  exit 1
else
  test "$?" -eq 1
fi

if rg -n '^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b' \
    "$audit_project/Proof.lean" "$audit_project/lakefile.lean"; then
  exit 1
else
  test "$?" -eq 1
fi

cd "$audit_project"
export LD_PRELOAD=/tmp/audit-work/proc_pid_shim.so
lake clean
lake build
