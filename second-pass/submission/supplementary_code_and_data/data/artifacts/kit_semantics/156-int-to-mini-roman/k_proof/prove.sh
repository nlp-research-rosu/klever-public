#!/usr/bin/env bash
set -u
set -o pipefail

mkdir -p proof-logs

python3 py2mpy.py solution.py > solution.mpy || exit 1
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy || exit 1
python3 validate_artifacts.py \
  > proof-logs/artifact-validation.log 2>&1 || exit 1

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  > proof-logs/kompile-llvm.log 2>&1 || exit 1

krun concrete_tests.mpy --definition runtime-kompiled \
  > proof-logs/krun.log 2>&1 || exit 1

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  > proof-logs/kompile-haskell.log 2>&1 || exit 1

run_positive_batch() {
  batch="$1"
  first="$2"
  last="$3"
  labels=""

  for number in $(seq "$first" "$last"); do
    label=$(printf 'SPEC.roman-%04d' "$number")
    if [ -z "$labels" ]; then
      labels="$label"
    else
      labels="$labels,$label"
    fi
  done

  kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC \
    --claims "$labels" \
    > "proof-logs/positive-${batch}.log" 2>&1
  rc=$?
  printf '%s\n' "$rc" > "proof-logs/positive-${batch}.exit"
  if [ "$rc" -ne 0 ] || ! rg -q '^#Top$' "proof-logs/positive-${batch}.log"; then
    echo "positive proof batch $batch failed" >&2
    return 1
  fi
}

# Ten positive target-proof commands cover every claim in spec.k exactly once.
run_positive_batch 01 1 100 || exit 1
run_positive_batch 02 101 200 || exit 1
run_positive_batch 03 201 300 || exit 1
run_positive_batch 04 301 400 || exit 1
run_positive_batch 05 401 500 || exit 1
run_positive_batch 06 501 600 || exit 1
run_positive_batch 07 601 700 || exit 1
run_positive_batch 08 701 800 || exit 1
run_positive_batch 09 801 900 || exit 1
run_positive_batch 10 901 1000 || exit 1

# Gate A body-sensitivity probe: this materially changed body must be rejected.
python3 validate_artifacts.py --solution solution_mutant.py \
  > proof-logs/body-mutation.log 2>&1
body_mutation_rc=$?
printf '%s\n' "$body_mutation_rc" > proof-logs/body-mutation.exit
if [ "$body_mutation_rc" -eq 0 ]; then
  echo "body mutation unexpectedly passed program identity" >&2
  exit 1
fi

# Gate A5 non-vacuity probe: a false result for input 19 must not prove.
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > proof-logs/vacuity.log 2>&1
vacuity_rc=$?
printf '%s\n' "$vacuity_rc" > proof-logs/vacuity.exit
if [ "$vacuity_rc" -eq 0 ]; then
  echo "false postcondition unexpectedly proved" >&2
  exit 1
fi

echo "All positive proof batches printed #Top and exited 0."
echo "Body and postcondition mutations failed as expected."
