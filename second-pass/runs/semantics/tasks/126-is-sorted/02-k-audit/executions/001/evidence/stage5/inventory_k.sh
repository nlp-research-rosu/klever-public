#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "usage: $0 ROOT" >&2
  exit 64
fi

root=$1
find "$root" -type f -name '*.k' -print0 |
  LC_ALL=C sort -z |
  while IFS= read -r -d '' file; do
    rel=${file#"$root"/}
    printf 'FILE\t%s\tSHA256\t' "$rel"
    sha256sum "$file" | awk '{print $1}'
    awk -v file="$rel" '
      function emit(kind) {
        text=$0
        sub(/^[[:space:]]+/, "", text)
        printf "ITEM\t%s\t%d\t%s\t%s\n", file, NR, kind, text
      }
      /^[[:space:]]*requires[[:space:]]/      { emit("requires") }
      /^[[:space:]]*module[[:space:]]/        { emit("module") }
      /^[[:space:]]*imports[[:space:]]/       { emit("imports") }
      /^[[:space:]]*configuration([[:space:]]|$)/ { emit("configuration") }
      /^[[:space:]]*syntax[[:space:]]/        { emit("syntax") }
      /^[[:space:]]*context([[:space:]]|$)/   { emit("context") }
      /^[[:space:]]*rule([[:space:]]|$)/      { emit("rule") }
      /^[[:space:]]*claim([[:space:]]|$)/     { emit("claim") }
      $0 !~ /^[[:space:]]*\/\// &&
      /\[[^]]*(function|functional|total|symbol|macro|priority|simplification|owise|concrete)/ {
        emit("attribute")
      }
      END {
        printf "COUNT\t%s\trules=%d\tsyntax=%d\tclaims=%d\tconfigurations=%d\tcontexts=%d\n",
          file, rule_count, syntax_count, claim_count, config_count, context_count
      }
      /^[[:space:]]*rule([[:space:]]|$)/      { rule_count++ }
      /^[[:space:]]*syntax[[:space:]]/        { syntax_count++ }
      /^[[:space:]]*claim([[:space:]]|$)/     { claim_count++ }
      /^[[:space:]]*configuration([[:space:]]|$)/ { config_count++ }
      /^[[:space:]]*context([[:space:]]|$)/   { context_count++ }
    ' "$file"
  done
