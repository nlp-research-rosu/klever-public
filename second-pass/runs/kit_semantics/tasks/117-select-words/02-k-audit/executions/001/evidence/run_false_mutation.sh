#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/117-select-words-audit
cp -a /audit-output/evidence/spec-reviewer-false-result.k "$scratch"/
cd "$scratch" || exit 2

echo '$ python3: evaluate trusted canonical and generated solution on ("a b", 1)'
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import importlib.util

for name, path in [
    ("canonical", "canonical.py"),
    ("generated", "solution.py"),
]:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print(name, repr(module.select_words("a b", 1)))
PY
python_status=$?
echo "python_exit=$python_status"
if test "$python_status" -ne 0; then
  exit 2
fi

echo '$ kprove spec-reviewer-false-result.k --definition reviewer-verification-kompiled --spec-module REVIEWER-FALSE-RESULT'
kprove spec-reviewer-false-result.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-FALSE-RESULT
proof_status=$?
echo "kprove_exit=$proof_status"

if test "$proof_status" -ne 1; then
  echo 'unexpected mutation status'
  exit 2
fi

echo 'EXPECTED_NONVACUITY_FAILURE'
exit 0
