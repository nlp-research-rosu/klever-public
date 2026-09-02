#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction

run() {
  local description="$1"
  shift
  printf '\nCOMMAND (%s):' "$description"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

printf 'AUDIT STAGE 2: program fidelity and differential checks\n'
mkdir -p "$scratch"

run "copy only candidate source artifacts into scratch" \
  cp \
    /candidate/prompt.py \
    /candidate/py2mpy.py \
    /candidate/solution.py \
    /candidate/solution.mpy \
    /candidate/semantic.k \
    /candidate/spec.k \
    /candidate/verification.k \
    /candidate/prove.sh \
    "$scratch/"
copy_status=$?

printf '\nCOMMAND (regenerate MPY with trusted translator): python3 /reference/py2mpy.py %q\n' \
  "$scratch/solution.py"
python3 /reference/py2mpy.py "$scratch/solution.py" > "$scratch/solution.regenerated.mpy"
translator_status=$?
printf 'EXIT STATUS: %d\n' "$translator_status"

run "submitted MPY is byte-identical to trusted regeneration" \
  cmp -s "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
identity_status=$?

run "hash submitted and regenerated MPY" \
  sha256sum "$scratch/solution.mpy" "$scratch/solution.regenerated.mpy"
hash_status=$?

run "run independent canonical-vs-candidate differential corpus" \
  python3 /audit-output/evidence/02_differential.py
differential_status=$?

if (( copy_status || translator_status || identity_status || hash_status || differential_status )); then
  exit 1
fi

