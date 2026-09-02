#!/usr/bin/env bash
set -o pipefail
printf '%s\n' 'COMMAND: locate relevant operational semantics and live K tooling'
printf '\n[K tools]\n'
command -v kompile || true
command -v kprove || true
command -v krun || true
kompile --version 2>&1 || true
kprove --version 2>&1 || true
printf '\n[map deletion/update semantics references]\n'
rg -n -C 5 --fixed-strings '<-undef]' \
  /reference/k-proof/reference-semantics \
  /reference/k-proof/verification.k || true
rg -n -C 4 'in_keys|undef|scopeLoc|#endcall|frame\(' \
  /reference/k-proof/reference-semantics/semantics/call.k \
  /reference/k-proof/reference-semantics/semantics/core.k \
  /reference/k-proof/reference-semantics/semantics/dict.k \
  /reference/k-proof/reference-semantics/semantics/builtins.k |
  sed -n '1,800p'
printf '\n[Stage 1 top-level entries]\n'
find /reference/k-proof -maxdepth 1 -printf '%f %y\n' | sort
