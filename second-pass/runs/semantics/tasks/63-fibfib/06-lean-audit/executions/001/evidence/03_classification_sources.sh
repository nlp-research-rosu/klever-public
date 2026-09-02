#!/usr/bin/env bash
set -uo pipefail

printf '%s\n' '--- frozen verification.k ---'
nl -ba /reference/k-proof/verification.k
printf '%s\n' '--- frozen source solution ---'
nl -ba /reference/k-proof/solution.py
printf '%s\n' '--- loop and final claims ---'
sed -n '1,74p' /reference/k-proof/spec.k | nl -ba
printf '%s\n' '--- supplied operational integer dispatch ---'
sed -n '1,35p' /reference/k-proof/reference-semantics/semantics/int.k | nl -ba
printf '%s\n' '--- supplied semantics import closure roots ---'
sed -n '34,90p' /reference/k-proof/reference-semantics/semantics.k | nl -ba
printf '%s\n' '--- pinned K builtin integer hooks ---'
sed -n '1258,1272p' /usr/include/kframework/builtin/domains.md | nl -ba
printf '%s\n' '--- all verification-module rules and claims ---'
rg -n '^\s*(rule|claim)\b' /reference/k-proof/verification.k
printf '%s\n' '--- exact arithmetic rule/claim occurrences in frozen K sources ---'
rg -n -F 'N:Int -Int (I:Int +Int 1)' \
  /reference/k-proof/verification.k \
  /reference/k-proof/spec.k \
  /reference/k-proof/reference-semantics || true
