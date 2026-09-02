#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/pairs-audit
EVIDENCE=/audit-output/evidence
SPEC=/audit-output/evidence/stage5_bridge-witness.k
cd "$WORK" || exit 99
export PATH="$HOME/.nix-profile/bin:$PATH"

echo '$ trusted translation of bridge context'
python3 trusted-py2mpy.py \
  /audit-output/evidence/stage5_bridge_context.py \
  > stage5_bridge_context.mpy
translate_status=$?
echo "exit=$translate_status"
cp stage5_bridge_context.mpy "$EVIDENCE/stage5_bridge_context.mpy"

echo '$ krun context under fixed base definition'
krun stage5_bridge_context.mpy \
  --definition verification-kompiled \
  > "$EVIDENCE/stage5_context_fixed.log" 2>&1
fixed_context_status=$?
echo "exit=$fixed_context_status"

echo '$ krun context under bridge-enabled definition'
krun stage5_bridge_context.mpy \
  --definition verification-lemmas-kompiled \
  > "$EVIDENCE/stage5_context_extended.log" 2>&1
extended_context_status=$?
echo "exit=$extended_context_status"

run_proof() {
  name=$1
  definition=$2
  module=$3
  claim=$4
  (
    echo "$ kprove $SPEC --definition $definition --spec-module $module --claims $module.$claim"
    kprove "$SPEC" \
      --definition "$definition" \
      --spec-module "$module" \
      --claims "$module.$claim"
    status=$?
    echo "exit=$status"
    exit "$status"
  ) > "$EVIDENCE/$name.log" 2>&1
  status=$?
  echo "$name exit=$status"
  return "$status"
}

overall=0
run_proof stage5_fixed_correct_heap \
  verification-kompiled \
  AUDIT-BRIDGE-FIXED \
  real-empty-fixed-heap
status=$?
(( status == 0 )) || overall=1

run_proof stage5_fixed_rejects_synthetic_heap \
  verification-kompiled \
  AUDIT-BRIDGE-FIXED \
  real-empty-synthetic-heap
fixed_false_status=$?
if (( fixed_false_status == 0 )); then
  overall=1
fi

run_proof stage5_extended_accepts_synthetic_heap \
  verification-lemmas-kompiled \
  AUDIT-BRIDGE-EXTENDED \
  real-empty-synthetic-heap
extended_false_status=$?
(( extended_false_status == 0 )) || overall=1

echo "expected_fixed_false_exit_nonzero=$fixed_false_status"
echo "extended_false_conclusion_exit=$extended_false_status"
exit "$overall"
