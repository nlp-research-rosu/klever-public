#!/usr/bin/env bash
set -u -o pipefail

root=/tmp/audit-work/58-common-audit
candidate="$root/candidate"
overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run kompile --version || overall=1
run kprove --version || overall=1
run python3 /audit-output/evidence/pinning_check.py || overall=1

# Fresh concrete definition: no candidate cache or compiled directory is copied.
run kompile --backend llvm "$candidate/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition "$root/semantic-kompiled-audit" || overall=1

run python3 /audit-output/evidence/concrete_compare.py || overall=1

# Fresh proof definition from source.
run kompile --backend haskell "$candidate/verification.k" \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition "$root/verification-kompiled-audit" || overall=1

# The candidate has exactly one positive target claim.
run kprove "$candidate/spec.k" \
  --definition "$root/verification-kompiled-audit" \
  --spec-module SPEC || overall=1

printf '\nOVERALL_EXIT=%d\n' "$overall"
exit "$overall"
