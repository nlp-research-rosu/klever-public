#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 99

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n\n' "$rc"
}

printf '## Task-specific symbol isolation\n'
run rg -n 'sum_to_n|triangular|runSumToN' reference-semantics verification.k spec.k

printf '## All K claims in the audited source set\n'
run rg -n '^[[:space:]]*claim\b' reference-semantics verification.k spec.k

printf '## Opaque, concrete-only, totality, priority, and fallback inventory\n'
run rg -n -i 'no-evaluators|opaque|trusted|oracle|\[concrete\]|\[priority|\[owise|\[macro|\[function|\[functional|\[total' \
  reference-semantics/semantics.k reference-semantics/semantics verification.k spec.k

printf '## Declarations and rules needed by solution.mpy\n'
run rg -n \
  -e 'syntax (Module|Stmt|Stmts|Expr|Val|KItem)' \
  -e '#loadAll|FuncDef\(|Return\(|Name\(|Int\(|BinOp\(|Call\(' \
  -e '#callee|#evalArgs|#applyK\(toCall\(closureVal|#bindP|#pop' \
  -e 'applyBin\("(\+|\*|//)"|pyMod' \
  reference-semantics/semantics/syntax.k \
  reference-semantics/semantics/core.k \
  reference-semantics/semantics/operators.k \
  reference-semantics/semantics/int.k \
  reference-semantics/semantics/functions.k \
  reference-semantics/semantics/call.k \
  verification.k spec.k

printf '## Source line and declaration counts\n'
run wc -l reference-semantics/semantics.k reference-semantics/semantics/*.k verification.k spec.k
run bash -c 'for f in reference-semantics/semantics.k reference-semantics/semantics/*.k verification.k spec.k; do printf "%s " "$f"; rg -c "^[[:space:]]*(syntax|rule|claim|configuration|context|alias)\\b" "$f"; done'
