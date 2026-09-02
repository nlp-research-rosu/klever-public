#!/usr/bin/env bash
set -euo pipefail

echo '$ nl -ba /reference/k-proof/verification.k'
nl -ba /reference/k-proof/verification.k

echo '$ nl -ba /reference/k-proof/solution.py'
nl -ba /reference/k-proof/solution.py

echo '$ nl -ba /reference/k-proof/solution.mpy'
nl -ba /reference/k-proof/solution.mpy

echo '$ nl -ba /reference/k-proof/spec.k'
nl -ba /reference/k-proof/spec.k

echo '$ nl -ba functions.k | sed -n 13,20p; sed -n 62,90p'
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k |
    sed -n -e '13,20p' -e '62,90p'

echo '$ nl -ba call.k | sed -n 18,21p; sed -n 69,75p'
nl -ba /reference/k-proof/reference-semantics/semantics/call.k |
    sed -n -e '18,21p' -e '69,75p'

echo '$ nl -ba core.k | sed -n 123,154p; sed -n 183,220p'
nl -ba /reference/k-proof/reference-semantics/semantics/core.k |
    sed -n -e '123,154p' -e '183,220p'

echo '$ nl -ba controls.k | sed -n 50,54p'
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k |
    sed -n '50,54p'

echo '$ nl -ba operators.k | sed -n 10,17p'
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k |
    sed -n '10,17p'

echo '$ nl -ba int.k | sed -n 7,27p'
nl -ba /reference/k-proof/reference-semantics/semantics/int.k |
    sed -n '7,27p'

echo '$ nl -ba list.k | sed -n 12,15p'
nl -ba /reference/k-proof/reference-semantics/semantics/list.k |
    sed -n '12,15p'

echo '$ sed -n 1,160p obligation-map.json'
sed -n '1,160p' /reference/klean-generation/generated/obligation-map.json

echo '$ sed -n 1,180p generator-manifest.json'
sed -n '1,180p' /reference/klean-generation/generator-manifest.json
