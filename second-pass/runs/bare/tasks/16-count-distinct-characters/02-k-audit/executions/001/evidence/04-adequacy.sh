#!/usr/bin/env bash
set +e
cd /tmp/audit-work/build || exit 90

echo '$ kast solution.mpy --definition semantics-kompiled --sort Program --output json > /tmp/audit-work/generated/program.json'
kast solution.mpy \
  --definition semantics-kompiled \
  --sort Program \
  --output json > /tmp/audit-work/generated/program.json
actual_parse=$?
echo "exit=$actual_parse"

echo '$ kast claim-program.mpy --definition semantics-kompiled --sort Program --output json > /tmp/audit-work/generated/claim-program.json'
kast claim-program.mpy \
  --definition semantics-kompiled \
  --sort Program \
  --output json > /tmp/audit-work/generated/claim-program.json
claim_parse=$?
echo "exit=$claim_parse"

echo '$ cmp -s /tmp/audit-work/generated/program.json /tmp/audit-work/generated/claim-program.json'
cmp -s /tmp/audit-work/generated/program.json /tmp/audit-work/generated/claim-program.json
identity=$?
echo "exit=$identity"

echo '$ sha256sum normalized parsed program terms'
sha256sum \
  /tmp/audit-work/generated/program.json \
  /tmp/audit-work/generated/claim-program.json
hashes=$?
echo "exit=$hashes"

echo '$ krun solution.mpy --definition semantics-kompiled -cINPUT="\"\""'
krun solution.mpy --definition semantics-kompiled -cINPUT='""'
empty_run=$?
echo "exit=$empty_run"

echo '$ Python concrete substitutions for the universal claim domain'
python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters

canonical = load("canonical", "/reference/canonical.py")
submitted = load("submitted", "/tmp/audit-work/candidate-src/solution.py")
for value in ("", "xyzXYZ", "Jerry", "Åå", "😀"):
    print(ascii(value), "canonical=", canonical(value), "submitted=", submitted(value))
PY
python_compare=$?
echo "exit=$python_compare"

echo "summary actual_parse=$actual_parse claim_parse=$claim_parse identity=$identity hashes=$hashes empty_run=$empty_run python_compare=$python_compare"
if (( actual_parse || claim_parse || identity || hashes || empty_run || python_compare )); then
  exit 1
fi
