#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md
evidence=/audit-output/evidence

echo 'COMMAND: verify seven required stage headings'
heading_status=0
for stage in 1 2 3 4 5 6 7; do
  if ! rg -q "^## $stage\\." "$review"; then
    heading_status=1
  fi
done
echo "EXIT_STATUS: $heading_status"

echo 'COMMAND: verify exact terminal verdict pair'
tail -n 2 "$review"
expected='VERDICT: CONCERNS
LEGITIMACY: LEGIT'
actual=$(tail -n 2 "$review")
if [ "$actual" = "$expected" ]; then
  verdict_status=0
else
  verdict_status=1
fi
echo "EXIT_STATUS: $verdict_status"

echo 'COMMAND: shell syntax-check reviewer scripts'
syntax_status=0
while IFS= read -r script; do
  if ! bash -n "$script"; then
    syntax_status=1
  fi
done < <(find "$evidence" -maxdepth 1 -type f -name '*.sh' | sort)
echo "EXIT_STATUS: $syntax_status"

echo 'COMMAND: ensure evidence top-level entries are not symlinks'
symlink_count=$(find "$evidence" -maxdepth 1 -type l | wc -l)
echo "SYMLINK_COUNT: $symlink_count"
if [ "$symlink_count" -eq 0 ]; then
  symlink_status=0
else
  symlink_status=1
fi
echo "EXIT_STATUS: $symlink_status"

echo 'COMMAND: list final review/evidence sizes'
wc -l -w -c "$review"
find "$evidence" -maxdepth 1 -type f -printf '%f|%s\n' | sort

if [ "$heading_status" -eq 0 ] && \
   [ "$verdict_status" -eq 0 ] && \
   [ "$syntax_status" -eq 0 ] && \
   [ "$symlink_status" -eq 0 ]; then
  exit 0
fi
exit 1
