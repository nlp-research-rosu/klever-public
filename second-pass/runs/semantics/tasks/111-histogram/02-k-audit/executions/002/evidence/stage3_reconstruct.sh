#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/111-histogram
runtime_definition="$audit_work/runtime-audit-kompiled"
proof_definition="$audit_work/verification-audit-kompiled"
overall_status=0

run_and_record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf 'EXIT_STATUS: %s\n' "$command_status"
  if (( command_status != 0 )); then overall_status=1; fi
  return 0
}

run_in_work_and_record() {
  printf 'COMMAND: (cd %q &&' "$audit_work"
  printf ' %q' "$@"
  printf ')\n'
  (
    cd "$audit_work" &&
    "$@"
  )
  local command_status=$?
  printf 'EXIT_STATUS: %s\n' "$command_status"
  if (( command_status != 0 )); then overall_status=1; fi
  return 0
}

run_and_record kompile --version
run_and_record krun --version
run_and_record kprove --version
run_and_record python3 /audit-output/evidence/compare_function_ast.py

printf 'COMMAND: (cd %q && python3 py2mpy.py /audit-output/evidence/k_concrete_audit.py > k-concrete-audit.mpy)\n' "$audit_work"
(
  cd "$audit_work" &&
  python3 py2mpy.py /audit-output/evidence/k_concrete_audit.py > k-concrete-audit.mpy
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

run_in_work_and_record \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$runtime_definition"

run_in_work_and_record \
  krun k-concrete-audit.mpy \
  --definition "$runtime_definition" \
  --output pretty

run_in_work_and_record \
  kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition "$proof_definition"

run_in_work_and_record \
  kprove spec.k \
  --definition "$proof_definition" \
  --spec-module HISTOGRAM-SPEC \
  --warnings none

printf '%s\n' \
  "COMMAND: (cd $audit_work && awk '<mechanical module rename and 13 inert claim labels>' spec.k > spec-labeled.k)"
(
  cd "$audit_work" &&
  awk '
    /^module HISTOGRAM-SPEC$/ {
      print "module HISTOGRAM-SPEC-LABELED"
      next
    }
    /^  claim$/ {
      claim_count++
      printf "  claim [claim-%02d]:\n", claim_count
      next
    }
    { print }
    END {
      print "LABELED_CLAIM_COUNT=" claim_count > "/dev/stderr"
      if (claim_count != 13) exit 1
    }
  ' spec.k > spec-labeled.k
)
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

for claim_number in $(seq -w 1 13); do
  run_in_work_and_record \
    kprove spec-labeled.k \
    --definition "$proof_definition" \
    --spec-module HISTOGRAM-SPEC-LABELED \
    --claims "HISTOGRAM-SPEC-LABELED.claim-$claim_number" \
    --warnings none
done

exit "$overall_status"
