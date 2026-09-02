#!/usr/bin/env bash
set -euo pipefail
export PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cd /tmp/audit-work/reconstruction

timeout 600 kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop
echo "INNER_LOOP_TARGET_KPROVE_EXIT=$?"

timeout 600 kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop
echo "INNER_AND_OUTER_TARGETS_KPROVE_EXIT=$?"

timeout 1200 kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC.count-up-to
echo "ALL_NAMED_TARGETS_KPROVE_EXIT=$?"
