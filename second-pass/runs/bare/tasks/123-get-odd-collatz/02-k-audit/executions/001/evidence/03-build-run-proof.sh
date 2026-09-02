#!/usr/bin/env bash
set -o pipefail

cd /tmp/audit-work/candidate-src || exit 90

echo 'COMMAND: kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --backend llvm --output-definition /tmp/audit-work/semantic-kompiled-audit'
kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition /tmp/audit-work/semantic-kompiled-audit
semantic_build_rc=$?
echo "EXIT: $semantic_build_rc"
if (( semantic_build_rc != 0 )); then
  exit "$semantic_build_rc"
fi

echo 'COMMAND: python3 /audit-output/evidence/03-concrete-oracle.py'
python3 /audit-output/evidence/03-concrete-oracle.py
oracle_rc=$?
echo "EXIT: $oracle_rc"

concrete_rc=0
for n in 1 2 3 5 27; do
  echo "COMMAND: krun solution.mpy -cN=$n --definition /tmp/audit-work/semantic-kompiled-audit --output pretty"
  krun solution.mpy \
    -cN="$n" \
    --definition /tmp/audit-work/semantic-kompiled-audit \
    --output pretty
  this_rc=$?
  echo "EXIT: $this_rc"
  if (( this_rc != 0 )); then
    concrete_rc=$this_rc
  fi
done
if (( oracle_rc != 0 || concrete_rc != 0 )); then
  exit 91
fi

echo 'COMMAND: kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition /tmp/audit-work/verification-kompiled-audit'
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition /tmp/audit-work/verification-kompiled-audit
proof_build_rc=$?
echo "EXIT: $proof_build_rc"
if (( proof_build_rc != 0 )); then
  exit "$proof_build_rc"
fi

echo 'COMMAND: kprove spec.k --definition /tmp/audit-work/verification-kompiled-audit --spec-module SPEC --output pretty'
kprove spec.k \
  --definition /tmp/audit-work/verification-kompiled-audit \
  --spec-module SPEC \
  --output pretty
all_proof_rc=$?
echo "EXIT: $all_proof_rc"

echo 'COMMAND: kprove spec.k --definition /tmp/audit-work/verification-kompiled-audit --spec-module SPEC --claims SPEC.even-step --output pretty'
kprove spec.k \
  --definition /tmp/audit-work/verification-kompiled-audit \
  --spec-module SPEC \
  --claims SPEC.even-step \
  --output pretty
even_proof_rc=$?
echo "EXIT: $even_proof_rc"

echo 'COMMAND: kprove spec.k --definition /tmp/audit-work/verification-kompiled-audit --spec-module SPEC --claims SPEC.odd-step --output pretty'
kprove spec.k \
  --definition /tmp/audit-work/verification-kompiled-audit \
  --spec-module SPEC \
  --claims SPEC.odd-step \
  --output pretty
odd_proof_rc=$?
echo "EXIT: $odd_proof_rc"

if (( all_proof_rc != 0 || even_proof_rc != 0 || odd_proof_rc != 0 )); then
  exit 92
fi
