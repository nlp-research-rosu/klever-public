#!/usr/bin/env bash
set -u

cd /tmp/audit-work/candidate || exit 97
overall=0

run_step() {
  local label="$1"
  shift
  echo "BEGIN $label"
  printf 'COMMAND'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local result=$?
  echo "EXIT $label $result"
  if [[ $result -ne 0 ]]; then
    overall=1
  fi
  echo "END $label"
}

run_step tool_versions kompile --version

run_step build_character \
  kompile verification.k \
    --backend haskell \
    --main-module STRONGEST-EXTENSION-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-verification-kompiled \
    -I .

run_step prove_character \
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module STRONGEST-EXTENSION-SPEC \
    --claims character-loop-correct \
    --output pretty

run_step build_strength \
  kompile verification.k \
    --backend haskell \
    --main-module STRONGEST-EXTENSION-WITH-CHAR-LOOP-LEMMA \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-char-loop-lemma-kompiled \
    -I .

run_step prove_strength \
  kprove spec.k \
    --definition audit-char-loop-lemma-kompiled \
    --spec-module STRONGEST-EXTENSION-SPEC \
    --claims extension-strength-correct \
    --output pretty

run_step build_selection \
  kompile verification.k \
    --backend haskell \
    --main-module STRONGEST-EXTENSION-WITH-STRENGTH-LEMMA \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-strength-lemma-kompiled \
    -I .

run_step prove_selection \
  kprove spec.k \
    --definition audit-strength-lemma-kompiled \
    --spec-module STRONGEST-EXTENSION-SPEC \
    --claims selection-loop-correct \
    --output pretty

run_step build_entry \
  kompile verification.k \
    --backend haskell \
    --main-module STRONGEST-EXTENSION-WITH-LOOP-LEMMAS \
    --syntax-module MPY-SYNTAX \
    --output-definition audit-loop-lemmas-kompiled \
    -I .

run_step prove_entry \
  kprove spec.k \
    --definition audit-loop-lemmas-kompiled \
    --spec-module STRONGEST-EXTENSION-SPEC \
    --claims strongest-extension-correct \
    --output pretty

echo "RECONSTRUCTION_OVERALL_EXIT=$overall"
exit "$overall"
