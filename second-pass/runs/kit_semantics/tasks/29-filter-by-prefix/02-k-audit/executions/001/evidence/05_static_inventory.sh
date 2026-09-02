#!/usr/bin/env bash
set -u

cd /tmp/audit-work/work || exit 1
echo 'COMMAND: bash /audit-output/evidence/05_static_inventory.sh'

echo
echo '== Candidate-local declarations/rules/claims in the positive proof closure =='
for file in domain.k verification-core.k verification.k connection-spec.k loop-connection-spec.k spec.k
do
  echo "FILE $file"
  nl -ba "$file"
done

echo
echo '== Indexed candidate-local declaration starts =='
rg -n \
  '^[[:space:]]*(syntax|configuration|context|rule|claim|alias|macro|module|imports|requires)\\b|\\[(function|total|functional|simplification|concrete|priority|owise|macro)' \
  domain.k verification-core.k verification.k connection-spec.k loop-connection-spec.k spec.k

echo
echo '== Source AST constructors actually submitted =='
rg -o \
  'Module|ImportFrom|FuncDef|Params|Assign|Name|ListExpr|Str|For|If|Call|Attribute|Expr|Return' \
  solution.mpy |
  sort |
  uniq -c

echo
echo '== Relevant fixed-semantics rule/declaration excerpts =='
for span in \
  'reference-semantics/semantics/syntax.k:9:61' \
  'reference-semantics/semantics/core.k:12:60' \
  'reference-semantics/semantics/core.k:117:154' \
  'reference-semantics/semantics/core.k:183:229' \
  'reference-semantics/semantics/controls.k:8:75' \
  'reference-semantics/semantics/functions.k:8:16' \
  'reference-semantics/semantics/functions.k:62:90' \
  'reference-semantics/semantics/call.k:15:24' \
  'reference-semantics/semantics/call.k:69:75' \
  'reference-semantics/semantics/list.k:8:20' \
  'reference-semantics/semantics/list.k:52:55' \
  'reference-semantics/semantics/tuple.k:30:41' \
  'reference-semantics/semantics/str.k:7:22' \
  'reference-semantics/semantics/methods.k:60:62' \
  'reference-semantics/semantics/methods.k:166:170'
do
  file="${span%%:*}"
  rest="${span#*:}"
  start="${rest%%:*}"
  end="${rest##*:}"
  echo "SPAN $file:$start-$end"
  nl -ba "$file" | sed -n "${start},${end}p"
done

echo
echo 'SCRIPT_EXIT: 0'
