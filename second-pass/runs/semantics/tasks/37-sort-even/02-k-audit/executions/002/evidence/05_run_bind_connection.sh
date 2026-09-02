#!/usr/bin/env bash
set -u

scratch="/tmp/audit-work/37-sort-even"
evidence="/audit-output/evidence"
summary="$evidence/05-bind-connection-summary.log"
definition="$scratch/bind-fixed-kompiled"

printf '%s\n' \
  'COMMAND: cp -a /audit-output/evidence/05-bind-fixed.k /tmp/audit-work/37-sort-even/bind-fixed.k' \
  'COMMAND: cp -a /audit-output/evidence/05-bind-connection-spec.k /tmp/audit-work/37-sort-even/bind-connection-spec.k' \
  > "$summary"
cp -a "$evidence/05-bind-fixed.k" "$scratch/bind-fixed.k" >> "$summary" 2>&1
copy_fixed_status=$?
cp -a "$evidence/05-bind-connection-spec.k" "$scratch/bind-connection-spec.k" >> "$summary" 2>&1
copy_spec_status=$?
printf 'COPY_FIXED_EXIT_STATUS: %s\n' "$copy_fixed_status" >> "$summary"
printf 'COPY_SPEC_EXIT_STATUS: %s\n' "$copy_spec_status" >> "$summary"

build_log="$evidence/05-bind-connection-build.log"
printf '%s\n' \
  'COMMAND: kompile bind-fixed.k --backend haskell --main-module BIND-FIXED --syntax-module MPY-SYNTAX -I . --output-definition bind-fixed-kompiled' \
  > "$build_log"
if [ "$copy_fixed_status" -eq 0 ] && [ "$copy_spec_status" -eq 0 ]; then
  (
    cd "$scratch" &&
    kompile bind-fixed.k \
      --backend haskell \
      --main-module BIND-FIXED \
      --syntax-module MPY-SYNTAX \
      -I . \
      --output-definition "$definition"
  ) >> "$build_log" 2>&1
  build_status=$?
else
  build_status=1
fi
printf 'EXIT_STATUS: %s\n' "$build_status" >> "$build_log"
printf 'BUILD_EXIT_STATUS: %s\n' "$build_status" >> "$summary"

proof_log="$evidence/05-bind-connection-proof.log"
printf '%s\n' \
  'COMMAND: kprove bind-connection-spec.k --definition bind-fixed-kompiled --spec-module BIND-CONNECTION-SPEC --claims BIND-CONNECTION-SPEC.singleton-bind --output pretty' \
  > "$proof_log"
if [ "$build_status" -eq 0 ]; then
  (
    cd "$scratch" &&
    kprove bind-connection-spec.k \
      --definition "$definition" \
      --spec-module BIND-CONNECTION-SPEC \
      --claims BIND-CONNECTION-SPEC.singleton-bind \
      --output pretty
  ) >> "$proof_log" 2>&1
  proof_status=$?
else
  proof_status=1
fi
printf 'EXIT_STATUS: %s\n' "$proof_status" >> "$proof_log"
printf 'PROOF_EXIT_STATUS: %s\n' "$proof_status" >> "$summary"

top_status=1
if [ "$proof_status" -eq 0 ] && rg -q '^#Top$' "$proof_log"; then
  top_status=0
fi
printf 'TOP_CHECK_EXIT_STATUS: %s\n' "$top_status" >> "$summary"

if [ "$copy_fixed_status" -ne 0 ] || [ "$copy_spec_status" -ne 0 ] || \
   [ "$build_status" -ne 0 ] || [ "$proof_status" -ne 0 ] || \
   [ "$top_status" -ne 0 ]; then
  printf '%s\n' 'OVERALL_EXIT_STATUS: 1' >> "$summary"
  exit 1
fi
printf '%s\n' 'OVERALL_EXIT_STATUS: 0' >> "$summary"
exit 0
