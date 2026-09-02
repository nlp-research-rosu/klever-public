#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction

printf 'tool_versions_begin\n'
kompile --version
kprove --version
krun --version
printf 'tool_versions_end\n'

printf 'COMMAND: python3 /reference/py2mpy.py smoke.py > regenerated-smoke.mpy\n'
python3 /reference/py2mpy.py smoke.py > regenerated-smoke.mpy
status=$?
printf 'EXIT: %s\n' "$status"
if [ "$status" -ne 0 ]; then exit "$status"; fi
cmp -s smoke.mpy regenerated-smoke.mpy
status=$?
printf 'smoke_mpy_byte_identity_exit=%s\n' "$status"
if [ "$status" -ne 0 ]; then exit "$status"; fi

printf '%s\n' 'COMMAND: kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled'
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
status=$?
printf 'EXIT: %s\n' "$status"
if [ "$status" -ne 0 ]; then exit "$status"; fi

printf '%s\n' 'COMMAND: krun regenerated-smoke.mpy --definition audit-runtime-kompiled'
krun regenerated-smoke.mpy --definition audit-runtime-kompiled
status=$?
printf 'EXIT: %s\n' "$status"
if [ "$status" -ne 0 ]; then exit "$status"; fi

printf '%s\n' 'COMMAND: kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled'
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
status=$?
printf 'EXIT: %s\n' "$status"
if [ "$status" -ne 0 ]; then exit "$status"; fi

printf '%s\n' 'COMMAND: kprove spec.k --definition audit-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
status=$?
printf 'EXIT: %s\n' "$status"
if [ "$status" -ne 0 ]; then exit "$status"; fi

printf '%s\n' 'COMMAND: kprove summary-test.k --definition audit-verification-kompiled --spec-module SUMMARY-TEST'
kprove summary-test.k \
  --definition audit-verification-kompiled \
  --spec-module SUMMARY-TEST
status=$?
printf 'EXIT: %s\n' "$status"
exit "$status"
