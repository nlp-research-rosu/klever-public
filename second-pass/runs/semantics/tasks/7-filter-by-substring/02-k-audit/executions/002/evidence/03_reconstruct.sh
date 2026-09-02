#!/usr/bin/env bash
set -u

work=/tmp/audit-work/7-filter-by-substring/candidate
out=/audit-output/evidence
failed=0

run_logged() {
  name=$1
  shift
  log="$out/03_${name}.log"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  (
    cd "$work" || exit 125
    "$@"
  ) >"$log" 2>&1
  status=$?
  printf 'EXIT: %d\n' "$status"
  lines=$(wc -l <"$log")
  printf 'LOG: %s (%d lines)\n' "$log" "$lines"
  sed -n '1,200p' "$log"
  if (( lines > 280 )); then
    printf '[... bounded log: middle omitted ...]\n'
    tail -n 80 "$log"
  fi
  if (( status != 0 )); then
    failed=1
  fi
}

run_logged prebuild find . -maxdepth 2 -type d -name '*-kompiled' -print
run_logged translate_concrete bash -c \
  'python3 ../trusted/py2mpy.py concrete_tests.py > concrete_tests.regenerated.mpy && cmp concrete_tests.regenerated.mpy concrete_tests.mpy'
run_logged llvm_build kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
run_logged concrete_krun krun concrete_tests.regenerated.mpy \
  --definition audit-runtime-kompiled
run_logged haskell_build kompile verification.k \
  --backend haskell \
  --main-module FILTER-VERIFICATION \
  --syntax-module FILTER-VERIFICATION \
  --output-definition audit-verification-kompiled
run_logged loop_claim kprove spec-loop-only.k \
  --definition audit-verification-kompiled \
  --spec-module FILTER-SPEC-LOOP-ONLY \
  --output pretty
run_logged entry_claim kprove spec-entry-only.k \
  --definition audit-verification-kompiled \
  --spec-module FILTER-SPEC-ENTRY-ONLY \
  --output pretty
run_logged all_claims kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module FILTER-SPEC \
  --output pretty

exit "$failed"
