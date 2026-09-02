#!/usr/bin/env bash
set +e

audit_source=/tmp/audit-work/32-find-zero/source

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

run cp /audit-output/evidence/positive-return-spec.k "$audit_source/positive-return-spec.k"
run cp /audit-output/evidence/positive-approx-spec.k "$audit_source/positive-approx-spec.k"

cd "$audit_source" || exit 98
printf 'WORKDIR: %s\n' "$PWD"

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

printf '\nCOMMAND: python3 /reference/py2mpy.py /audit-output/evidence/concrete_audit_calls.py > %s/audit-calls.mpy\n' "$audit_source"
python3 /reference/py2mpy.py /audit-output/evidence/concrete_audit_calls.py > "$audit_source/audit-calls.mpy"
printf 'EXIT_STATUS: %d\n' "$?"

printf '\nCOMMAND: python3 /audit-output/evidence/compose_modules.py %s/solution.mpy %s/audit-calls.mpy > %s/audit-concrete.mpy\n' "$audit_source" "$audit_source" "$audit_source"
python3 /audit-output/evidence/compose_modules.py "$audit_source/solution.mpy" "$audit_source/audit-calls.mpy" > "$audit_source/audit-concrete.mpy"
printf 'EXIT_STATUS: %d\n' "$?"

run krun "$audit_source/audit-concrete.mpy" \
  --definition "$audit_source/audit-runtime-kompiled" \
  --output none

run kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

run kprove positive-return-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-POSITIVE-RETURN-SPEC

run kprove positive-approx-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-POSITIVE-APPROX-SPEC

run kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
