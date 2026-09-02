#!/usr/bin/env bash
set -euo pipefail

root=/tmp/audit-work/52-below-threshold/bridge-mutation
mkdir -p "$root"
cp -a /tmp/audit-work/52-below-threshold/reference-semantics "$root/reference-semantics"
cp /audit-output/evidence/bridge-mutated-verification.k "$root/verification.k"
cp /candidate/spec.k "$root/spec.k"
sha256sum "$root/verification.k" "$root/spec.k"
rg -n -F '#iterYield(I' "$root/verification.k"
