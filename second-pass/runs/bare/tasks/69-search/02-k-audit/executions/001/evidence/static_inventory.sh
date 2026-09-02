#!/usr/bin/env bash
set -u

audit_src=/tmp/audit-work/69-search-audit/src
files=(
  semantic.k
  verification-core.k
  verification.k
  loop-lemma-spec.k
  spec.k
  solution.mpy
)

printf 'Source hashes\n'
for file in "${files[@]}"; do
  sha256sum "$audit_src/$file"
done

printf '\nDeclarations, rules, claims, attributes, and configuration lines\n'
rg -n \
  '(^\s*(module|endmodule|imports|requires|configuration|syntax|rule|claim)\b|\[(function|total|functional|simplification|macro|priority|anywhere|owise|trusted)[^]]*\])' \
  "$audit_src/semantic.k" \
  "$audit_src/verification-core.k" \
  "$audit_src/verification.k" \
  "$audit_src/loop-lemma-spec.k" \
  "$audit_src/spec.k"

printf '\nComplete numbered K sources\n'
for file in "${files[@]}"; do
  printf '\n===== %s =====\n' "$file"
  nl -ba "$audit_src/$file"
done
