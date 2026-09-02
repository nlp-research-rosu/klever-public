#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/make_pinning_spec.py > /tmp/audit-work/source/pinning-spec.k'
python3 /audit-output/evidence/make_pinning_spec.py \
  > /tmp/audit-work/source/pinning-spec.k
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: kprove pinning-spec.k --definition verification-kompiled --spec-module REVIEWER-PINNING-SPEC --claims module_identity'
kprove \
  pinning-spec.k \
  --definition verification-kompiled \
  --spec-module REVIEWER-PINNING-SPEC \
  --claims module_identity
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: sed -n 1,120p pinning-spec.k'
sed -n '1,120p' pinning-spec.k
printf 'EXIT_STATUS: %s\n' "$?"
