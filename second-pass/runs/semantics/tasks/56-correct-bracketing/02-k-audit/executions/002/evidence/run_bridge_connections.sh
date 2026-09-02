#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

run_log() {
  name="$1"
  shift
  {
    printf 'WORKDIR: %s\n' "$work"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    (
      cd "$work"
      "$@"
    )
    status=$?
    printf 'EXIT_STATUS: %d\n' "$status"
    return "$status"
  } > "$evidence/$name.log" 2>&1
}

run_log stage5_kompile_fixed \
  timeout 300s kompile fixed-verification.k \
  --backend haskell \
  --main-module FIXED-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fixed-verification-kompiled

run_log stage5_fixed_bridge_connections \
  timeout 300s kprove fixed-bridge-spec.k \
  --definition fixed-verification-kompiled \
  --spec-module FIXED-BRIDGE-SPEC \
  --claims FIXED-BRIDGE-SPEC.return-bool,FIXED-BRIDGE-SPEC.return-depth-equality,FIXED-BRIDGE-SPEC.if-bracket-open,FIXED-BRIDGE-SPEC.if-bracket-close,FIXED-BRIDGE-SPEC.augassign-plus,FIXED-BRIDGE-SPEC.augassign-minus,FIXED-BRIDGE-SPEC.if-depth-negative,FIXED-BRIDGE-SPEC.if-depth-nonnegative,FIXED-BRIDGE-SPEC.pop-normalization \
  --output pretty

run_log stage5_extended_concrete \
  timeout 300s krun audit_concrete.mpy \
  --definition audit-verification-kompiled \
  --output pretty
