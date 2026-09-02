#!/usr/bin/env bash
set -u

export PATH="$HOME/.nix-profile/bin:$PATH"
scratch=/tmp/audit-work/140-fix-spaces
evidence=/audit-output/evidence

cd "$scratch" || exit 2

printf '$ kast solution.mpy --definition proof-main-kompiled --module MPY-SYNTAX --sort Module --expand-macros --output kore > kast-solution.kore\n'
kast solution.mpy \
  --definition proof-main-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore > kast-solution.kore
status_solution=$?
printf '[exit %d]\n' "$status_solution"

printf '$ kast --expression solutionModule --definition proof-main-kompiled --module FIX-SPACES-BASE --sort Module --expand-macros --output kore > kast-macro.kore\n'
kast \
  --expression solutionModule \
  --definition proof-main-kompiled \
  --module FIX-SPACES-BASE \
  --sort Module \
  --expand-macros \
  --output kore > kast-macro.kore
status_macro=$?
printf '[exit %d]\n' "$status_macro"

printf '$ cmp -s kast-solution.kore kast-macro.kore\n'
cmp -s kast-solution.kore kast-macro.kore
status_cmp=$?
printf '[exit %d]\n' "$status_cmp"

printf '$ sha256sum kast-solution.kore kast-macro.kore\n'
sha256sum kast-solution.kore kast-macro.kore
status_hash=$?
printf '[exit %d]\n' "$status_hash"

cp kast-solution.kore "$evidence/program-identity-solution.kore"
cp kast-macro.kore "$evidence/program-identity-macro.kore"

if [[ "$status_solution" -ne 0 || "$status_macro" -ne 0 || "$status_cmp" -ne 0 ]]; then
  exit 1
fi
