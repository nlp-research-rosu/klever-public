#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction
sha256sum semantic.k verification.k spec.k solution.mpy
printf 'semantic_rule_count='
rg -c '^[[:space:]]*rule([[:space:]]|$)' semantic.k
printf 'verification_rule_count='
rg -c '^[[:space:]]*rule([[:space:]]|$)' verification.k
printf 'spec_claim_count='
rg -c '^[[:space:]]*claim([[:space:]]|$)' spec.k
rg -n 'syntax|configuration|rule|claim|function|functional|total|opaque|priority|simplification|owise' \
  semantic.k verification.k spec.k
printf '%s\n' 'solution_constructor_inventory:'
rg -o '[A-Z][A-Za-z]*\(' solution.mpy | sort -u
printf '%s\n' 'semantic.k:'
nl -ba semantic.k
printf '%s\n' 'verification.k:'
nl -ba verification.k
printf '%s\n' 'spec.k:'
nl -ba spec.k
