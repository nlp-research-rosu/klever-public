#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd /tmp/audit-work/reconstruction || exit 125
run cp /audit-output/evidence/loop_binding_witness.py loop-binding-witness.py
run cp /audit-output/evidence/spec-loop-binding-witness.k spec-loop-binding-witness.k

printf '%s\n' '$ python3 trusted-py2mpy.py loop-binding-witness.py > loop-binding-witness.mpy'
python3 trusted-py2mpy.py loop-binding-witness.py > loop-binding-witness.mpy
printf '[exit %d]\n' "$?"

run sha256sum loop-binding-witness.py loop-binding-witness.mpy
run sed -n 1,120p loop-binding-witness.mpy
run python3 -c \
  'import importlib.util; p="loop-binding-witness.py"; s=importlib.util.spec_from_file_location("w",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.digitSum("A"))'
run krun loop-binding-witness.mpy \
  --definition audit-concrete-llvm-kompiled \
  '-cINPUT="A"' \
  --output pretty

# A machine-checked false conclusion about Python, enabled by the semantics.
run kprove spec-loop-binding-witness.k \
  --definition audit-proof-haskell-kompiled \
  --spec-module SPEC-LOOP-BINDING-WITNESS \
  --claims SPEC-LOOP-BINDING-WITNESS.semantic-result

# The actual Python result is rejected because the K execution reaches 66.
run kprove spec-loop-binding-witness.k \
  --definition audit-proof-haskell-kompiled \
  --spec-module SPEC-LOOP-BINDING-WITNESS \
  --claims SPEC-LOOP-BINDING-WITNESS.python-result
