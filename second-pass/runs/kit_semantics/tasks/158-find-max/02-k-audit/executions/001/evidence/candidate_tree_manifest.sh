#!/usr/bin/env bash
set -euo pipefail

root=/candidate
output=/audit-output/evidence/candidate_tree.manifest.tsv

printf '$ cd /candidate && hash every mounted entry into %s\n' "$output"
(
  cd "$root"
  while IFS= read -r -d '' path; do
    kind=$(stat -c '%F' "$path")
    mode=$(stat -c '%a' "$path")
    size=$(stat -c '%s' "$path")
    if [[ -f "$path" && ! -L "$path" ]]; then
      digest=$(sha256sum "$path" | cut -d' ' -f1)
      target=-
    elif [[ -L "$path" ]]; then
      digest=-
      target=$(readlink "$path")
    else
      digest=-
      target=-
    fi
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$kind" "$mode" "$size" "$digest" "$target" "${path#./}"
  done < <(find . -mindepth 1 -print0 | sort -z)
) > "$output"

entries=$(wc -l < "$output")
symlinks=$(awk -F '\t' '$1 == "symbolic link" { count += 1 } END { print count + 0 }' "$output")
printf 'entries=%d\n' "$entries"
printf 'symlinks=%d\n' "$symlinks"
sha256sum "$output"

if (( symlinks != 0 )); then
  printf 'Candidate symlinks require manual review\n'
  awk -F '\t' '$1 == "symbolic link" { print }' "$output"
fi

printf 'Required proof artifacts\n'
for path in \
  solution.py \
  solution.mpy \
  verification.k \
  spec.k \
  prove.sh \
  PROOF.md; do
  stat -c '%F %s %n' "$root/$path"
done
