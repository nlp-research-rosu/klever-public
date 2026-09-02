#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/k-proof

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run_in_work() {
  printf '+ (cd %q &&' "$WORK"
  printf ' %q' "$@"
  printf ')\n'
  (
    cd "$WORK" || exit 125
    "$@"
  )
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'Toolchain:\n'
run kompile --version
run kprove --version
run krun --version

printf '\nFreshness checks (candidate compiled artifacts/caches were not copied):\n'
run find "$WORK" -maxdepth 1 -printf '%y %f -> %l\n'
run test ! -e "$WORK/fresh-semantic-kompiled"
run test ! -e "$WORK/fresh-verification-kompiled"

printf '\nTrusted regeneration inside scratch:\n'
run_in_work bash -c \
  'python3 py2mpy.py solution.py > regenerated-solution.mpy'
run_in_work cmp regenerated-solution.mpy solution.mpy
run_in_work sha256sum regenerated-solution.mpy solution.mpy

printf '\nBuild concrete Haskell semantics from source:\n'
run_in_work kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-semantic-kompiled

printf '\nConcrete execution and independent Python code-point oracle:\n'
for input in '1234' 'ab' '#a@C' '' '@A[`a{' 'éa' 'ß1'; do
  printf '\nINPUT=%q\n' "$input"
  run python3 -c \
    'import sys; from pathlib import Path; ns={}; exec(Path("/tmp/audit-work/k-proof/solution.py").read_text(),ns); s=sys.argv[1]; out=ns["solve"](s); print("python_result=",repr(out)); print("python_codepoints=",[ord(c) for c in out])' \
    "$input"
  run_in_work krun solution.mpy \
    --definition fresh-semantic-kompiled \
    -cINPUT="pstr(\"$input\")"
done

printf '\nBuild proof definition from source:\n'
run_in_work kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled

printf '\nRun every positive target claim (SPEC contains one unlabeled claim):\n'
run_in_work kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC
