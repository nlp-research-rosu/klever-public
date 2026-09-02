#!/usr/bin/env bash
set -u

printf 'Execute the exact regenerated submitted Module under the fresh LLVM definition:\n'
printf '$ timeout 120s krun regenerated-solution.mpy --definition /tmp/audit-work/build/runtime-kompiled\n'
timeout 120s krun regenerated-solution.mpy \
  --definition /tmp/audit-work/build/runtime-kompiled
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
