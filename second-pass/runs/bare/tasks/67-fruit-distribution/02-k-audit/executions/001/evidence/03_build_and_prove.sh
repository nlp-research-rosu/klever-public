#!/usr/bin/env bash
set -u

audit_failures=0
audit_work=/tmp/audit-work/fresh

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  if (( status != 0 )); then
    audit_failures=$((audit_failures + 1))
  fi
  return 0
}

run_expect_text() {
  expected=$1
  shift
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  output=$("$@" 2>&1)
  status=$?
  printf '%s\n' "$output"
  printf 'EXIT_STATUS: %d\n' "$status"
  if (( status != 0 )) || [[ "$output" != *"$expected"* ]]; then
    printf 'EXPECTED_TEXT_NOT_CONFIRMED: %s\n' "$expected"
    audit_failures=$((audit_failures + 1))
  else
    printf 'EXPECTED_TEXT_CONFIRMED: %s\n' "$expected"
  fi
  return 0
}

run kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition audit-semantic-kompiled
run krun solution.mpy \
  --definition audit-semantic-kompiled \
  --output pretty

run kompile semantic-driver.k \
  --main-module AUDIT-DRIVER \
  --syntax-module AUDIT-DRIVER \
  --backend llvm \
  --output-definition audit-driver-kompiled
run_expect_text 'VInt ( 7 )' krun audit-normal.mpy \
  --definition audit-driver-kompiled \
  --output pretty
run_expect_text 'VInt ( 0 )' krun audit-zero.mpy \
  --definition audit-driver-kompiled \
  --output pretty
run_expect_text 'VInt ( 0 )' krun audit-all-fruit.mpy \
  --definition audit-driver-kompiled \
  --output pretty

run python3 -c \
  'import importlib.util; p="/tmp/audit-work/fresh/solution.py"; s=importlib.util.spec_from_file_location("candidate_for_k_compare",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.fruit_distribution("7 apples and 5 oranges",19)); print(m.fruit_distribution("0 apples and 0 oranges",0)); print(m.fruit_distribution("7 apples and 5 oranges",12))'
run python3 -c \
  'import importlib.util; p="/reference/canonical.py"; s=importlib.util.spec_from_file_location("canonical_for_k_compare",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.fruit_distribution("7 apples and 5 oranges",19)); print(m.fruit_distribution("0 apples and 0 oranges",0)); print(m.fruit_distribution("7 apples and 5 oranges",12))'

run kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  --output-definition audit-verification-kompiled

printf 'COMMAND: krun solution.mpy --definition audit-verification-kompiled --depth 0 --output kast > /tmp/audit-work/fresh/source.kast\n'
krun solution.mpy \
  --definition audit-verification-kompiled \
  --depth 0 \
  --output kast \
  > source.kast
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if (( status != 0 )); then audit_failures=$((audit_failures + 1)); fi

printf 'COMMAND: krun solution-alias.mpy --definition audit-verification-kompiled --depth 0 --output kast > /tmp/audit-work/fresh/alias.kast\n'
krun solution-alias.mpy \
  --definition audit-verification-kompiled \
  --depth 0 \
  --output kast \
  > alias.kast
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
if (( status != 0 )); then audit_failures=$((audit_failures + 1)); fi
run cmp --silent source.kast alias.kast
run sha256sum source.kast alias.kast

run_expect_text '#Top' kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
for claim_name in general example-1 example-2 example-3 example-4; do
  run_expect_text '#Top' kprove spec-audit.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-AUDIT \
    --claims "SPEC-AUDIT.${claim_name}"
done

printf 'AUDIT_FAILURE_COUNT: %d\n' "$audit_failures"
exit "$audit_failures"
