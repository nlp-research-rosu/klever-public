#!/usr/bin/env bash
set -uo pipefail

translated=/tmp/audit-work/review-57/build/solution.trusted-regenerated.mpy

printf 'COMMAND: python3 /tmp/audit-work/review-57/trusted/py2mpy.py /tmp/audit-work/review-57/src/solution.py > %s\n' "$translated"
python3 /tmp/audit-work/review-57/trusted/py2mpy.py \
  /tmp/audit-work/review-57/src/solution.py > "$translated"
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || exit "$status"

printf 'COMMAND: cmp -s %s /tmp/audit-work/review-57/src/solution.mpy\n' "$translated"
cmp -s "$translated" /tmp/audit-work/review-57/src/solution.mpy
status=$?
printf 'EXIT_STATUS: %d\n' "$status"

printf 'COMMAND: sha256sum %s /tmp/audit-work/review-57/src/solution.mpy\n' "$translated"
sha256sum "$translated" /tmp/audit-work/review-57/src/solution.mpy
hash_status=$?
printf 'EXIT_STATUS: %d\n' "$hash_status"

(( status == 0 && hash_status == 0 ))
