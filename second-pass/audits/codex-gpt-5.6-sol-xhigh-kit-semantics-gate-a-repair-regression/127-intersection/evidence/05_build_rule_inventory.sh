#!/usr/bin/env bash
set -euo pipefail

root=/tmp/audit-work/127-intersection/candidate-src
mapfile -t files < <(
  {
    find "$root/reference-semantics" -type f -name '*.k' -print
    printf '%s\n' "$root/verification.k" "$root/spec.k"
  } | sort
)

printf 'RULE INVENTORY: every top-level K declaration in the supplied tree and proof sources\n'
printf 'Classification rule: entries under reference-semantics are TRUSTED_SUPPLIED_BASELINE;\n'
printf 'entries under verification.k/spec.k are CANDIDATE_LOCAL and require individual review.\n\n'

printf 'FILE SUMMARY\n'
for file in "${files[@]}"; do
  relative=${file#"$root/"}
  lines=$(wc -l < "$file")
  bytes=$(wc -c < "$file")
  digest=$(sha256sum "$file" | cut -d' ' -f1)
  printf '%s\tlines=%s\tbytes=%s\tsha256=%s\n' "$relative" "$lines" "$bytes" "$digest"
done

printf '\nDECLARATION INDEX\n'
for file in "${files[@]}"; do
  relative=${file#"$root/"}
  awk -v file="$relative" '
    /^[[:space:]]*(configuration|syntax|context|rule|claim|alias)([[:space:]]|$)/ {
      line=$0
      sub(/^[[:space:]]*/, "", line)
      kind=line
      sub(/[[:space:]].*$/, "", kind)
      classification=(file ~ /^reference-semantics\// ? "TRUSTED_SUPPLIED_BASELINE" : "CANDIDATE_LOCAL")
      printf "%s\t%s:%d\t%s\t%s\n", classification, file, NR, kind, line
    }
  ' "$file"
done

printf '\nATTRIBUTE INDEX\n'
for file in "${files[@]}"; do
  relative=${file#"$root/"}
  awk -v file="$relative" '
    /\[(.*(function|functional|total|symbol|no-evaluators|concrete|simplification|priority|owise|macro|macro-rec).*)\]/ {
      line=$0
      sub(/^[[:space:]]*/, "", line)
      classification=(file ~ /^reference-semantics\// ? "TRUSTED_SUPPLIED_BASELINE" : "CANDIDATE_LOCAL")
      printf "%s\t%s:%d\t%s\n", classification, file, NR, line
    }
  ' "$file"
done

printf '\nOPAQUE/SYMBOL INDEX\n'
for file in "${files[@]}"; do
  relative=${file#"$root/"}
  awk -v file="$relative" '
    /symbol\(|opaque|trusted primitive|trusted opaque/ {
      line=$0
      sub(/^[[:space:]]*/, "", line)
      printf "%s:%d\t%s\n", file, NR, line
    }
  ' "$file"
done
