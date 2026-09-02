#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/55-fib-independent-audit
evidence=/audit-output/evidence
cd "$scratch"

printf '%s\n' 'COMMAND: kprove context-spec.k --definition verification-proof-kompiled --spec-module CONTEXT-SPEC --dry-run --output none'
kprove context-spec.k \
  --definition verification-proof-kompiled \
  --spec-module CONTEXT-SPEC \
  --dry-run \
  --output none \
  2>&1 | tee "$evidence/05_context_dry_run.log"
printf 'EXIT_STATUS context_dry_run=0\n'

printf '%s\n' 'COMMAND: kprove context-spec.k --definition verification-proof-kompiled --spec-module CONTEXT-SPEC --output pretty'
kprove context-spec.k \
  --definition verification-proof-kompiled \
  --spec-module CONTEXT-SPEC \
  --output pretty \
  2>&1 | tee "$evidence/05_context_proof.log"
grep -qx '#Top' "$evidence/05_context_proof.log"
printf 'EXIT_STATUS context_proof=0 SIGNAL=#Top\n'

printf '%s\n' 'COMMAND: python3 py2mpy.py mutated-solution.py > mutated-solution.mpy'
python3 py2mpy.py mutated-solution.py > mutated-solution.mpy
printf 'EXIT_STATUS mutated_translation=0\n'

printf '%s\n' 'COMMAND: kast mutated-solution.mpy --definition verification-proof-kompiled --sort Program --output json'
kast mutated-solution.mpy \
  --definition verification-proof-kompiled \
  --sort Program \
  --output json > mutated-program-kast.json
printf 'EXIT_STATUS mutated_kast=0\n'

printf '%s\n' 'COMMAND: kprove body-mutation-spec.k --definition verification-proof-kompiled --spec-module BODY-MUTATION-SPEC --dry-run --emit-json-spec body-mutation-spec-kast.json --output none'
kprove body-mutation-spec.k \
  --definition verification-proof-kompiled \
  --spec-module BODY-MUTATION-SPEC \
  --dry-run \
  --emit-json-spec body-mutation-spec-kast.json \
  --output none \
  2>&1 | tee "$evidence/05_body_mutation_dry_run.log"
printf 'EXIT_STATUS body_mutation_dry_run=0\n'

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/05_body_mutation_compare.py'
python3 /audit-output/evidence/05_body_mutation_compare.py
printf 'EXIT_STATUS body_constructor_compare=0\n'

printf '%s\n' 'COMMAND: kprove body-mutation-spec.k --definition verification-proof-kompiled --spec-module BODY-MUTATION-SPEC --output pretty'
set +e
kprove body-mutation-spec.k \
  --definition verification-proof-kompiled \
  --spec-module BODY-MUTATION-SPEC \
  --output pretty \
  > "$evidence/05_body_mutation_proof.log" 2>&1
mutation_status=$?
set -e
sed -n '1,180p' "$evidence/05_body_mutation_proof.log"
printf 'EXIT_STATUS body_mutation_proof=%s EXPECTED_NONZERO=true\n' "$mutation_status"
test "$mutation_status" -ne 0
grep -q 'WarnStuckClaimState' "$evidence/05_body_mutation_proof.log"
