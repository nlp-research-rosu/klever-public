#!/usr/bin/env bash
set -u

src=/tmp/audit-work/candidate-src
reconstruction=/tmp/audit-work/reconstruction-final
proof_definition="$reconstruction/proof-kompiled"
runtime_definition="$reconstruction/runtime-kompiled"

mkdir -p "$reconstruction" || exit 90
cd "$src" || exit 91

printf '%s\n' '$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/reconstruction-final/proof-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_definition"
proof_build_rc=$?
printf 'EXIT proof_build=%s\n' "$proof_build_rc"

printf '%s\n' '$ kprove spec.k --definition /tmp/audit-work/reconstruction-final/proof-kompiled --spec-module SPEC --claims SPEC.loop-invariant'
kprove spec.k \
  --definition "$proof_definition" \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
loop_rc=$?
printf 'EXIT loop_claim=%s\n' "$loop_rc"

printf '%s\n' '$ kprove spec.k --definition /tmp/audit-work/reconstruction-final/proof-kompiled --spec-module SPEC'
kprove spec.k \
  --definition "$proof_definition" \
  --spec-module SPEC
all_rc=$?
printf 'EXIT all_target_claims=%s\n' "$all_rc"

printf '%s\n' '$ kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/reconstruction-final/runtime-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$runtime_definition"
runtime_build_rc=$?
printf 'EXIT runtime_build=%s\n' "$runtime_build_rc"

printf '%s\n' '$ python3 /reference/py2mpy.py /audit-output/evidence/stage3/concrete_audit.py > /tmp/audit-work/reconstruction-final/concrete_audit.mpy'
python3 /reference/py2mpy.py \
  /audit-output/evidence/stage3/concrete_audit.py \
  > "$reconstruction/concrete_audit.mpy"
translate_rc=$?
printf 'EXIT concrete_translate=%s\n' "$translate_rc"

printf '%s\n' '$ krun /tmp/audit-work/reconstruction-final/concrete_audit.mpy --definition /tmp/audit-work/reconstruction-final/runtime-kompiled'
krun "$reconstruction/concrete_audit.mpy" \
  --definition "$runtime_definition"
runtime_rc=$?
printf 'EXIT concrete_runtime=%s\n' "$runtime_rc"

if (( proof_build_rc != 0 ||
      loop_rc != 0 ||
      all_rc != 0 ||
      runtime_build_rc != 0 ||
      translate_rc != 0 ||
      runtime_rc != 0 )); then
  exit 1
fi

exit 0
