#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference

echo 'RENDERED_MODE: SUPPLIED_SEMANTICS'
if [ -d "$reference/reference-semantics" ] && [ ! -L "$reference/reference-semantics" ]; then
  echo 'MODE_MOUNT_CHECK: PASS (trusted reference semantics is a real directory)'
else
  echo 'MODE_MOUNT_CHECK: FAIL'
fi

echo 'CANDIDATE_ENTRY_TYPES:'
find "$candidate" -printf '%y %P -> %l\n' | LC_ALL=C sort
echo 'TRUSTED_SEMANTICS_ENTRY_TYPES:'
find "$reference/reference-semantics" -printf '%y %P -> %l\n' | LC_ALL=C sort

echo 'SEMANTICS_RECURSIVE_DIFF:'
diff --recursive --no-dereference \
  "$candidate/reference-semantics" \
  "$reference/reference-semantics"
semantics_status=$?
echo "SEMANTICS_DIFF_STATUS: $semantics_status"

for pair in \
  "$candidate/prompt.py:$reference/prompt.py" \
  "$candidate/py2mpy.py:$reference/py2mpy.py"
do
  left=${pair%%:*}
  right=${pair#*:}
  cmp --silent "$left" "$right"
  status=$?
  echo "BYTE_COMPARE: $left $right STATUS=$status"
done

echo 'REQUESTED_GENERATION_METADATA:'
for name in \
  run-input.json \
  metrics.json \
  codex-last.txt \
  codex-output.log \
  generation-trace.json \
  generation-trace.jsonl \
  structured-generation-trace.json \
  trace.json
do
  path="$candidate/$name"
  if [ -L "$path" ]; then
    echo "SYMLINK $path -> $(readlink "$path")"
  elif [ -e "$path" ]; then
    stat -c '%F %s %n' "$path"
  else
    echo "MISSING $path"
  fi
done

echo 'SOURCE_HASHES:'
sha256sum \
  "$candidate/prompt.py" \
  "$reference/prompt.py" \
  "$candidate/py2mpy.py" \
  "$reference/py2mpy.py" \
  "$candidate/solution.py" \
  "$candidate/solution.mpy" \
  "$candidate/spec.k" \
  "$candidate/verification.k"

exit 0
