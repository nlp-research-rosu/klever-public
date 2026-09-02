#!/usr/bin/env bash
set -uo pipefail
set -x

cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean-app-path-shim.so \
  /audit-output/evidence/lean-app-path-shim.c
export LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so
export PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH

audit_stage5_dir="$(mktemp -d /tmp/audit-work/stage5-audit.XXXXXX)"
cp -a /candidate/. "$audit_stage5_dir/"
cp -a /reference/klean-generation/generated/. "$audit_stage5_dir/Base/"
cp /audit-output/evidence/ProofAxioms.lean "$audit_stage5_dir/ProofAxioms.lean"

printf '%s\n' "$audit_stage5_dir"
find "$audit_stage5_dir" -maxdepth 2 -type f -printf '%P\n' | sort
cd "$audit_stage5_dir"
lake clean
lake build
lake env lean ProofAxioms.lean
