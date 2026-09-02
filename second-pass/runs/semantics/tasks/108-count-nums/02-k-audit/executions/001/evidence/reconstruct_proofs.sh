#!/usr/bin/env bash
set -euo pipefail

runner=/audit-output/evidence/run-command.sh
source_dir=/tmp/audit-work/audit-108/source
build_root=/tmp/audit-work/audit-108/build-proof

cd "$source_dir"

"$runner" /audit-output/evidence/build_loop_base.log \
  kompile verification.k \
  --backend haskell \
  --main-module COUNT-NUMS-VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/loop-base-kompiled"

"$runner" /audit-output/evidence/prove_positive_loop.log \
  kprove spec.k \
  --definition "$build_root/loop-base-kompiled" \
  --spec-module POSITIVE-LOOP-SPEC

"$runner" /audit-output/evidence/prove_negative_loop.log \
  kprove spec.k \
  --definition "$build_root/loop-base-kompiled" \
  --spec-module NEGATIVE-LOOP-SPEC

"$runner" /audit-output/evidence/build_digit_loop.log \
  kompile verification.k \
  --backend haskell \
  --main-module DIGIT-LOOP-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/digit-loop-kompiled"

"$runner" /audit-output/evidence/prove_positive_function.log \
  kprove spec.k \
  --definition "$build_root/digit-loop-kompiled" \
  --spec-module POSITIVE-FUNCTION-SPEC

"$runner" /audit-output/evidence/prove_negative_function.log \
  kprove spec.k \
  --definition "$build_root/digit-loop-kompiled" \
  --spec-module NEGATIVE-FUNCTION-SPEC

"$runner" /audit-output/evidence/build_digit_function.log \
  kompile verification.k \
  --backend haskell \
  --main-module DIGIT-FUNCTION-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/digit-function-kompiled"

"$runner" /audit-output/evidence/prove_signed_function.log \
  kprove spec.k \
  --definition "$build_root/digit-function-kompiled" \
  --spec-module SIGNED-FUNCTION-SPEC

"$runner" /audit-output/evidence/build_signed_digit.log \
  kompile verification.k \
  --backend haskell \
  --main-module SIGNED-DIGIT-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/signed-digit-kompiled"

"$runner" /audit-output/evidence/prove_count_loop_with_n.log \
  kprove spec.k \
  --definition "$build_root/signed-digit-kompiled" \
  --spec-module COUNT-LOOP-WITH-N-SPEC

"$runner" /audit-output/evidence/build_count_loop_with_n.log \
  kompile verification.k \
  --backend haskell \
  --main-module COUNT-LOOP-WITH-N-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/count-loop-with-n-kompiled"

"$runner" /audit-output/evidence/prove_count_loop.log \
  kprove spec.k \
  --definition "$build_root/count-loop-with-n-kompiled" \
  --spec-module COUNT-LOOP-SPEC

"$runner" /audit-output/evidence/build_count_loop.log \
  kompile verification.k \
  --backend haskell \
  --main-module COUNT-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition "$build_root/count-loop-kompiled"

"$runner" /audit-output/evidence/prove_count_nums.log \
  kprove spec.k \
  --definition "$build_root/count-loop-kompiled" \
  --spec-module COUNT-NUMS-SPEC
