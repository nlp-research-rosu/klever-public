#!/usr/bin/env bash
set -u
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
work=/tmp/audit-work/fresh
mutation=/audit-output/evidence/spec-vacuity-audit.k

kprove "$mutation" \
  --definition "$work/verification-kompiled" \
  --spec-module HOW-MANY-TIMES-SPEC-VACUITY-AUDIT \
  --dry-run
dry_rc=$?
echo "MUTATION_DRY_RUN_EXIT=$dry_rc"

kprove "$mutation" \
  --definition "$work/verification-kompiled" \
  --spec-module HOW-MANY-TIMES-SPEC-VACUITY-AUDIT
proof_rc=$?
echo "MUTATION_KPROVE_EXIT=$proof_rc"

if test "$dry_rc" -eq 0 && test "$proof_rc" -ne 0; then
  exit 0
fi
exit 1
