#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

printf 'COMMAND: show frozen source, translated source, verification rules, and target claims\n'
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k

printf '\nCOMMAND: show supplied operational rules used by the loop proof\n'
sed -n '1,112p' /reference/k-proof/reference-semantics/semantics/controls.k
sed -n '1,55p' /reference/k-proof/reference-semantics/semantics/str.k
sed -n '1,45p' /reference/k-proof/reference-semantics/semantics/operators.k
sed -n '1,35p' /reference/k-proof/reference-semantics/semantics/int.k
sed -n '1,50p' /reference/k-proof/reference-semantics/semantics/bool.k
sed -n '1,125p' /reference/k-proof/reference-semantics/semantics/call.k
sed -n '60,120p' /reference/k-proof/reference-semantics/semantics/functions.k
