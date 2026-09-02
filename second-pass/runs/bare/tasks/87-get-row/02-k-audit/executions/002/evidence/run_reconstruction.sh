#!/usr/bin/env bash
set -u

work=/tmp/audit-work/87-get-row-review
cd "$work" || exit 1

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return "$status"
}

run kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition concrete-kompiled || exit $?

run krun solution.mpy \
  --definition concrete-kompiled \
  -cLST='pyList(vcons(pyList(vcons(pyInt(1),vcons(pyInt(2),vcons(pyInt(1),vnil)))),vcons(pyList(vcons(pyInt(1),vnil)),vnil)))' \
  -cX='pyInt(1)' \
  --output pretty || exit $?

run python3 -c \
  'from solution import get_row; from trusted_canonical import get_row as c; x=([[1,2,1],[1]],1); print("generated=",get_row(*x)); print("canonical=",c(*x))' \
  || exit $?

run krun solution.mpy \
  --definition concrete-kompiled \
  -cLST='pyList(vnil)' \
  -cX='pyInt(1)' \
  --output pretty || exit $?

run python3 -c \
  'from solution import get_row; from trusted_canonical import get_row as c; x=([],1); print("generated=",get_row(*x)); print("canonical=",c(*x))' \
  || exit $?

run krun solution.mpy \
  --definition concrete-kompiled \
  -cLST='pyList(vcons(pyList(vnil),vcons(pyList(vcons(pyInt(-1),vcons(pyInt(0),vcons(pyInt(-1),vnil)))),vcons(pyList(vnil),vnil))))' \
  -cX='pyInt(-1)' \
  --output pretty || exit $?

run python3 -c \
  'from solution import get_row; from trusted_canonical import get_row as c; x=([[],[-1,0,-1],[]],-1); print("generated=",get_row(*x)); print("canonical=",c(*x))' \
  || exit $?

run kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition proof-kompiled || exit $?

printf '%s\n' \
  'COMMAND: kast solution.mpy --definition proof-kompiled --module MPY-SYNTAX --sort Program --output kore > parsed-program.kore'
kast solution.mpy \
  --definition proof-kompiled \
  --module MPY-SYNTAX \
  --sort Program \
  --output kore > parsed-program.kore
status=$?
printf 'EXIT: %d\n' "$status"
if [ "$status" -ne 0 ]; then exit "$status"; fi

printf '%s\n' \
  'COMMAND: kast --expression solutionProgram --definition proof-kompiled --module VERIFICATION --sort Program --expand-macros --output kore > claimed-program.kore'
kast \
  --expression solutionProgram \
  --definition proof-kompiled \
  --module VERIFICATION \
  --sort Program \
  --expand-macros \
  --output kore > claimed-program.kore
status=$?
printf 'EXIT: %d\n' "$status"
if [ "$status" -ne 0 ]; then exit "$status"; fi

run cmp -s parsed-program.kore claimed-program.kore || exit $?
run sha256sum parsed-program.kore claimed-program.kore || exit $?

run kprove spec.k \
  --definition proof-kompiled \
  --spec-module SPEC || exit $?

labels=(
  example-prompt
  example-empty
  example-third
  symbolic-000
  symbolic-001
  symbolic-010
  symbolic-011
  symbolic-100
  symbolic-101
  symbolic-110
  symbolic-111
)
for label in "${labels[@]}"; do
  run kprove spec-labelled.k \
    --definition proof-kompiled \
    --spec-module SPEC-LABELLED \
    --claims "SPEC-LABELLED.$label" || exit $?
done

printf 'CLAIMS_RUN_INDIVIDUALLY: %d\n' "${#labels[@]}"
exit 0
