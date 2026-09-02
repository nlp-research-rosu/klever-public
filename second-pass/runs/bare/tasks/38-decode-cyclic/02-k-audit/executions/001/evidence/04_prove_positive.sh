#!/usr/bin/env bash
set -u

src=/tmp/audit-work/38-decode-cyclic-audit/candidate-src
proof=/tmp/audit-work/38-decode-cyclic-audit/build-proof/verification-kompiled
overall=0

prove_target() {
  description=$1
  logfile=$2
  shift 2
  printf '\nTarget: %s\n$' "$description"
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1 | tee "$logfile"
  status=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ] || ! grep -Fxq '#Top' "$logfile"; then
    printf '[closure check failed: requires exit 0 and an exact #Top line]\n'
    overall=1
  else
    printf '[closure check passed]\n'
  fi
}

printf 'The loop claim is first proved alone.  The complete target then proves both\n'
printf 'claims together because program-correct intentionally uses loop-correct as\n'
printf 'its circularity; selecting program-correct alone removes that dependency.\n'
prove_target loop-correct-alone \
  /audit-output/evidence/04-loop-correct.raw.log \
  kprove "$src/spec.k" \
    --definition "$proof" \
    --spec-module SPEC \
    --claims SPEC.loop-correct

prove_target complete-two-claim-target \
  /audit-output/evidence/04-complete-target.raw.log \
  kprove "$src/spec.k" \
    --definition "$proof" \
    --spec-module SPEC

printf '\nOverall independent-positive-proof status: %d\n' "$overall"
exit "$overall"
