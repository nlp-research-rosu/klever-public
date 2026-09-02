#!/usr/bin/env bash
set -u

work=/tmp/audit-work/46-fib4-audit/candidate-src
evidence=/audit-output/evidence

run_logged() {
  local tag=$1
  shift
  local log="$evidence/$tag.log"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1 | tee "$log"
  local rc=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$rc" | tee -a "$log"
  return 0
}

run_logged stage6_copy_mutation cp \
  "$evidence/spec-vacuity.k" "$work/spec-vacuity.k"

run_logged stage6_python_witness python3 -c \
  'import importlib.util
def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m.fib4
c = load("/tmp/audit-work/46-fib4-audit/reference/canonical.py", "canonical")
g = load("/tmp/audit-work/46-fib4-audit/candidate-src/solution.py", "candidate")
print({"n": 7, "canonical": c(7), "candidate": g(7), "mutated_expected": 15})
raise SystemExit(0 if c(7) == g(7) == 14 and g(7) != 15 else 1)'

cd "$work" || exit 99

run_logged stage6_mutation_dry_run timeout 120s \
  kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module FIB4-SPEC-VACUITY \
  --claims FIB4-SPEC-VACUITY.operational-cases-false \
  --dry-run

run_logged stage6_mutation_proof timeout 300s \
  kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module FIB4-SPEC-VACUITY \
  --claims FIB4-SPEC-VACUITY.operational-cases-false \
  --output pretty
