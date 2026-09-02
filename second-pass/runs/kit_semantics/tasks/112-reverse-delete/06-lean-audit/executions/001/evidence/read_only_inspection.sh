#!/bin/bash
set -euxo pipefail

env | rg '^AUDIT_MODE='
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
sed -n '1,120p' /reference/generation-tools/source-manifest.json
sed -n '1,120p' /reference/klean-generation/generator-manifest.json
nl -ba /reference/k-proof/verification.k
sed -n '1,180p' /reference/lemma-discovery.json
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/reference-semantics/semantics/str.k | sed -n '1,60p'
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k | sed -n '1,82p'
sed -n '1,160p' /reference/klean-generation/generated/obligation-map.json
nl -ba /reference/klean-generation/generated/Klean112ReverseDelete/Lemmas.lean
rg -n '^\s*def\s+targetStatement\b' /reference/klean-generation/generated -g '*.lean' || test "$?" -eq 1
test ! -e /candidate
