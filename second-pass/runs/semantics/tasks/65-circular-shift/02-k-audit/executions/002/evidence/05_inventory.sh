#!/usr/bin/env bash
set -uo pipefail

root=/tmp/audit-work/reconstruction

echo '$ sha256sum every reviewed K source'
find "$root/reference-semantics" -type f -name '*.k' -print0 |
  sort -z |
  xargs -0 sha256sum
sha_pipeline=("${PIPESTATUS[@]}")
echo "EXIT_STATUS find=${sha_pipeline[0]} sort=${sha_pipeline[1]} xargs=${sha_pipeline[2]}"

echo '$ exhaustive declaration/rule/context/claim inventory'
rg --line-number \
  '^[[:space:]]*(requires|module|endmodule|imports|configuration|syntax|context|rule|claim|alias)([[:space:]]|$)' \
  "$root/reference-semantics" \
  "$root/verification.k" \
  "$root/spec.k"
inventory_status=$?
echo "EXIT_STATUS=$inventory_status"

echo '$ source-by-source inventory counts'
for source in \
  "$root/reference-semantics/semantics.k" \
  "$root"/reference-semantics/semantics/*.k \
  "$root/verification.k" \
  "$root/spec.k"
do
  declarations=$(rg --count \
    '^[[:space:]]*(requires|module|endmodule|imports|configuration|syntax|context|rule|claim|alias)([[:space:]]|$)' \
    "$source")
  rules=$(rg --count '^[[:space:]]*rule([[:space:]]|$)' "$source" || true)
  syntax=$(rg --count '^[[:space:]]*syntax([[:space:]]|$)' "$source" || true)
  contexts=$(rg --count '^[[:space:]]*context([[:space:]]|$)' "$source" || true)
  claims=$(rg --count '^[[:space:]]*claim([[:space:]]|$)' "$source" || true)
  functions=$(rg --count '\[[^]]*(function|functional)[^]]*\]' "$source" || true)
  totals=$(rg --count '\[[^]]*total[^]]*\]' "$source" || true)
  simplifications=$(rg --count '\[[^]]*simplification[^]]*\]' "$source" || true)
  priorities=$(rg --count '\[priority\\(' "$source" || true)
  concretes=$(rg --count '\[[^]]*concrete[^]]*\]' "$source" || true)
  echo "COUNT file=$source declarations=${declarations:-0} rules=${rules:-0} syntax=${syntax:-0} contexts=${contexts:-0} claims=${claims:-0} function_attrs=${functions:-0} total_attrs=${totals:-0} simplification_attrs=${simplifications:-0} priority_attrs=${priorities:-0} concrete_attrs=${concretes:-0}"
done

echo '$ every special attribute occurrence, including multiline rule attributes'
rg --line-number \
  '\[(function|functional|total|simplification|concrete|owise|priority|strict|seqstrict|macro|token|bracket|left|right)' \
  "$root/reference-semantics" \
  "$root/verification.k" \
  "$root/spec.k"
attributes_status=$?
echo "EXIT_STATUS=$attributes_status"

if (( inventory_status != 0 || attributes_status != 0 )); then
  exit 1
fi
