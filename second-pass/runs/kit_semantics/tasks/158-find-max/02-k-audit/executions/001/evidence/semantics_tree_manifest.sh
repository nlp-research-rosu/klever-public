#!/usr/bin/env bash
set -euo pipefail

make_manifest() {
  root=$1
  output=$2
  (
    cd "$root"
    while IFS= read -r -d '' path; do
      kind=$(stat -c '%F' "$path")
      mode=$(stat -c '%a' "$path")
      if [[ -f "$path" ]]; then
        digest=$(sha256sum "$path" | cut -d' ' -f1)
        size=$(stat -c '%s' "$path")
      else
        digest=-
        size=-
      fi
      printf '%s\t%s\t%s\t%s\t%s\n' \
        "$kind" "$mode" "$size" "$digest" "${path#./}"
    done < <(find . -mindepth 1 -print0 | sort -z)
  ) > "$output"
}

printf '%s\n' \
  '$ bash /audit-output/evidence/semantics_tree_manifest.sh'
make_manifest \
  /reference/reference-semantics \
  /audit-output/evidence/reference-semantics.manifest.tsv
make_manifest \
  /candidate/reference-semantics \
  /audit-output/evidence/candidate-reference-semantics.manifest.tsv

sha256sum \
  /audit-output/evidence/reference-semantics.manifest.tsv \
  /audit-output/evidence/candidate-reference-semantics.manifest.tsv
cmp \
  /audit-output/evidence/reference-semantics.manifest.tsv \
  /audit-output/evidence/candidate-reference-semantics.manifest.tsv
printf 'manifests_byte_identical=yes\n'
