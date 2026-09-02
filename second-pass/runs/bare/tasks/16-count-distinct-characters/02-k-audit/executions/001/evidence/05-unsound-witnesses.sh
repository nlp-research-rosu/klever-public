#!/usr/bin/env bash
set +e
cd /tmp/audit-work/build || exit 90

run() {
  echo "$ $*"
  "$@"
  status=$?
  echo "exit=$status"
  return "$status"
}

echo '$ Python oracle and submitted program on semantic counterexamples'
python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters

canonical = load("canonical", "/reference/canonical.py")
submitted = load("submitted", "/tmp/audit-work/candidate-src/solution.py")
for value in ("Åå", "😀"):
    print(ascii(value), "canonical=", canonical(value), "submitted=", submitted(value))
PY
python_status=$?
echo "exit=$python_status"

run krun solution.mpy --definition semantics-kompiled '-cINPUT="Åå"'
krun_lower=$?

run krun solution.mpy --definition semantics-kompiled '-cINPUT="😀"'
krun_character=$?

run kprove spec-unsound-lower.k \
  --definition verification-kompiled \
  --spec-module SPEC-UNSOUND-LOWER
prove_lower=$?

run kprove spec-unsound-character.k \
  --definition verification-kompiled \
  --spec-module SPEC-UNSOUND-CHARACTER
prove_character=$?

echo "summary python=$python_status krun_lower=$krun_lower krun_character=$krun_character prove_lower=$prove_lower prove_character=$prove_character"
if (( python_status || krun_lower || krun_character || prove_lower || prove_character )); then
  exit 1
fi
