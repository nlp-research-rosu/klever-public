#!/usr/bin/env bash
set -u
set -o pipefail

EVIDENCE=/audit-output/evidence
SCRATCH=/tmp/audit-work/reconstruction

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

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

run rm -rf "$SCRATCH"
run mkdir -p "$SCRATCH"
run cp -a /candidate/reference-semantics "$SCRATCH/reference-semantics"
run cp /candidate/solution.py "$SCRATCH/solution.py"
run cp /candidate/solution.mpy "$SCRATCH/solution.mpy"
run cp /candidate/spec.k "$SCRATCH/spec.k"
run cp /candidate/verification.k "$SCRATCH/verification.k"
run cp /audit-output/evidence/runtime_tests.py "$SCRATCH/runtime_tests.py"
run find "$SCRATCH" -name '*-kompiled' -o -name '.kompile-*' -o -name '__pycache__'
run cmp -s "$SCRATCH/solution.py" /candidate/solution.py
run cmp -s "$SCRATCH/solution.mpy" /candidate/solution.mpy

printf '\n$ python3 /reference/py2mpy.py %s > %s\n' \
  "$SCRATCH/runtime_tests.py" "$SCRATCH/runtime_tests.mpy"
python3 /reference/py2mpy.py "$SCRATCH/runtime_tests.py" \
  > "$SCRATCH/runtime_tests.mpy"
status=$?
printf '[exit %d]\n' "$status"

run python3 /audit-output/evidence/verify_runtime_prefix.py \
  "$SCRATCH/solution.py" "$SCRATCH/runtime_tests.py"

run_logged stage3_llvm_build \
  kompile "$SCRATCH/reference-semantics/semantics.k" \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/runtime-kompiled"

run_logged stage3_krun \
  krun "$SCRATCH/runtime_tests.mpy" \
  --definition "$SCRATCH/runtime-kompiled" \
  --output pretty

run_logged stage3_base_build \
  kompile "$SCRATCH/verification.k" \
  --backend haskell \
  --main-module STRONGEST-EXTENSION-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/verification-kompiled" \
  -I "$SCRATCH"

run_logged stage3_character_claim \
  kprove "$SCRATCH/spec.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module STRONGEST-EXTENSION-SPEC \
  --claims character-loop-correct \
  --output pretty

run_logged stage3_char_lemma_build \
  kompile "$SCRATCH/verification.k" \
  --backend haskell \
  --main-module STRONGEST-EXTENSION-WITH-CHAR-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/char-loop-lemma-kompiled" \
  -I "$SCRATCH"

run_logged stage3_strength_claim \
  kprove "$SCRATCH/spec.k" \
  --definition "$SCRATCH/char-loop-lemma-kompiled" \
  --spec-module STRONGEST-EXTENSION-SPEC \
  --claims extension-strength-correct \
  --output pretty

run_logged stage3_strength_lemma_build \
  kompile "$SCRATCH/verification.k" \
  --backend haskell \
  --main-module STRONGEST-EXTENSION-WITH-STRENGTH-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/strength-lemma-kompiled" \
  -I "$SCRATCH"

run_logged stage3_selection_claim \
  kprove "$SCRATCH/spec.k" \
  --definition "$SCRATCH/strength-lemma-kompiled" \
  --spec-module STRONGEST-EXTENSION-SPEC \
  --claims selection-loop-correct \
  --output pretty

run_logged stage3_loop_lemmas_build \
  kompile "$SCRATCH/verification.k" \
  --backend haskell \
  --main-module STRONGEST-EXTENSION-WITH-LOOP-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition "$SCRATCH/loop-lemmas-kompiled" \
  -I "$SCRATCH"

run_logged stage3_entry_claim \
  kprove "$SCRATCH/spec.k" \
  --definition "$SCRATCH/loop-lemmas-kompiled" \
  --spec-module STRONGEST-EXTENSION-SPEC \
  --claims strongest-extension-correct \
  --output pretty
