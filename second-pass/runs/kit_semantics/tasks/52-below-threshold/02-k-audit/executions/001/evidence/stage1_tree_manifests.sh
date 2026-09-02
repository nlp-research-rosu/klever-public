#!/usr/bin/env bash
set -u

evidence=/audit-output/evidence
status=0

printf 'STAGE 1 SUPPLEMENT: INDEPENDENT FULL-TREE MANIFESTS\n'

printf '\n$ (cd /candidate && find . -printf TYPE/PATH/SIZE metadata) > candidate-tree-types.txt\n'
(cd /candidate && find . -printf '%y\t%P\t%s\t%l\n' | LC_ALL=C sort) \
  > "$evidence/candidate-tree-types.txt"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then status=1; fi

printf '\n$ (cd /candidate && find . -type f -printf relative paths | sort | sha256sum each) > candidate-tree-sha256.txt\n'
(cd /candidate && find . -type f -printf '%P\n' | LC_ALL=C sort | while IFS= read -r file; do sha256sum "$file"; done) \
  > "$evidence/candidate-tree-sha256.txt"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then status=1; fi

printf '\n$ (cd /generation-evidence && find . -printf TYPE/PATH/SIZE metadata) > generation-tree-types.txt\n'
(cd /generation-evidence && find . -printf '%y\t%P\t%s\t%l\n' | LC_ALL=C sort) \
  > "$evidence/generation-tree-types.txt"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then status=1; fi

printf '\n$ (cd /generation-evidence && find . -type f -printf relative paths | sort | sha256sum each) > generation-tree-sha256.txt\n'
(cd /generation-evidence && find . -type f -printf '%P\n' | LC_ALL=C sort | while IFS= read -r file; do sha256sum "$file"; done) \
  > "$evidence/generation-tree-sha256.txt"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then status=1; fi

printf '\n$ wc -l tree manifests\n'
wc -l "$evidence/candidate-tree-types.txt" "$evidence/candidate-tree-sha256.txt" \
  "$evidence/generation-tree-types.txt" "$evidence/generation-tree-sha256.txt"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then status=1; fi

printf '\n$ sha256sum tree manifests\n'
sha256sum "$evidence/candidate-tree-types.txt" "$evidence/candidate-tree-sha256.txt" \
  "$evidence/generation-tree-types.txt" "$evidence/generation-tree-sha256.txt"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then status=1; fi

exit "$status"
