#!/usr/bin/env bash
set -uo pipefail
PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  mode_boundary_status=1
  stat -c '%F %n -> %N' /reference/reference-semantics
else
  mode_boundary_status=0
  printf 'GENERATED_SEMANTICS_BOUNDARY=reference-semantics absent\n'
fi

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log prompt.py py2mpy.py \
  solution.py solution.mpy semantic.k verification.k spec.k prove.sh; do
  stat -c '%F %s bytes %n -> %N' "/candidate/$artifact"
done
artifact_status=$?

find /candidate -type l -printf 'SYMLINK %p -> %l\n'
symlink_find_status=$?
find /candidate -maxdepth 1 -mindepth 1 \
  -printf 'TOP_LEVEL %y %f %s bytes -> %l\n' | sort
top_level_status=$?
find /candidate/codex-trace -type f -printf 'TRACE_FILE %p %s bytes\n' | sort
trace_find_status=$?
sha256sum \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/prompt.py /candidate/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k \
  /candidate/prove.sh
hash_status=$?

set +x
printf 'MODE_BOUNDARY_STATUS=%s\n' "$mode_boundary_status"
printf 'REQUIRED_ARTIFACT_STAT_STATUS=%s\n' "$artifact_status"
printf 'SYMLINK_FIND_STATUS=%s\n' "$symlink_find_status"
printf 'TOP_LEVEL_LIST_STATUS=%s\n' "$top_level_status"
printf 'TRACE_FIND_STATUS=%s\n' "$trace_find_status"
printf 'HASH_STATUS=%s\n' "$hash_status"
if (( mode_boundary_status || artifact_status || symlink_find_status ||
      top_level_status || trace_find_status || hash_status )); then
  exit 1
fi
exit 0
