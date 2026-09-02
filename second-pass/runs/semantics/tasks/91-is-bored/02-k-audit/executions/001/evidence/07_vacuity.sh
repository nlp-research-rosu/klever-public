#!/usr/bin/env bash
set -u

printf 'Witness: the mutated entry configuration is concrete and satisfiable;\n'
printf 'both Python implementations return 0 for "Hello world", while the mutation requires 1.\n'
python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored

canonical = load("canonical", "/reference/canonical.py")
generated = load("generated", "/tmp/audit-work/source/solution.py")
value = "Hello world"
print(f"input={value!r} canonical={canonical(value)} generated={generated(value)} mutated_expected=1")
PY
python_status=$?
printf '[python witness exit %d]\n' "$python_status"

printf '\nBuild/parse the selected mutation without proving it:\n'
printf '$ timeout 300s kprove spec-vacuity.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC-VACUITY --claims prompt-example-0-false --dry-run > /tmp/audit-work/vacuity-dry-run.kore\n'
timeout 300s kprove spec-vacuity.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims prompt-example-0-false \
  --dry-run > /tmp/audit-work/vacuity-dry-run.kore
dry_status=$?
printf '[exit %d]\n' "$dry_status"
wc -c /tmp/audit-work/vacuity-dry-run.kore

printf '\nProve the deliberately false selected mutation (non-zero expected):\n'
printf '$ timeout 300s kprove spec-vacuity.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC-VACUITY --claims prompt-example-0-false\n'
timeout 300s kprove spec-vacuity.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims prompt-example-0-false
prove_status=$?
printf '[exit %d]\n' "$prove_status"

if (( python_status == 0 && dry_status == 0 && prove_status != 0 && prove_status != 124 )); then
  exit 0
fi
exit 1
