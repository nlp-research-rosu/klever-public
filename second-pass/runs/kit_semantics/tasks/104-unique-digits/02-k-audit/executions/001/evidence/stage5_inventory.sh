#!/usr/bin/env bash
set -euo pipefail

root=/tmp/audit-work/candidate-src
semantics=$root/reference-semantics/semantics

printf 'LOCAL VERIFICATION DECLARATIONS AND RULE STARTS\n'
rg -n '^[[:space:]]+(syntax|rule|context|configuration)\b|^module |^endmodule' \
  "$root/verification.k"

printf '\nSPECIFICATION CLAIM STARTS\n'
rg -n '^[[:space:]]+claim\b|^module |^endmodule|^[[:space:]]+requires\b' \
  "$root/spec.k"

printf '\nLOCAL SPECIAL ATTRIBUTES\n'
rg -n '\[(function|total|functional|simplification|concrete|owise|priority|symbol|no-evaluators|macro)' \
  "$root/verification.k" "$root/spec.k" || true

printf '\nUSED SURFACE SYNTAX DECLARATIONS\n'
rg -n 'syntax (Expr|Stmt|Stmts|Params|Module)|\"(Int|Name|BinOp|ListExpr|TupleExpr|Call|Attribute|Compare|Assign|AugAssign|For|While|If|Return|Expr|FuncDef)\"' \
  "$semantics/syntax.k"

printf '\nUSED FIXED-SEMANTICS RULES AND ATTRIBUTES\n'
rg -n -F \
  -e '#loadAll' \
  -e 'Name(' \
  -e '#look' \
  -e '#evalArgs' \
  -e 'Int(' \
  -e 'truthy' \
  -e '#alloc' \
  -e 'Assign(' \
  -e 'AugAssign(' \
  -e '#branch' \
  -e 'For(' \
  -e '#loop(' \
  -e '#iterNext(list' \
  -e '#iterYield' \
  -e 'While(' \
  -e '#while(' \
  -e '#whileCond' \
  -e 'TupleExpr' \
  -e 'toTuple' \
  -e '#bindTgt(Name' \
  -e 'BinOp(' \
  -e 'Compare(' \
  -e 'applyBin("%"' \
  -e 'applyBin("+"' \
  -e 'applyBin("//"' \
  -e 'applyCmp("=="' \
  -e 'applyCmp(">"' \
  -e 'FuncDef(' \
  -e '#applyK(toCall(closureVal' \
  -e '#bindP' \
  -e 'Return(' \
  -e '#pop' \
  -e 'Call(' \
  -e '#callee' \
  -e 'builtinV("sum"' \
  -e '#sumAcc' \
  -e 'intOf' \
  -e 'Attribute(' \
  -e 'boundMethodV(ref(H:Int), "append"' \
  -e 'valSeqConcat' \
  -e 'builtinV("sorted"' \
  -e 'sortVS' \
  -e 'insVS' \
  "$semantics/core.k" \
  "$semantics/controls.k" \
  "$semantics/operators.k" \
  "$semantics/int.k" \
  "$semantics/list.k" \
  "$semantics/tuple.k" \
  "$semantics/call.k" \
  "$semantics/functions.k" \
  "$semantics/builtins.k" \
  "$semantics/sort.k"

printf '\nCANDIDATE-LOCAL OPERATIONAL BRIDGES\n'
if rg -n -F \
  -e '<k>' \
  -e '<heap>' \
  -e '<scopes>' \
  -e '[priority' \
  -e '[concrete' \
  -e '[simplification' \
  -e 'no-evaluators' \
  -e 'symbol(' \
  "$root/verification.k"
then
  :
else
  printf 'NONE\n'
fi

printf '\nINVENTORY_STATUS: COMPLETE\n'
