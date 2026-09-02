#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
claims=(
  return-bool
  return-depth-equality
  if-bracket-open
  if-bracket-close
  augassign-plus
  augassign-minus
  if-depth-negative
  if-depth-nonnegative
  pop-normalization
)

for label in "${claims[@]}"; do
  log="$evidence/stage5_fixed_connection_${label}.log"
  {
    printf 'WORKDIR: %s\n' "$work"
    printf 'COMMAND: timeout 120s kprove fixed-bridge-spec.k --definition fixed-verification-kompiled --spec-module FIXED-BRIDGE-SPEC --claims %q --output pretty\n' \
      "FIXED-BRIDGE-SPEC.$label"
    (
      cd "$work"
      timeout 120s kprove fixed-bridge-spec.k \
        --definition fixed-verification-kompiled \
        --spec-module FIXED-BRIDGE-SPEC \
        --claims "FIXED-BRIDGE-SPEC.$label" \
        --output pretty
    )
    status=$?
    printf 'EXIT_STATUS: %d\n' "$status"
  } > "$log" 2>&1
done
