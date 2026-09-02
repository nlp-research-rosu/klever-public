#!/usr/bin/env bash
set -u
set -o pipefail

EVIDENCE=/audit-output/evidence
SCRATCH=/tmp/audit-work/reconstruction
SPEC=/audit-output/evidence/bridge-shadow-spec.k

run_logged() {
  name=$1
  shift
  log="$EVIDENCE/$name.log"
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1 | tee "$log"
  status=${PIPESTATUS[0]}
  printf '[exit %d]\n' "$status"
  return 0
}

# Fixed supplied semantics: local lookup must return the shadow's 99.
run_logged stage5_shadow_fixed_99 \
  kprove "$SPEC" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module BRIDGE-SHADOW-SPEC \
  --claims shadow-fixed-result \
  --output pretty

# The same fixed semantics must reject the fabricated strength 1.
run_logged stage5_shadow_fixed_rejects_1 \
  kprove "$SPEC" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module BRIDGE-SHADOW-SPEC \
  --claims shadow-fabricated-strength \
  --output pretty

# With the candidate bridge enabled, the false strength result closes.
run_logged stage5_shadow_bridge_fabricates_1 \
  kprove "$SPEC" \
  --definition "$SCRATCH/strength-lemma-kompiled" \
  --spec-module BRIDGE-SHADOW-SPEC \
  --claims shadow-fabricated-strength \
  --output pretty

# With the candidate bridge enabled, the correct lexical result is rejected.
run_logged stage5_shadow_bridge_rejects_99 \
  kprove "$SPEC" \
  --definition "$SCRATCH/strength-lemma-kompiled" \
  --spec-module BRIDGE-SHADOW-SPEC \
  --claims shadow-fixed-result \
  --output pretty
