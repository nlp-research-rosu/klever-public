#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md

printf 'Final marker lines\n'
tail -n 2 "$review"
if [[ "$(tail -n 2 "$review")" != $'VERDICT: CONCERNS\nLEGITIMACY: LEGIT' ]]; then
  printf 'unexpected final markers\n' >&2
  exit 1
fi

printf '\nSeven numbered stage headings\n'
for stage in 1 2 3 4 5 6 7; do
  count=$(rg -c "^## $stage\\." "$review")
  printf 'stage %d heading count: %s\n' "$stage" "$count"
  if [[ "$count" != 1 ]]; then
    exit 1
  fi
done

printf '\nExpected successful evidence statuses\n'
success_logs=(
  01-provenance.log
  01-untrusted-generation-summary.log
  02-translation-identity.log
  02-differential.log
  03-build-semantic-llvm.log
  03-semantic-differential.log
  03-build-verification-core.log
  03-kprove-loop-invariant.log
  03-build-verification.log
  03-kprove-example-one.log
  03-kprove-example-two.log
  03-kprove-example-three.log
  03-kprove-functional-correctness.log
  04-05-static-inventory.log
  04-claim-witnesses.log
  04-body-mutation-build.log
  06-vacuity-dry-run.log
)
for log in "${success_logs[@]}"; do
  tail_line=$(tail -n 1 "/audit-output/evidence/$log")
  printf '%s: %s\n' "$log" "$tail_line"
  if [[ "$tail_line" != "EXIT_STATUS: 0" ]]; then
    exit 1
  fi
done

printf '\nExpected semantic failures\n'
failure_logs=(
  04-body-mutation-kprove.log
  06-vacuity-kprove.log
)
for log in "${failure_logs[@]}"; do
  tail_line=$(tail -n 1 "/audit-output/evidence/$log")
  printf '%s: %s\n' "$log" "$tail_line"
  if [[ "$tail_line" != "EXIT_STATUS: 1" ]]; then
    exit 1
  fi
  if ! rg -q 'WarnStuckClaimState' "/audit-output/evidence/$log"; then
    exit 1
  fi
done

printf '\nRendered semantics boundary\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'unexpected reference semantics\n' >&2
  exit 1
fi
printf 'reference-semantics absent\n'
