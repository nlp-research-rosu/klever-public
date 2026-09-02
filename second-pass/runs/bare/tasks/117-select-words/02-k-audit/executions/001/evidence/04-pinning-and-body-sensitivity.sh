#!/usr/bin/env bash
set -u
set -x

cd /tmp/audit-work/fresh || exit 90
python3 /audit-output/evidence/04-pinning-check.py
pinning_exit=$?

python3 -c 'print("original witness", __import__("solution").select_words("u", 0)); print("mutated witness", [w for w in "u".split() if len([c for c in w if c.lower() not in "aeio"]) == 0])'
witness_exit=$?

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
body_mutation_exit=$?

echo "pinning_exit=$pinning_exit"
echo "witness_exit=$witness_exit"
echo "body_mutation_exit=$body_mutation_exit"

test "$pinning_exit" -eq 0
pinning_assert_exit=$?
test "$witness_exit" -eq 0
witness_assert_exit=$?
test "$body_mutation_exit" -ne 0
mutation_assert_exit=$?

echo "pinning_assert_exit=$pinning_assert_exit"
echo "witness_assert_exit=$witness_assert_exit"
echo "mutation_assert_exit=$mutation_assert_exit"
test "$pinning_assert_exit" -eq 0 \
  -a "$witness_assert_exit" -eq 0 \
  -a "$mutation_assert_exit" -eq 0
