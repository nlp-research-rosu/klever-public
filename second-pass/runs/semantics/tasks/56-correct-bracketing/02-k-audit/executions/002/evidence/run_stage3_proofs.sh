#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

run_log() {
  name="$1"
  shift
  {
    printf 'WORKDIR: %s\n' "$work"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    (
      cd "$work"
      "$@"
    )
    status=$?
    printf 'EXIT_STATUS: %d\n' "$status"
    return "$status"
  } >"$evidence/$name.log" 2>&1
}

run_log stage3_kprove_mutual_loops \
  timeout 300s kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-zero,SPEC.loop-positive \
  --output pretty

run_log stage3_kprove_all \
  timeout 300s kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-zero,SPEC.loop-positive,SPEC.correct-bracketing \
  --output pretty
