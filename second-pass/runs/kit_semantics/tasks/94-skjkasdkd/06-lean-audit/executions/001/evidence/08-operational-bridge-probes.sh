#!/usr/bin/env bash
set -uo pipefail
set -x

cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean-app-path-shim.so \
  /audit-output/evidence/lean-app-path-shim.c
export LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so
export PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH

rg -n -F "hook{}(\"INT.tmod\")" \
  /reference/k-proof/verification-kompiled/definition.kore
rg -n -F 'rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)' \
  /reference/k-proof/reference-semantics/semantics/float.k

k_probe_dir="$(mktemp -d /tmp/audit-work/k-bridge-probe.XXXXXX)"
kompile --backend llvm /tmp/audit-work/int-probe.k \
  --main-module INT-PROBE \
  --syntax-module INT-PROBE \
  --output-definition "$k_probe_dir/int-probe-kompiled"
krun --definition "$k_probe_dir/int-probe-kompiled" --output pretty \
  /tmp/audit-work/int-probe-negative-dividend.in
krun --definition "$k_probe_dir/int-probe-kompiled" --output pretty \
  /tmp/audit-work/int-probe-negative-divisor.in

lean_probe_dir="$(mktemp -d /tmp/audit-work/lean-bridge-probe.XXXXXX)"
cp -a /candidate/. "$lean_probe_dir/"
cp -a /reference/klean-generation/generated/. "$lean_probe_dir/Base/"
cp /audit-output/evidence/BridgeProbe.lean "$lean_probe_dir/BridgeProbe.lean"
cd "$lean_probe_dir"
lake clean
lake build
lake env lean BridgeProbe.lean

counterfactual_dir="$(
  mktemp -d /tmp/audit-work/lean-counterfactual.XXXXXX
)"
cp -a /candidate/. "$counterfactual_dir/"
cp -a /reference/klean-generation/generated/. "$counterfactual_dir/Base/"
cp /audit-output/evidence/Proof-counterfactual.lean \
  "$counterfactual_dir/Proof.lean"
cp /audit-output/evidence/CounterfactualProbe.lean \
  "$counterfactual_dir/CounterfactualProbe.lean"
cd "$counterfactual_dir"
lake clean
lake build
lake env lean CounterfactualProbe.lean
