#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/46-fib4
evidence=/audit-output/evidence
overall=0

run_logged() {
  local label="$1"
  shift
  local log="$evidence/$label.log"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" >"$log" 2>&1
  local status=$?
  sed -n '1,260p' "$log"
  printf 'EXIT_STATUS=%s\n' "$status" | tee -a "$log"
  if [[ $status -ne 0 ]]; then
    overall=1
  fi
}

cd "$work" || exit 2

if [[ -e concrete-kompiled || -e proof-kompiled ]]; then
  echo "fresh-build guard failed: kompiled directory already exists"
  exit 2
fi

run_logged stage3-kompile-llvm \
  kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX --output-definition concrete-kompiled

run_logged stage3-kompile-haskell \
  kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX --output-definition proof-kompiled

for n in 0 1 2 3 4 5 7 10 20; do
  run_logged "stage3-krun-n${n}" \
    krun solution.mpy -cARG="$n" --definition concrete-kompiled
done

claims=(
  fib4-spec-link
  loop-correct
  fib4-inductive-init
  fib4-base-0
  fib4-base-1
  fib4-base-2
  fib4-base-3
  fib4-seven
)
for claim in "${claims[@]}"; do
  run_logged "stage3-kprove-${claim}" \
    kprove spec.k --definition proof-kompiled --spec-module SPEC \
    --claims "SPEC.${claim}"
done

run_logged stage3-kprove-all \
  kprove spec.k --definition proof-kompiled --spec-module SPEC

printf 'OVERALL_EXIT_STATUS=%s\n' "$overall"
exit "$overall"
