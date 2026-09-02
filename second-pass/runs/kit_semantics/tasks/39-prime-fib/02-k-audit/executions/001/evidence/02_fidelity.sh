#!/usr/bin/env bash
set -eu
set -o pipefail

scratch=/tmp/audit-work/39-prime-fib-audit

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

echo "Fresh source copies used for execution"
run mkdir -p "$scratch"
run cp -a /reference/reference-semantics "$scratch/"
run cp /reference/canonical.py "$scratch/trusted_canonical.py"
run cp /reference/prompt.py "$scratch/trusted_prompt.py"
run cp /reference/py2mpy.py "$scratch/py2mpy.py"
run cp /candidate/solution.py "$scratch/solution.py"
run cp /candidate/solution.mpy "$scratch/solution.submitted.mpy"
run cp /candidate/verification.k /candidate/spec.k /candidate/spec-vacuity.k /candidate/spec-body-mutation.k "$scratch/"
run cp /audit-output/evidence/02_differential.py "$scratch/02_differential.py"

echo "Trusted regeneration and byte-identity check"
printf '$ (cd %q && python3 py2mpy.py solution.py > solution.regenerated.mpy)\n' "$scratch"
(cd "$scratch" && python3 py2mpy.py solution.py > solution.regenerated.mpy)
printf '[exit %d]\n' "$?"
run cmp -s "$scratch/solution.submitted.mpy" "$scratch/solution.regenerated.mpy"
run sha256sum "$scratch/solution.submitted.mpy" "$scratch/solution.regenerated.mpy"

echo "Independent canonical-versus-generated differential"
printf '$ (cd %q && python3 02_differential.py)\n' "$scratch"
(cd "$scratch" && python3 02_differential.py)
printf '[exit %d]\n' "$?"
