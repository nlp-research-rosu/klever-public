#!/usr/bin/env bash
set -u
cd /tmp/audit-work/case || exit 125

printf '$ kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled --warnings none\n'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  --warnings none
rc=$?
printf '[exit %d]\n' "$rc"
exit "$rc"
