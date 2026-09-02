#!/usr/bin/env bash
set -u
set -o pipefail
set -x

reconstruction=/tmp/audit-work/reconstruction
no_bridge=/tmp/audit-work/no-bridge

python3 -c 'import importlib.util; load=lambda n,p:(lambda s:(lambda m:(s.loader.exec_module(m),m)[1])(importlib.util.module_from_spec(s)))(importlib.util.spec_from_file_location(n,p)); c=load("canonical","/reference/canonical.py"); g=load("generated","/tmp/audit-work/reconstruction/solution.py"); print("canonical(o) =",c.parse_music("o")); print("generated(o) =",g.parse_music("o"))'
python_status=$?
printf 'ground Python comparison exit: %d\n' "$python_status"

krun /audit-output/evidence/ground-o.mpy \
  --definition "$reconstruction/runtime-kompiled"
ground_krun_status=$?
printf 'fixed-semantics ground-o krun exit: %d\n' "$ground_krun_status"

mkdir -p "$no_bridge"
cp -a /reference/reference-semantics "$no_bridge/reference-semantics"
cp /candidate/spec.k "$no_bridge/spec.k"
cp /audit-output/evidence/verification-no-split-bridge.k "$no_bridge/verification.k"
cd "$no_bridge" || exit 90

kompile verification.k \
  --backend haskell \
  --main-module PARSE-MUSIC-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-no-bridge-kompiled
no_bridge_build_status=$?
printf 'no-bridge kompile exit: %d\n' "$no_bridge_build_status"

if test "$no_bridge_build_status" -eq 0; then
  kprove spec.k \
    --definition verification-no-bridge-kompiled \
    --spec-module PARSE-MUSIC-ENTRY-SPEC \
    --branching-allowed 100
  no_bridge_proof_status=$?
else
  no_bridge_proof_status=125
fi
printf 'no-bridge entry kprove exit (nonzero expected): %d\n' "$no_bridge_proof_status"

if test "$python_status" -ne 0 \
  || test "$ground_krun_status" -ne 0 \
  || test "$no_bridge_build_status" -ne 0; then
  exit 1
fi
if test "$no_bridge_proof_status" -eq 0; then
  exit 2
fi
exit 0
