#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/43-pairs-sum-to-zero
source_dir="$scratch/candidate"
evidence=/audit-output/evidence

run_logged() {
  local log="$1"
  shift
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  "$@" >> "$log" 2>&1
  local status=$?
  echo "EXIT_STATUS: $status" >> "$log"
  return "$status"
}

{
  echo 'COMMAND: kompile --version'
  kompile --version
  echo 'COMMAND: kprove --version'
  kprove --version
  echo 'COMMAND: krun --version'
  krun --version
  echo 'EXIT_STATUS: 0'
} > "$evidence/03-tool-versions.log" 2>&1

for output in \
  "$scratch/concrete-kompiled" \
  "$scratch/fresh-semantic-kompiled" \
  "$scratch/proof-kompiled"
do
  if [[ -e "$output" || -L "$output" ]]; then
    echo "Refusing to reuse pre-existing build output: $output" >&2
    exit 90
  fi
done

cd "$source_dir" || exit 91

run_logged "$evidence/03-kompile-concrete.log" \
  kompile semantic.k \
    --backend llvm \
    --main-module MPY-SEMANTIC \
    --syntax-module MPY-SYNTAX \
    --output-definition "$scratch/concrete-kompiled" \
  || exit $?

run_logged "$evidence/03-kompile-fresh-semantic-haskell.log" \
  kompile semantic.k \
    --backend haskell \
    --main-module MPY-SEMANTIC \
    --syntax-module MPY-SYNTAX \
    --output-definition "$scratch/fresh-semantic-kompiled" \
  || exit $?

run_logged "$evidence/03-kompile-proof-haskell.log" \
  kompile verification.k \
    --backend haskell \
    --main-module MPY-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$scratch/proof-kompiled" \
  || exit $?

run_logged "$evidence/03-positive-kprove-candidate-command.log" \
  kprove spec.k \
    --definition "$scratch/fresh-semantic-kompiled" \
    --spec-module SPEC \
  || exit $?

run_logged "$evidence/03-positive-kprove-proof-definition.log" \
  kprove spec.k \
    --definition "$scratch/proof-kompiled" \
    --spec-module SPEC \
  || exit $?

echo 'BUILD_AND_POSITIVE_PROOF_EXIT_STATUS: 0'
