#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
scratch=/tmp/audit-work/140-fix-spaces
evidence=/audit-output/evidence
overall=0

run_expect() {
  name=$1
  expectation=$2
  shift 2
  log="$evidence/$name.log"
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  "$@" >> "$log" 2>&1
  status=$?
  printf '[exit %d; expected %s]\n' "$status" "$expectation" >> "$log"
  printf '%s exit=%d expected=%s\n' "$name" "$status" "$expectation"
  if [[ "$expectation" == "zero" && "$status" -ne 0 ]]; then
    overall=1
  fi
  if [[ "$expectation" == "nonzero" && "$status" -eq 0 ]]; then
    overall=1
  fi
}

cd "$scratch" || exit 2

run_expect bridge-01-nonspace-fixed-correct zero \
  kprove bridge-witness.k \
    --definition proof-base-kompiled \
    --spec-module BRIDGE-NONSPACE-FIXED-CORRECT

run_expect bridge-02-nonspace-fixed-wrong nonzero \
  kprove bridge-witness.k \
    --definition proof-base-kompiled \
    --spec-module BRIDGE-NONSPACE-FIXED-WRONG

run_expect bridge-03-nonspace-enabled-wrong zero \
  kprove bridge-witness.k \
    --definition proof-loop-kompiled \
    --spec-module BRIDGE-NONSPACE-ENABLED-WRONG

run_expect bridge-04-space-fixed-correct zero \
  kprove bridge-witness.k \
    --definition proof-base-kompiled \
    --spec-module BRIDGE-SPACE-FIXED-CORRECT

run_expect bridge-05-space-fixed-wrong nonzero \
  kprove bridge-witness.k \
    --definition proof-base-kompiled \
    --spec-module BRIDGE-SPACE-FIXED-WRONG

run_expect bridge-06-space-enabled-wrong zero \
  kprove bridge-witness.k \
    --definition proof-loop-kompiled \
    --spec-module BRIDGE-SPACE-ENABLED-WRONG

printf 'overall_exit=%d\n' "$overall"
exit "$overall"
