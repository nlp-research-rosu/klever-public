#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

cd /tmp/audit-work/candidate

test ! -e auditor-runtime-kompiled
printf 'fresh_runtime_dir_check_exit=%s\n' "$?"
test ! -e auditor-verification-kompiled
printf 'fresh_verification_dir_check_exit=%s\n' "$?"

python3 /reference/py2mpy.py auditor-smoke.py > auditor-smoke.mpy
printf 'auditor_smoke_translate_exit=%s\n' "$?"

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition auditor-runtime-kompiled
printf 'llvm_kompile_exit=%s\n' "$?"

krun auditor-smoke.mpy --definition auditor-runtime-kompiled
printf 'llvm_krun_smoke_exit=%s\n' "$?"

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition auditor-verification-kompiled
printf 'haskell_kompile_exit=%s\n' "$?"

