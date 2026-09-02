#!/usr/bin/env bash
set -u
set -x

export PATH="$HOME/.nix-profile/bin:$PATH"
work=/tmp/audit-work/fresh

kompile /audit-output/evidence/fixed-wrapper.k \
  --backend haskell \
  --main-module HOW-MANY-TIMES-FIXED-AUDIT \
  --syntax-module MPY-SYNTAX \
  --output-definition "$work/fixed-verification-kompiled"
fixed_build_rc=$?
echo "FIXED_BUILD_EXIT=$fixed_build_rc"

kprove /audit-output/evidence/spec-bridge-wrong-binding.k \
  --definition "$work/verification-kompiled" \
  --spec-module HOW-MANY-TIMES-BRIDGE-WRONG-BINDING-AUDIT
bridge_rc=$?
echo "BRIDGE_WRONG_BINDING_KPROVE_EXIT=$bridge_rc"

if test "$fixed_build_rc" -eq 0; then
  kprove /audit-output/evidence/spec-fixed-wrong-binding.k \
    --definition "$work/fixed-verification-kompiled" \
    --spec-module HOW-MANY-TIMES-FIXED-WRONG-BINDING-SPEC
  fixed_rc=$?
else
  fixed_rc=125
fi
echo "FIXED_WRONG_BINDING_KPROVE_EXIT=$fixed_rc"

# Required witness shape: the bridge proves 1, fixed semantics rejects 1.
if test "$fixed_build_rc" -eq 0 &&
   test "$bridge_rc" -eq 0 &&
   test "$fixed_rc" -ne 0
then
  exit 0
fi
exit 1
