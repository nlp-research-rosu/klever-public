#!/usr/bin/env bash
set -u

audit_k_dir=/tmp/audit-work/k-stage1-classification
printf '%s\n' 'COMMAND: fresh-copy Stage 1, compile VERIFICATION-BASE, prove loop-correct, compile VERIFICATION, prove intersection-correct'
printf 'WORKDIR=%s\n' "$audit_k_dir"
if test -e "$audit_k_dir"; then
  printf '%s\n' 'ERROR: fresh audit directory already exists'
  exit 97
fi
mkdir -p "$audit_k_dir"
cp -a /reference/k-proof/. "$audit_k_dir/"
cd "$audit_k_dir" || exit 98

printf '\n[kompile VERIFICATION-BASE]\n'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
command_code=$?
printf 'EXIT_CODE=%s\n' "$command_code"
if test "$command_code" -ne 0; then exit "$command_code"; fi

printf '\n[kprove LOOP-SPEC.loop-correct against VERIFICATION-BASE]\n'
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC \
  --claims loop-correct \
  --output pretty
command_code=$?
printf 'EXIT_CODE=%s\n' "$command_code"
if test "$command_code" -ne 0; then exit "$command_code"; fi

printf '\n[kompile VERIFICATION]\n'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
command_code=$?
printf 'EXIT_CODE=%s\n' "$command_code"
if test "$command_code" -ne 0; then exit "$command_code"; fi

printf '\n[kprove SPEC.intersection-correct against VERIFICATION]\n'
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims intersection-correct \
  --output pretty
command_code=$?
printf 'EXIT_CODE=%s\n' "$command_code"
exit "$command_code"
