#!/usr/bin/env bash
set -u

status=0
run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

printf 'STAGE 5 EXHAUSTIVE RULE/DECLARATION INVENTORY\n'
run python3 /audit-output/evidence/rule_inventory.py
run sha256sum /audit-output/evidence/rule-inventory.tsv \
  /audit-output/evidence/rule-inventory-summary.txt
run wc -l /audit-output/evidence/rule-inventory.tsv

printf '\nPROOF-LOCAL INVENTORY (EVERY ROW)\n'
run awk -F '\t' 'NR == 1 || $1 == "candidate-local" { print }' \
  /audit-output/evidence/rule-inventory.tsv

printf '\nUSED CONSTRUCT/RULE SURFACES\n'
run rg -n \
  'Module|#loadAll|FuncDef|closureVal|Call|#callee|#evalArgs|#applyK|#bindP|frame|#endcall|#pop|Assign|Name|#look|For|#loop|#iterNext|#iterYield|#iterDone|#loopStep|If|#branch|Compare|applyCmp|Continue|#cont|#loopLbl|Return|Bool|Int|Float|list[(]' \
  /reference/reference-semantics/semantics/syntax.k \
  /reference/reference-semantics/semantics/core.k \
  /reference/reference-semantics/semantics/functions.k \
  /reference/reference-semantics/semantics/call.k \
  /reference/reference-semantics/semantics/controls.k \
  /reference/reference-semantics/semantics/operators.k \
  /reference/reference-semantics/semantics/list.k \
  /reference/reference-semantics/semantics/int.k \
  /reference/reference-semantics/semantics/bool.k \
  /reference/reference-semantics/semantics/float.k \
  /candidate/base-verification.k /candidate/verification-loops.k \
  /candidate/verification.k /candidate/connection-spec.k \
  /candidate/loop-spec.k /candidate/spec.k

exit "$status"
