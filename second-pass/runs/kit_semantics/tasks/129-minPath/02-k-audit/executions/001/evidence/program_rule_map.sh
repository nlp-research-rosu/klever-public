#!/usr/bin/env bash
set -eu

cd /tmp/audit-work/129-minPath-audit

printf '%s\n' 'PROGRAM CONSTRUCTORS'
rg -o '(^|[^A-Za-z#])[A-Z][A-Za-z]*\(' solution.mpy \
  | sed -E 's/.*[^A-Za-z#]([A-Z][A-Za-z]*)\(.*/\1/' | sort -u

printf '%s\n' 'SYNTAX DECLARATIONS'
rg -n 'syntax (Expr|Stmt|Stmts|Module|Params|CmpOp|Index)|"(Int|Name|BinOp|Compare|CmpOp|Subscript|Assign|While|If|Return|Expr|FuncDef|Module|Params|ListExpr|Call|Attribute)"' \
  reference-semantics/semantics/syntax.k

printf '%s\n' 'USED OPERATIONAL RULES'
rg -n '#loadAll\(Module|FuncDef\(|Assign\(Name|Name\(X|Call\(|#callee|#evalArgs|#applyK\(toCall\(closureVal|Int\(I|While\(|#while|If\(|#branch|BinOp\(|Compare\(|Subscript\(|applyIndex\(list|ListExpr\(|toList|append|Return\(|#pop|seqLen\(list|applyBuiltin\("len"' \
  reference-semantics/semantics/core.k \
  reference-semantics/semantics/functions.k \
  reference-semantics/semantics/call.k \
  reference-semantics/semantics/controls.k \
  reference-semantics/semantics/operators.k \
  reference-semantics/semantics/int.k \
  reference-semantics/semantics/list.k \
  reference-semantics/semantics/subscript.k \
  reference-semantics/semantics/builtins.k

printf '%s\n' 'PROOF EXTENSION TRUST/BRIDGE CHECK'
rg -n '\[trusted\]|<k>|<heap>|<scopes>|rule .*Call\(|rule .*While\(|rule .*Return\(' verification.k || true

printf '%s\n' 'ADMITTED FIXED-SYMBOL SIMPLIFICATIONS'
rg -n -A8 'rule vsLen\(gridRows|rule valSeqAt\(gridRows|rule valSeqAt\(gridRow|rule \(gridAt.*==Int 1|rule \(gridAt.*<Int' verification.k

printf '%s\n' 'ALL CLAIM LABELS'
rg -n '^  claim' spec.k verification.k
