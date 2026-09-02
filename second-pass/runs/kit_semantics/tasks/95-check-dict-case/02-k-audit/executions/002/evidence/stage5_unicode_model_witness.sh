#!/usr/bin/env bash
set -eu

audit_src=/tmp/audit-work/case95/candidate-src
audit_case=/tmp/audit-work/case95

cp \
  /audit-output/evidence/stage5_unicode_model_witness.py \
  "$audit_src/audit-unicode-witness.py"

python3 -c 'import runpy; ns=runpy.run_path("audit-unicode-witness.py"); print({k: ns[k] for k in sorted(ns) if k.endswith("_result")})'
python3 \
  /tmp/audit-work/case95/trusted/py2mpy.py \
  audit-unicode-witness.py \
  >"$audit_case/audit-unicode-witness.mpy"

export PATH="$HOME/.nix-profile/bin:$PATH"
set +e
krun \
  "$audit_case/audit-unicode-witness.mpy" \
  --definition audit-runtime-kompiled \
  >"$audit_case/unicode.fixed.out"
runtime_exit=$?
set -e
printf 'LLVM_UNICODE_RUNTIME_EXIT=%s\n' "$runtime_exit"
test "$runtime_exit" -ne 0

cp \
  /audit-output/evidence/stage5_unicode_model_spec.k \
  "$audit_src/audit-unicode-model-spec.k"
kprove \
  audit-unicode-model-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-UNICODE-MODEL-SPEC
