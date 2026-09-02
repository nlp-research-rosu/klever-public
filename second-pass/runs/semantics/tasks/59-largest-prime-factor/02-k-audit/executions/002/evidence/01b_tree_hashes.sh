#!/usr/bin/env bash
set -u

normalized_tree_hash() {
  root=$1
  (
    cd "$root" || exit 1
    find . -type f -print0 |
      sort -z |
      while IFS= read -r -d '' path; do
        digest=$(sha256sum "$path" | cut -d ' ' -f 1)
        printf '%s  %s\n' "$digest" "$path"
      done |
      sha256sum
  )
}

for root in /candidate /reference /generation-evidence; do
  echo "$ normalized_tree_hash $root"
  normalized_tree_hash "$root"
  status=$?
  echo "[exit $status]"
done

echo "$ find /candidate -printf '%y %P -> %l\\n'"
find /candidate -printf '%y %P -> %l\n' | sort
echo "[exit $?]"
