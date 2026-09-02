#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/55-fib-independent-audit
cd "$scratch"

printf '%s\n' 'COMMAND: kast regenerated-solution.mpy --definition verification-proof-kompiled --sort Program --output json'
kast regenerated-solution.mpy \
  --definition verification-proof-kompiled \
  --sort Program \
  --output json > program-kast.json
printf 'EXIT_STATUS kast=0\n'

printf '%s\n' 'COMMAND: kprove spec.k --definition verification-proof-kompiled --spec-module SPEC --dry-run --emit-json-spec fresh-spec-kast.json --output none'
kprove spec.k \
  --definition verification-proof-kompiled \
  --spec-module SPEC \
  --dry-run \
  --emit-json-spec fresh-spec-kast.json \
  --output none
printf 'EXIT_STATUS spec_dry_run=0\n'

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/04_constructor_pinning.py'
python3 /audit-output/evidence/04_constructor_pinning.py
printf 'EXIT_STATUS constructor_compare=0\n'
