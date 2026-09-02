#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/audit79
evidence=/audit-output/evidence
status=0
export PATH="$HOME/.nix-profile/bin:$PATH"

record_status() {
  local command_status=$1
  echo "EXIT_STATUS $command_status"
  if (( command_status != 0 )); then status=1; fi
}

echo 'COMMAND: command -v kup'
command -v kup
command_status=$?
echo "EXIT_STATUS $command_status (kup optional because an independent K install is present)"

echo 'COMMAND: kompile --version'
kompile --version
record_status $?
echo 'COMMAND: krun --version'
krun --version
record_status $?
echo 'COMMAND: kprove --version'
kprove --version
record_status $?

echo 'COMMAND: kompile --backend llvm semantic.k --main-module SEMANTIC --syntax-module SEMANTIC-SYNTAX --output-definition concrete-kompiled-final'
kompile --backend llvm "$audit_work/semantic.k" \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition "$audit_work/concrete-kompiled-final"
record_status $?

if [[ -d "$audit_work/concrete-kompiled-final" ]]; then
  echo 'COMMAND: concrete_semantics_compare.py --definition concrete-kompiled-final --program solution.mpy'
  python3 "$evidence/concrete_semantics_compare.py" \
    --definition "$audit_work/concrete-kompiled-final" \
    --program "$audit_work/solution.mpy" \
    --canonical "$audit_work/canonical.py" \
    --generated "$audit_work/solution.py"
  record_status $?
else
  echo 'SKIP concrete execution: concrete-kompiled-final was not built'
  status=1
fi

echo 'COMMAND: kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module SEMANTIC-SYNTAX --output-definition verification-kompiled-final'
kompile --backend haskell "$audit_work/verification.k" \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition "$audit_work/verification-kompiled-final"
record_status $?

if [[ -d "$audit_work/verification-kompiled-final" ]]; then
  echo 'COMMAND: kprove spec.k --definition verification-kompiled-final --spec-module SPEC'
  kprove "$audit_work/spec.k" \
    --definition "$audit_work/verification-kompiled-final" \
    --spec-module SPEC
  record_status $?

  echo 'COMMAND: label_positive_spec.py spec.k > spec-labeled.k'
  python3 "$evidence/label_positive_spec.py" "$audit_work/spec.k" \
    > "$audit_work/spec-labeled.k"
  command_status=$?
  record_status "$command_status"
  if (( command_status == 0 )); then
    cp "$audit_work/spec-labeled.k" "$evidence/spec-labeled.k"
    for label in nonnegative negative example-15 example-32 example-negative-5; do
      echo "COMMAND: kprove spec-labeled.k --definition verification-kompiled-final --spec-module SPEC-LABELED --claims SPEC-LABELED.$label"
      kprove "$audit_work/spec-labeled.k" \
        --definition "$audit_work/verification-kompiled-final" \
        --spec-module SPEC-LABELED \
        --claims "SPEC-LABELED.$label"
      record_status $?
    done
  fi
else
  echo 'SKIP proof execution: verification-kompiled-final was not built'
  status=1
fi

echo "SCRIPT_EXIT_STATUS $status"
exit "$status"
