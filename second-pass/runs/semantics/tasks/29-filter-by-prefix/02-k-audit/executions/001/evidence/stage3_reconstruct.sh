#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/29-filter-by-prefix/candidate-src
evidence=/audit-output/evidence
status=0
export PATH="/home/agent/.nix-profile/bin:$PATH"

printf '%s\n' 'COMMAND: python3 ../trusted/py2mpy.py /audit-output/evidence/reviewer-concrete.py > reviewer-concrete.mpy'
python3 ../trusted/py2mpy.py \
  "$evidence/reviewer-concrete.py" \
  > reviewer-concrete.mpy
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: krun reviewer-concrete.mpy --definition runtime-kompiled --output pretty'
krun reviewer-concrete.mpy \
  --definition runtime-kompiled \
  --output pretty
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kprove spec.k --definition verification-kompiled --spec-module FILTER-BY-PREFIX-SPEC'
kprove spec.k \
  --definition verification-kompiled \
  --spec-module FILTER-BY-PREFIX-SPEC
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kprove /audit-output/evidence/spec-loop-only.k --definition verification-kompiled --spec-module FILTER-BY-PREFIX-LOOP-ONLY-SPEC'
kprove "$evidence/spec-loop-only.k" \
  --definition verification-kompiled \
  --spec-module FILTER-BY-PREFIX-LOOP-ONLY-SPEC
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kprove /audit-output/evidence/spec-entry-only.k --definition verification-kompiled --spec-module FILTER-BY-PREFIX-ENTRY-ONLY-SPEC'
kprove "$evidence/spec-entry-only.k" \
  --definition verification-kompiled \
  --spec-module FILTER-BY-PREFIX-ENTRY-ONLY-SPEC
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
