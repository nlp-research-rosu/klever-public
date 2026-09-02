#!/usr/bin/env bash
set -o pipefail

files=(
  /reference/reference-semantics/semantics.k
  /reference/reference-semantics/semantics/*.k
  /candidate/verification.k
  /candidate/spec.k
)

echo '$ sha256sum /reference/reference-semantics/semantics.k /reference/reference-semantics/semantics/*.k /candidate/verification.k /candidate/spec.k'
sha256sum "${files[@]}"
echo "exit=$?"

echo '$ rg -n "^\\s*(requires|module|imports|endmodule)" [all audited K sources]'
rg -n '^\s*(requires|module|imports|endmodule)' "${files[@]}"
echo "exit=$?"

echo '$ rg -n "^\\s*syntax\\b" [all audited K sources]'
rg -n '^\s*syntax\b' "${files[@]}"
echo "exit=$?"

echo '$ rg -n "^\\s*(configuration|context(?: alias)?)\\b" [all audited K sources]'
rg -n '^\s*(configuration|context(?: alias)?)\b' "${files[@]}"
echo "exit=$?"

echo '$ rg -n "^\\s*rule\\b" [all audited K sources]'
rg -n '^\s*rule\b' "${files[@]}"
echo "exit=$?"

echo '$ rg -n "^\\s*claim\\b" [all audited K sources]'
rg -n '^\s*claim\b' "${files[@]}"
echo "exit=$?"

echo '$ rg -n "\\[(?:[^]]*,\\s*)*(function|total|functional|symbol|priority|simplification|owise|anywhere|strict|seqstrict)" [all audited K sources]'
rg -n '\[(?:[^]]*,\s*)*(function|total|functional|symbol|priority|simplification|owise|anywhere|strict|seqstrict)' "${files[@]}"
echo "exit=$?"

echo '$ rg -n "\\b(opaque|hook|macro|alias)\\b" [all audited K sources]'
rg -n '\b(opaque|hook|macro|alias)\b' "${files[@]}"
opaque_rc=$?
echo "exit=$opaque_rc"

echo '$ rg -c "^\\s*syntax\\b|^\\s*configuration\\b|^\\s*context(?: alias)?\\b|^\\s*rule\\b|^\\s*claim\\b" [all audited K sources]'
rg -c '^\s*syntax\b|^\s*configuration\b|^\s*context(?: alias)?\b|^\s*rule\b|^\s*claim\b' "${files[@]}"
echo "exit=$?"

# An empty opaque/hook/macro/alias search is expected and is not a script failure.
exit 0
