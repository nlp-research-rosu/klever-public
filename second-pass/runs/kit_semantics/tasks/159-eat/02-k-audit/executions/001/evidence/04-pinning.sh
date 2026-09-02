#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/159-eat

python3 /audit-output/evidence/pinning_check.py
pinning_status=$?
echo "constructor_pinning_exit=${pinning_status}"

cp /audit-output/evidence/04-body-mutation.k audit-body-mutation.k
copy_status=$?
echo "body_mutation_copy_exit=${copy_status}"

kprove audit-body-mutation.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-BODY-MUTATION
body_mutation_status=$?
echo "body_mutation_kprove_exit=${body_mutation_status}"

if (( pinning_status != 0 || copy_status != 0 )); then
  exit 1
fi

# The mutation must parse/build and reach a stuck result obligation.
if (( body_mutation_status == 0 )); then
  exit 1
fi

exit 0
