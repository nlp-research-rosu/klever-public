#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/source-and-target-inspection.log

{
  printf '%s\n' '$ rg -n "#isEqualToSumEven" /reference/k-proof'
  rg -n '#isEqualToSumEven' /reference/k-proof
  printf '\n%s\n' '$ nl -ba verification.k'
  nl -ba /reference/k-proof/verification.k
  printf '\n%s\n' '$ nl -ba solution.mpy'
  nl -ba /reference/k-proof/solution.mpy
  printf '\n%s\n' '$ nl -ba solution.py'
  nl -ba /reference/k-proof/solution.py
  printf '\n%s\n' '$ nl -ba prompt.py'
  nl -ba /reference/k-proof/prompt.py
  printf '\n%s\n' '$ nl -ba semantics/call.k | sed -n "18,94p"'
  nl -ba /reference/k-proof/reference-semantics/semantics/call.k |
    sed -n '18,94p'
  printf '\n%s\n' '$ nl -ba semantics/functions.k | sed -n "62,91p"'
  nl -ba /reference/k-proof/reference-semantics/semantics/functions.k |
    sed -n '62,91p'
  printf '\n%s\n' '$ nl -ba semantics/core.k | sed -n "129,210p"'
  nl -ba /reference/k-proof/reference-semantics/semantics/core.k |
    sed -n '129,210p'
  printf '\n%s\n' '$ nl -ba semantics/operators.k | sed -n "10,20p"'
  nl -ba /reference/k-proof/reference-semantics/semantics/operators.k |
    sed -n '10,20p'
  printf '\n%s\n' '$ nl -ba semantics/int.k | sed -n "7,28p"'
  nl -ba /reference/k-proof/reference-semantics/semantics/int.k |
    sed -n '7,28p'
  printf '\n%s\n' '$ nl -ba semantics/bool.k | sed -n "8,25p"'
  nl -ba /reference/k-proof/reference-semantics/semantics/bool.k |
    sed -n '8,25p'
  printf '\n%s\n' '$ python3 -m json.tool obligation-map.json'
  python3 -m json.tool \
    /reference/klean-generation/generated/obligation-map.json
  printf '\n%s\n' '$ nl -ba generated Lemmas.lean'
  nl -ba \
    /reference/klean-generation/generated/Klean138IsEqualToSumEven/Lemmas.lean
  printf '\n%s\n' '$ rg -n "targetStatement" generated; accept exit 1 as no match'
  rg -n 'targetStatement' /reference/klean-generation/generated
  target_code=$?
  printf 'RG_EXIT_CODE: %s\n' "$target_code"
  if [[ "$target_code" -ne 1 ]]; then
    exit 1
  fi
  printf '\n%s\n' '$ test ! -e /candidate'
  test ! -e /candidate
  code=$?
  printf 'TEST_EXIT_CODE: %s\n' "$code"
  exit "$code"
} >"$log" 2>&1
