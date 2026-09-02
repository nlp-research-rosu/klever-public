#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
overall=0
cd "$work" || exit 125

run_step() {
  description=$1
  shift
  echo "COMMAND: $description"
  "$@"
  status=$?
  echo "EXIT_STATUS: $status"
  if (( status != 0 )); then
    overall=1
  fi
}

run_step 'kompile --version' kompile --version
run_step 'kprove --version' kprove --version
run_step 'krun --version' krun --version

echo 'COMMAND: python3 /reference/py2mpy.py /audit-output/evidence/03_k_concrete_tests.py > /tmp/audit-work/reconstruction/03_k_concrete_tests.mpy'
python3 /reference/py2mpy.py /audit-output/evidence/03_k_concrete_tests.py > "$work/03_k_concrete_tests.mpy"
status=$?
echo "EXIT_STATUS: $status"
if (( status != 0 )); then overall=1; fi

run_step \
  'kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled' \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-runtime-kompiled

run_step \
  'krun 03_k_concrete_tests.mpy --definition audit-runtime-kompiled --output pretty' \
  krun 03_k_concrete_tests.mpy \
    --definition audit-runtime-kompiled \
    --output pretty

run_step \
  'kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled -I .' \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-kompiled \
    -I .

for label in residue-0 residue-1 residue-2 get-max-triples-correct; do
  run_step \
    "kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.$label -I . --output pretty" \
    kprove spec.k \
      --definition audit-verification-kompiled \
      --spec-module SPEC \
      --claims "SPEC.$label" \
      -I . \
      --output pretty
done

exit "$overall"
