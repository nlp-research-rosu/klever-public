#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/124-valid-date
LOG=/audit-output/evidence/02_fidelity.log

mkdir -p "$WORK"
cp /candidate/solution.py "$WORK/solution.py"
cp /candidate/solution.mpy "$WORK/solution.mpy"
cp /candidate/verification.k "$WORK/verification.k"
cp /candidate/spec.k "$WORK/spec.k"
cp /candidate/prove.sh "$WORK/prove.sh"
cp /reference/canonical.py "$WORK/trusted_canonical.py"
cp /reference/prompt.py "$WORK/trusted_prompt.py"
cp /reference/py2mpy.py "$WORK/trusted_py2mpy.py"
cp -a /reference/reference-semantics "$WORK/reference-semantics"

{
  printf '%s\n' 'COMMAND: python3 trusted_py2mpy.py solution.py > regenerated-solution.mpy'
  (
    cd "$WORK"
    python3 trusted_py2mpy.py solution.py > regenerated-solution.mpy
  )
  printf 'EXIT_STATUS: %s\n' "$?"

  printf '%s\n' 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy'
  cmp -s "$WORK/regenerated-solution.mpy" "$WORK/solution.mpy"
  printf 'EXIT_STATUS: %s\n' "$?"

  printf '%s\n' 'COMMAND: sha256sum submitted and regenerated solution.mpy'
  sha256sum "$WORK/solution.mpy" "$WORK/regenerated-solution.mpy"
  printf 'EXIT_STATUS: %s\n' "$?"

  printf '%s\n' 'COMMAND: python3 /audit-output/evidence/02_differential.py'
  python3 /audit-output/evidence/02_differential.py
  printf 'EXIT_STATUS: %s\n' "$?"
} >"$LOG" 2>&1

sed -n '1,240p' "$LOG"
