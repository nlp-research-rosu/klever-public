#!/usr/bin/env bash
set -u

printf '%s\n' 'CANDIDATE TOP-LEVEL K FILE MANIFEST'
find /candidate -maxdepth 1 -type f -name '*.k' -print0 \
  | sort -z \
  | xargs -0 -r sha256sum

printf '%s\n' 'POSITIVE THEORY: FULL NUMBERED SOURCES'
for file in /candidate/verification.k /candidate/spec.k /candidate/connection-spec.k; do
  printf 'FILE %s\n' "$file"
  nl -ba "$file"
done

printf '%s\n' 'ALL CANDIDATE-LOCAL K DECLARATION/RULE/CLAIM STARTS'
rg -n \
  '^[[:space:]]*(syntax|configuration|context|rule|claim|module|endmodule|imports|requires)' \
  /candidate/*.k

printf '%s\n' 'ALL CANDIDATE-LOCAL SEMANTIC ATTRIBUTES'
rg -n \
  '\\[(function|functional|total|symbol|no-evaluators|priority|simplification|concrete|owise|strict|seqstrict)' \
  /candidate/*.k || true

printf '%s\n' 'SUPPLIED SEMANTICS DECLARATION/RULE/CONTEXT COUNTS BY FILE'
for file in /reference/reference-semantics/semantics.k \
            /reference/reference-semantics/semantics/*.k; do
  syntax_count=$(rg -c '^[[:space:]]*syntax[[:space:]]' "$file" || true)
  rule_count=$(rg -c '^[[:space:]]*rule[[:space:]]' "$file" || true)
  context_count=$(rg -c '^[[:space:]]*context[[:space:]]' "$file" || true)
  config_count=$(rg -c '^[[:space:]]*configuration([[:space:]]|$)' "$file" || true)
  printf '%s syntax=%s rule=%s context=%s configuration=%s\n' \
    "$file" "${syntax_count:-0}" "${rule_count:-0}" \
    "${context_count:-0}" "${config_count:-0}"
done

printf '%s\n' 'SUPPLIED SEMANTICS: COMPLETE RULE/CONTEXT/CONFIGURATION START INVENTORY'
rg -n \
  '^[[:space:]]*(configuration([[:space:]]|$)|context[[:space:]]|rule[[:space:]])' \
  /reference/reference-semantics/semantics.k \
  /reference/reference-semantics/semantics/*.k

printf '%s\n' 'SOLUTION CONSTRUCT EXECUTION-SLICE LOCATIONS'
rg -n \
  'syntax (Expr|Stmt|Stmts|Module|Params)|#loadAll|FuncDef|Assign\(|Name\(|ListExpr|For\(|#loop\(|#loopStep|#iterNext\(list|#iterYield|While\(|#while\(|Compare\(|BinOp\(|applyBin\("%"|applyBin\("//"|applyCmp\(">"|applyCmp\("=="|#branch|Call\(|#callee|#evalArgs|Attribute\(|append"|"sort"|Return\(|#pop|sortVS' \
  /reference/reference-semantics/semantics/syntax.k \
  /reference/reference-semantics/semantics/core.k \
  /reference/reference-semantics/semantics/list.k \
  /reference/reference-semantics/semantics/controls.k \
  /reference/reference-semantics/semantics/functions.k \
  /reference/reference-semantics/semantics/call.k \
  /reference/reference-semantics/semantics/operators.k \
  /reference/reference-semantics/semantics/int.k \
  /reference/reference-semantics/semantics/sort.k \
  /reference/reference-semantics/semantics/tuple.k
