#!/usr/bin/env bash
set -uo pipefail
cd /tmp/audit-work/46-fib4-review || exit 99

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/build_rule_inventory.py
run wc -l -c /audit-output/evidence/rule-inventory.md
run rg -n '^\\s*(syntax|rule|claim|context|configuration)\\b' verification.k
run rg -n -F \
  -e 'symbol(' \
  -e 'no-evaluators' \
  -e '[simplification' \
  -e '[functional' \
  reference-semantics verification.k
run rg -n 'fib4' reference-semantics verification.k
run rg -n -F \
  -e 'syntax Expr' \
  -e 'syntax Stmt' \
  -e 'syntax Stmts' \
  -e 'syntax Params' \
  -e 'syntax Module' \
  -e '#loadAll' \
  -e 'FuncDef' \
  -e 'Name(' \
  -e 'Assign(' \
  -e 'If(' \
  -e 'While(' \
  -e 'Call(' \
  -e 'Return(' \
  -e 'BinOp(' \
  -e 'Compare(' \
  -e 'Assert(' \
  reference-semantics/semantics/{syntax,core,functions,call,controls,operators,int,assert}.k

run python3 /audit-output/evidence/make_body_mutation.py
run timeout 900 kprove spec-body-mutation.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC-BODY-MUTATION \
  --claims FIB4-SPEC-BODY-MUTATION.operational-cases \
  --output pretty
