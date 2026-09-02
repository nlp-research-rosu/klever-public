#!/usr/bin/env bash
set -euo pipefail

root=${1:-/tmp/audit-work/reconstruction}
mapfile -t files < <(
  {
    printf '%s\n' "$root/reference-semantics/semantics.k"
    find "$root/reference-semantics/semantics" -maxdepth 1 -type f -name '*.k' -print
    printf '%s\n' "$root/verification.k" "$root/spec.k"
  } | sort
)

printf 'INVENTORY_ROOT %s\n' "$root"
printf 'SOURCE_FILE_COUNT %d\n' "${#files[@]}"
for file in "${files[@]}"; do
  rel=${file#"$root/"}
  printf '\nSOURCE %s\n' "$rel"
  sha256sum "$file"
  awk '
    /^[[:space:]]*(configuration|syntax|context|rule|claim|alias)([[:space:]]|$)/ {
      kind=$1
      count[kind]++
      line=$0
      sub(/^[[:space:]]+/, "", line)
      printf "DECL\t%d\t%s\n", NR, line
    }
    END {
      printf "COUNTS"
      printf "\tconfiguration=%d", count["configuration"] + 0
      printf "\tsyntax=%d", count["syntax"] + 0
      printf "\tcontext=%d", count["context"] + 0
      printf "\trule=%d", count["rule"] + 0
      printf "\tclaim=%d", count["claim"] + 0
      printf "\talias=%d\n", count["alias"] + 0
    }
  ' "$file"
  rg -n \
    'function|functional|total|symbol|no-evaluators|priority\(|simplification|concrete|owise|strict|macro' \
    "$file" | sed 's/^/ATTRIBUTE\t/' || true
done
