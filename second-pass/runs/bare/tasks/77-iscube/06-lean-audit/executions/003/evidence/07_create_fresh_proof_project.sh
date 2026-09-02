#!/usr/bin/env bash
set -euo pipefail
set -x

destination=/tmp/audit-work/77-iscube-proof-audit
test ! -e "$destination"
mkdir -p "$destination/Base"
cp -a /candidate/. "$destination/"
cp -a /reference/klean-generation/generated/. "$destination/Base/"
find "$destination" -maxdepth 3 -type f -print | sort
sha256sum \
  "$destination/Proof.lean" \
  "$destination/lakefile.lean" \
  "$destination/lean-toolchain" \
  "$destination/Base/Klean77Iscube/Lemmas.lean" \
  "$destination/Base/obligation-map.json"
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.klean_export import tree_digest; print(tree_digest(Path("/tmp/audit-work/77-iscube-proof-audit/Base")))'
