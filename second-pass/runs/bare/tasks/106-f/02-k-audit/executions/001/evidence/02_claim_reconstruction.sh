#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/106-f
source_dir="$work/source"
definition="$work/build/verification-kompiled"
evidence=/audit-output/evidence
export PATH="$HOME/.nix-profile/bin:$PATH"

echo 'PRECONDITION: SPEC.loop-invariant was separately proved with exit 0 and #Top.'
rg -x '#Top' "$evidence/02_kprove_loop_invariant.log"
loop_evidence_status=$?
echo "EXIT_STATUS: $loop_evidence_status"

echo 'COMMAND: isolate SPEC.main-correct, retaining separately proved loop claim as a trusted lemma'
(
  cd "$source_dir" &&
  timeout 180 kprove spec.k \
    --definition "$definition" \
    --spec-module SPEC \
    --claims SPEC.loop-invariant,SPEC.main-correct \
    --trusted SPEC.loop-invariant \
    --output pretty
) 2>&1 | tee "$evidence/02_kprove_main_with_proved_loop.log"
main_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $main_status" | tee -a "$evidence/02_kprove_main_with_proved_loop.log"

echo 'COMMAND: prove all positive claims together with neither claim trusted'
(
  cd "$source_dir" &&
  timeout 180 kprove spec.k \
    --definition "$definition" \
    --spec-module SPEC \
    --output pretty
) 2>&1 | tee "$evidence/02_kprove_all.log"
all_status=${PIPESTATUS[0]}
echo "EXIT_STATUS: $all_status" | tee -a "$evidence/02_kprove_all.log"

echo 'COMMAND: verify exact #Top success lines'
top_status=0
for proof_log in \
  "$evidence/02_kprove_loop_invariant.log" \
  "$evidence/02_kprove_main_with_proved_loop.log" \
  "$evidence/02_kprove_all.log"; do
  if ! rg -x '#Top' "$proof_log"; then
    top_status=1
  fi
done
echo "EXIT_STATUS: $top_status"

if [ "$loop_evidence_status" -eq 0 ] && [ "$main_status" -eq 0 ] && [ "$all_status" -eq 0 ] && [ "$top_status" -eq 0 ]; then
  exit 0
fi
exit 1
