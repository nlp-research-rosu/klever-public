#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/extract_verification_module.py > /tmp/audit-work/source/verification-module.mpy'
python3 /audit-output/evidence/extract_verification_module.py \
  > /tmp/audit-work/source/verification-module.mpy
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: kast solution.regenerated.mpy --definition runtime-kompiled --sort Module --output kast > regenerated-module.kast'
kast \
  solution.regenerated.mpy \
  --definition runtime-kompiled \
  --sort Module \
  --output kast \
  > regenerated-module.kast
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: kast verification-module.mpy --definition runtime-kompiled --sort Module --output kast > verification-module.kast'
kast \
  verification-module.mpy \
  --definition runtime-kompiled \
  --sort Module \
  --output kast \
  > verification-module.kast
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: cmp -s regenerated-module.kast verification-module.kast'
cmp -s regenerated-module.kast verification-module.kast
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: sha256sum regenerated-module.kast verification-module.kast'
sha256sum regenerated-module.kast verification-module.kast
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: sed -n 1,80p verification-module.mpy'
sed -n '1,80p' verification-module.mpy
printf 'EXIT_STATUS: %s\n' "$?"
