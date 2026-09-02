#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/26-remove-duplicates/candidate
inventory=/audit-output/evidence/06-rule-inventory.txt
numbered=/audit-output/evidence/06-full-numbered-k-sources.txt

mapfile -t files < <(
  {
    printf '%s\n' "$scratch/reference-semantics/semantics.k"
    find "$scratch/reference-semantics/semantics" -maxdepth 1 -type f -name '*.k' -print
    printf '%s\n' "$scratch/verification.k" "$scratch/spec.k"
  } | sort
)

awk '
  function kind(line) {
    if (line ~ /^requires[[:space:]]/) return "requires-file"
    if (line ~ /^[[:space:]]*module[[:space:]]/) return "module"
    if (line ~ /^[[:space:]]*imports[[:space:]]/) return "import"
    if (line ~ /^[[:space:]]*configuration([[:space:]]|$)/) return "configuration"
    if (line ~ /^[[:space:]]*syntax[[:space:]]+priority([[:space:]]|$)/) return "syntax-priority"
    if (line ~ /^[[:space:]]*syntax[[:space:]]/) return "syntax"
    if (line ~ /^[[:space:]]*context[[:space:]]+alias([[:space:]]|$)/) return "context-alias"
    if (line ~ /^[[:space:]]*context([[:space:]]|$)/) return "context"
    if (line ~ /^[[:space:]]*rule([[:space:]]|$)/) return "rule"
    if (line ~ /^[[:space:]]*claim([[:space:]]|$)/) return "claim"
    if (line ~ /^[[:space:]]*endmodule([[:space:]]|$)/) return "endmodule"
    return ""
  }
  {
    k = kind($0)
    if (k != "") {
      counts[k]++
      printf "%s:%d\t%s\t%s\n", FILENAME, FNR, k, $0
    }
    if ($0 ~ /\[/ &&
        ($0 ~ /function/ || $0 ~ /functional/ || $0 ~ /total/ ||
         $0 ~ /macro/ || $0 ~ /simplification/ || $0 ~ /priority/ ||
         $0 ~ /owise/ || $0 ~ /no-evaluators/ || $0 ~ /symbol/)) {
      attr_count++
      printf "%s:%d\tattribute\t%s\n", FILENAME, FNR, $0
    }
    if ($0 ~ /[[:space:]]requires[[:space:]]/ && $0 !~ /^[[:space:]]*requires[[:space:]]/) {
      guard_count++
      printf "%s:%d\tguard-inline\t%s\n", FILENAME, FNR, $0
    } else if ($0 ~ /^[[:space:]]*requires[[:space:]]/) {
      guard_count++
      printf "%s:%d\tguard\t%s\n", FILENAME, FNR, $0
    }
  }
  END {
    print "== COUNTS =="
    for (k in counts) printf "%s=%d\n", k, counts[k]
    printf "attribute_lines=%d\n", attr_count
    printf "guard_lines=%d\n", guard_count
  }
' "${files[@]}" > "$inventory"

{
  for file in "${files[@]}"; do
    printf '===== %s =====\n' "$file"
    nl -ba "$file"
  done
} > "$numbered"

printf 'inventory=%s\n' "$inventory"
printf 'numbered_sources=%s\n' "$numbered"
wc -l "$inventory" "$numbered"
