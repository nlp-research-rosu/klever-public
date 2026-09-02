#!/usr/bin/env bash
set -u

log=/audit-output/evidence/00_environment.log
exec > >(tee "$log") 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf 'rendered_semantics_mode=SUPPLIED_SEMANTICS\n'
run test -d /reference/reference-semantics
run test -f /reference/reference-semantics/semantics.k
run command -v kompile
run kompile --version
run command -v kprove
run kprove --version
run command -v krun
run krun --version
run python3 --version
