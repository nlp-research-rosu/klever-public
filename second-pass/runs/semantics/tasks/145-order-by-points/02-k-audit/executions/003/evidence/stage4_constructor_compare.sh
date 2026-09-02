#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

printf '%s\n' 'COMMAND: kast solution.regenerated.mpy --definition runtime-kompiled --sort Module --output kast > regenerated-module.kast'
kast \
  solution.regenerated.mpy \
  --definition runtime-kompiled \
  --sort Module \
  --output kast \
  > regenerated-module.kast
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/compiled_module_compare.py'
python3 /audit-output/evidence/compiled_module_compare.py
printf 'EXIT_STATUS: %s\n' "$?"
