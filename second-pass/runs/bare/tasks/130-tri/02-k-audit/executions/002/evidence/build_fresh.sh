#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/130-tri-audit
cd "$audit_work" || exit 2

run_checked() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS=%s\n' "$command_status"
  if [[ "$command_status" -ne 0 ]]; then
    exit "$command_status"
  fi
}

run_checked kompile semantic.k \
  --backend llvm \
  --main-module TRI-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-concrete-kompiled

run_checked kompile verification.k \
  --backend haskell \
  --main-module TRI-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-proof-kompiled

printf '\nFRESH DEFINITIONS\n'
find semantic-concrete-kompiled verification-proof-kompiled \
  -maxdepth 1 -type f -printf '%p %s bytes\n' | sort

