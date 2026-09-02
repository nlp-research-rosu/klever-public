#!/usr/bin/env bash
set -euo pipefail

nl -ba /reference/k-proof/prove.sh
rg -F -n -C 5 \
  -e 'IntSeq' \
  -e 'iCons' \
  -e 'strToCodes' \
  -e 'strContains' \
  -e '#loop' \
  -e 'For(' \
  -e 'AugAssign' \
  -e 'BoolOp' \
  -e 'notBool' \
  -e 'andBool' \
  -e 'CmpOp("in"' \
  -e 'countUpperFrom' \
  /reference/k-proof/reference-semantics \
  /reference/k-proof/verification.k \
  /reference/k-proof/spec.k \
  /reference/k-proof/solution.mpy
