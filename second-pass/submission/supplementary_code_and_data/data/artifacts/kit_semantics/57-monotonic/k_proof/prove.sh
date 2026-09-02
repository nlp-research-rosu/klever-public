#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
for corpus_shard in 0 1 2 3 4
do
  python3 generate_k_differential.py \
    --shard-count 5 \
    --shard-index "$corpus_shard" \
    > "k_differential_tests_${corpus_shard}.py"
  python3 py2mpy.py \
    "k_differential_tests_${corpus_shard}.py" \
    > "k_differential_tests_${corpus_shard}.mpy"
done

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
for corpus_shard in 0 1 2 3 4
do
  krun "k_differential_tests_${corpus_shard}.mpy" \
    --definition runtime-kompiled \
    --output none
done
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
then
  echo "UNEXPECTED SUCCESS: false-result mutation"
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation"
fi

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
then
  echo "UNEXPECTED SUCCESS: body mutation"
  exit 1
else
  echo "EXPECTED FAILURE: body mutation"
fi
