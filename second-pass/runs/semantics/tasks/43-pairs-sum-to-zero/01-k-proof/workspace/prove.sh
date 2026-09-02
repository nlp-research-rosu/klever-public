#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT_DIR"

# Translate the submitted source and the concrete K smoke program.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Required concrete LLVM definition and execution.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

# Base symbolic definition: no promoted reachability lemmas.
kompile verification.k \
  --backend haskell \
  --main-module PAIRS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Direct bounded symbolic executions against the reference semantics.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module PAIRS-SUMMARY-SPEC \
  --claims PAIRS-SUMMARY-SPEC.bounded-empty,PAIRS-SUMMARY-SPEC.bounded-one,PAIRS-SUMMARY-SPEC.bounded-two

# Prove membership by induction.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module PAIRS-SUMMARY-SPEC \
  --claims PAIRS-SUMMARY-SPEC.membership-summary

# Prove the loop invariant, using only the independently proved membership
# summary as a trusted lemma in this modular proof step.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module PAIRS-SUMMARY-SPEC \
  --claims PAIRS-SUMMARY-SPEC.membership-summary,PAIRS-SUMMARY-SPEC.loop-summary \
  --trusted PAIRS-SUMMARY-SPEC.membership-summary

# Promote the proved loop summary and compose the arbitrary-list theorem.
kompile verification.k \
  --backend haskell \
  --main-module PAIRS-VERIFICATION-LEMMAS \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-lemmas-kompiled
kprove spec.k \
  --definition verification-lemmas-kompiled \
  --spec-module PAIRS-MAIN-SPEC

# Negative validation: a deliberately wrong empty-list result must not prove.
MUTATION_FILE="$ROOT_DIR/mutation-spec.k"
trap 'rm -f -- "$MUTATION_FILE"' EXIT
sed '0,/=> false/s//=> true/' spec.k > "$MUTATION_FILE"
if kprove "$MUTATION_FILE" \
    --definition verification-kompiled \
    --spec-module PAIRS-SUMMARY-SPEC \
    --claims PAIRS-SUMMARY-SPEC.bounded-empty \
    --warnings none; then
  echo "ERROR: wrong-result mutation unexpectedly proved" >&2
  exit 1
fi
echo "Expected failure: wrong-result mutation was rejected."
