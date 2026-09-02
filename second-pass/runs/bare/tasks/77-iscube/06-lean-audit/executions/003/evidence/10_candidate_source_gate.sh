#!/usr/bin/env bash
set -euo pipefail
set -x

project=/tmp/audit-work/77-iscube-proof-audit
rg -n --hidden \
  -g '*.lean' \
  '\b(sorry|admit|unsafe|axiom|opaque)\b' \
  /candidate || test "$?" -eq 1
rg -n --hidden \
  -g '*.lean' \
  '^\s*(def|theorem|lemma|axiom|opaque)\s+' \
  /candidate
sha256sum \
  /candidate/Proof.lean \
  "$project/Proof.lean" \
  /reference/klean-generation/generated/Klean77Iscube/Lemmas.lean \
  "$project/Base/Klean77Iscube/Lemmas.lean"
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.klean_export import tree_digest; print(tree_digest(Path("/tmp/audit-work/77-iscube-proof-audit/Base")))'
