#!/usr/bin/env bash
set -e
set -u
set -o pipefail
PS4='+ ${BASH_SOURCE}:${LINENO}: '
set -x

for source in semantic.k verification.k spec.k; do
  sha256sum "$source"
  nl -ba "$source"
done

printf 'semantic_rule_count='
rg -c '^[[:space:]]*rule([[:space:]]|$)' semantic.k
printf 'verification_rule_count='
rg -c '^[[:space:]]*rule([[:space:]]|$)' verification.k
printf 'spec_claim_count='
rg -c '^[[:space:]]*claim([[:space:]]|$)' spec.k

printf 'attribute_occurrences:\n'
rg -n '\[(function|total|functional|simplification|symbol|priority|owise|concrete)' \
  semantic.k verification.k spec.k || true

printf 'all_local_declaration_starts:\n'
rg -n '^[[:space:]]*(syntax|configuration|rule|claim)([[:space:]]|$)' \
  semantic.k verification.k spec.k
