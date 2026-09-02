#!/usr/bin/env bash
set -u
set -o pipefail

printf '$ python3 -c <ground comparison>\n'
python3 - <<'PY'
import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension

args = ("C", ["a", "A", "B"])
canonical = load("canonical_ground", "/reference/canonical.py")(*args)
generated = load("generated_ground", "/candidate/solution.py")(*args)
print({"input": args, "canonical": canonical, "generated": generated})
assert canonical == generated == "C.A"
PY
status=$?
printf '[exit %d]\n' "$status"

printf '$ kprove /audit-output/evidence/ground-entry-spec.k --definition /tmp/audit-work/reconstruction/loop-lemmas-kompiled --spec-module GROUND-ENTRY-SPEC --claims ground-entry --output pretty\n'
kprove /audit-output/evidence/ground-entry-spec.k \
  --definition /tmp/audit-work/reconstruction/loop-lemmas-kompiled \
  --spec-module GROUND-ENTRY-SPEC \
  --claims ground-entry \
  --output pretty 2>&1 | tee /audit-output/evidence/stage4_ground_kprove.log
status=${PIPESTATUS[0]}
printf '[exit %d]\n' "$status"
