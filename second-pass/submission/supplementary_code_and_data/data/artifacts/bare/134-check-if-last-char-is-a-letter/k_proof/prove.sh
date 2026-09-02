#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

run_case() {
  local input="$1"
  local expected="$2"
  local actual

  actual="$(krun solution.mpy \
    --definition verification-kompiled \
    -cTXT="\"${input}\"")"
  printf '%s\n' "$actual"

  case "$actual" in
    *"pyBool ( ${expected} )"*) ;;
    *)
      printf 'unexpected result for %q: expected %s\n' "$input" "$expected" >&2
      return 1
      ;;
  esac
}

run_case "apple pie" false
run_case "apple pi e" true
run_case "apple pi e " false
run_case "" false
run_case "A" true

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
