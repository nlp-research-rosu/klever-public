#!/usr/bin/env bash
set -euo pipefail
set -x

counterfactual=/tmp/audit-work/35-max-element-counterfactual
test ! -e "$counterfactual"
mkdir -p "$counterfactual/Base"
cp /candidate/Proof.lean /candidate/lakefile.lean /candidate/lean-toolchain "$counterfactual/"
cp -a /reference/klean-generation/generated/. "$counterfactual/Base/"

sed -i '461s/:= floatMaxImpl/:= fun _ _ => 0.0/' "$counterfactual/Proof.lean"
sed -i '463s/:= floatMaxImpl/:= fun _ _ => 0.0/' "$counterfactual/Proof.lean"
diff -u /candidate/Proof.lean "$counterfactual/Proof.lean" || test "$?" -eq 1

cd "$counterfactual"
export LD_PRELOAD=/tmp/audit-work/proc_pid_shim.so
lake clean
lake build
lake env lean /audit-output/evidence/PrintAxioms.lean
