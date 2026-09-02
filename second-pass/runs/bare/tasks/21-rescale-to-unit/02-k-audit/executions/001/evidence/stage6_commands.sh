#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run python3 -c '
from importlib.util import module_from_spec, spec_from_file_location
def load(path, name):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit
values = [0.0, 2.0]
print("satisfying_input=", values)
print("candidate=", load("/tmp/audit-work/source/solution.py", "candidate_nv")(values))
print("canonical=", load("/reference/canonical.py", "canonical_nv")(values))
print("mutated_expected=", [0.0, 0.0])
'

run kprove /audit-output/evidence/spec-vacuity-audit.k \
  -I /tmp/audit-work/source \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run

run kprove /audit-output/evidence/spec-vacuity-audit.k \
  -I /tmp/audit-work/source \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
