#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/proof-audit.Dl0nBZ/candidate
export PATH="/home/agent/.nix-profile/bin:$PATH"

run_status() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd "$WORK" || exit 90

printf '## ASCII concrete boundary test after isolated astral parser failure\n'
printf '$ python3 /reference/py2mpy.py concrete-tests-ascii.py > concrete-tests-ascii.mpy\n'
python3 /reference/py2mpy.py concrete-tests-ascii.py > concrete-tests-ascii.mpy
printf '[exit %d]\n' "$?"
run_status krun concrete-tests-ascii.mpy --definition runtime-kompiled

printf '\n## Entry claim modular proof\n'
printf 'The loop claim is marked trusted only in this file after its separate #Top run.\n'
run_status kprove spec-entry-modular.k \
  --definition verification-kompiled \
  --spec-module SPEC-ENTRY-MODULAR
