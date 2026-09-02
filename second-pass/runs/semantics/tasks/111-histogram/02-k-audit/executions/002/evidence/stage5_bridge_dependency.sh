#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/111-histogram
no_bridge_definition="$audit_work/verification-no-bridge-kompiled"
overall_status=0

printf '%s\n' \
  "COMMAND: rename VERIFICATION, remove only the proof-local splitWS(tokenText(...)) rule"
(
  cd "$audit_work" &&
  sed \
    -e 's/^module VERIFICATION$/module VERIFICATION-NO-BRIDGE/' \
    -e '/^  rule splitWS(tokenText(TS:ValSeq), \.IntSeq, \.ValSeq) => TS$/d' \
    verification.k > verification-no-bridge.k
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf '%s\n' \
  "COMMAND: retarget spec-labeled.k to VERIFICATION-NO-BRIDGE"
(
  cd "$audit_work" &&
  sed \
    -e 's/requires "verification.k"/requires "verification-no-bridge.k"/' \
    -e 's/^  imports VERIFICATION$/  imports VERIFICATION-NO-BRIDGE/' \
    spec-labeled.k > spec-no-bridge.k
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf 'COMMAND: (cd %q && diff -u verification.k verification-no-bridge.k)\n' "$audit_work"
(
  cd "$audit_work" &&
  diff -u verification.k verification-no-bridge.k
)
diff_status=$?
printf 'EXPECTED_DIFF_EXIT_STATUS: %s\n' "$diff_status"
if (( diff_status != 1 )); then overall_status=1; fi

printf '%s\n' \
  "COMMAND: kompile verification-no-bridge.k --backend haskell --main-module VERIFICATION-NO-BRIDGE --syntax-module VERIFICATION-NO-BRIDGE --output-definition $no_bridge_definition"
(
  cd "$audit_work" &&
  kompile verification-no-bridge.k \
    --backend haskell \
    --main-module VERIFICATION-NO-BRIDGE \
    --syntax-module VERIFICATION-NO-BRIDGE \
    --output-definition "$no_bridge_definition"
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf '%s\n' \
  "COMMAND: kprove spec-no-bridge.k --definition $no_bridge_definition --spec-module HISTOGRAM-SPEC-LABELED --claims HISTOGRAM-SPEC-LABELED.claim-02 --warnings none"
(
  cd "$audit_work" &&
  kprove spec-no-bridge.k \
    --definition "$no_bridge_definition" \
    --spec-module HISTOGRAM-SPEC-LABELED \
    --claims HISTOGRAM-SPEC-LABELED.claim-02 \
    --warnings none
)
command_status=$?
printf 'CONCRETE_CLAIM_EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf '%s\n' \
  "COMMAND: kprove spec-no-bridge.k --definition $no_bridge_definition --spec-module HISTOGRAM-SPEC-LABELED --claims HISTOGRAM-SPEC-LABELED.claim-06 --warnings none"
(
  cd "$audit_work" &&
  kprove spec-no-bridge.k \
    --definition "$no_bridge_definition" \
    --spec-module HISTOGRAM-SPEC-LABELED \
    --claims HISTOGRAM-SPEC-LABELED.claim-06 \
    --warnings none 2>&1 | tee no-bridge-symbolic-proof.raw.log
  proof_status=${PIPESTATUS[0]}
  printf 'EXPECTED_NONZERO_EXIT_STATUS: %s\n' "$proof_status"
  test "$proof_status" -ne 0 &&
    grep -q 'WarnStuckClaimState' no-bridge-symbolic-proof.raw.log &&
    grep -q 'splitWS' no-bridge-symbolic-proof.raw.log &&
    grep -q 'tokenText' no-bridge-symbolic-proof.raw.log
)
command_status=$?
printf 'SYMBOLIC_DEPENDENCY_VALIDATION_EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

exit "$overall_status"
