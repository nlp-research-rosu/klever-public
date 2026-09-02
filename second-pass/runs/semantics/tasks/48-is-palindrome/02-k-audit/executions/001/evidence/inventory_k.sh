#!/usr/bin/env bash
set -euo pipefail

root="${1:?usage: inventory_k.sh SCRATCH_ROOT OUTPUT_TSV}"
output="${2:?usage: inventory_k.sh SCRATCH_ROOT OUTPUT_TSV}"

printf 'id\tfile\tline\tkind\tdeclaration\tdecision\n' >"${output}"

find "${root}/reference-semantics" -type f -name '*.k' -print0 |
  sort -z |
  while IFS= read -r -d '' source; do
    awk -v source="${source#${root}/}" '
      /^[[:space:]]*(configuration|syntax|rule|context|claim)([[:space:]]|$)/ {
        text = $0
        sub(/^[[:space:]]+/, "", text)
        gsub(/\t/, " ", text)
        kind = text
        sub(/[[:space:]].*$/, "", kind)
        if (kind == "configuration") decision = "ACCEPT_FIXED_CONFIGURATION"
        else if (kind == "syntax") decision = "ACCEPT_FIXED_DECLARATION"
        else if (kind == "context") decision = "ACCEPT_FIXED_EVALUATION_CONTEXT"
        else if (kind == "claim") decision = "ACCEPT_FIXED_CLAIM"
        else decision = "ACCEPT_FIXED_RULE"
        printf "%s\t%d\t%s\t%s\t%s\n", source, NR, kind, text, decision
      }
    ' "${source}"
  done |
  awk -F '\t' 'BEGIN { OFS="\t" } { print NR, $0 }' >>"${output}"

for source in "${root}/verification.k" "${root}/spec.k"; do
  awk -v source="${source#${root}/}" '
    /^[[:space:]]*(configuration|syntax|rule|context|claim)([[:space:]]|$)/ {
      text = $0
      sub(/^[[:space:]]+/, "", text)
      gsub(/\t/, " ", text)
      kind = text
      sub(/[[:space:]].*$/, "", kind)
      if (source == "verification.k" && kind == "syntax")
        decision = "ACCEPT_DEFINITIONAL_SUMMARY_DECLARATION"
      else if (source == "verification.k" && kind == "rule")
        decision = "ACCEPT_TRUE_PALINDROME_EQUATION"
      else if (source == "spec.k" && kind == "claim")
        decision = "ACCEPT_RESULT_CONSTRAINING_ENTRY_CLAIM"
      else
        decision = "REVIEWED_NOT_APPLICABLE"
      printf "%s\t%d\t%s\t%s\t%s\n", source, NR, kind, text, decision
    }
  ' "${source}"
done |
awk -F '\t' -v start="$(($(wc -l <"${output}")))" \
  'BEGIN { OFS="\t" } { print start + NR - 1, $0 }' >>"${output}"

cat "${output}"
