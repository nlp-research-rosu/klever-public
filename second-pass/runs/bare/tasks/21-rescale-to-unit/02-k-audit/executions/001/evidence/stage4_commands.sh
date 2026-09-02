#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

definition=/tmp/audit-work/build/verification-kompiled

run kast /tmp/audit-work/source/solution.mpy \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Program \
  --output kore \
  --output-file /tmp/audit-work/generated/submitted-program.kore
run kast /audit-output/evidence/solution-program-expanded.mpy \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Program \
  --output kore \
  --output-file /tmp/audit-work/generated/expanded-proof-program.kore
run cmp -s \
  /tmp/audit-work/generated/submitted-program.kore \
  /tmp/audit-work/generated/expanded-proof-program.kore
run sha256sum \
  /tmp/audit-work/generated/submitted-program.kore \
  /tmp/audit-work/generated/expanded-proof-program.kore
run python3 /audit-output/evidence/claim_witnesses.py
