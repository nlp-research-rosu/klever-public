#!/usr/bin/env bash
set -uo pipefail

candidate_root=/candidate
reference_root=/reference
status=0

printf '%s\n' 'SEMANTICS_BOUNDARY: GENERATED_SEMANTICS'
if [[ -e "$reference_root/reference-semantics" || -L "$reference_root/reference-semantics" ]]; then
  printf '%s\n' 'ERROR: forbidden /reference/reference-semantics is present'
  status=1
else
  printf '%s\n' 'OK: /reference/reference-semantics is absent'
fi

required=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
  prove.sh
)

for artifact in "${required[@]}"; do
  path="$candidate_root/$artifact"
  if [[ -L "$path" ]]; then
    printf 'ERROR: required artifact is symlink: %s\n' "$path"
    status=1
  elif [[ ! -e "$path" ]]; then
    printf 'ERROR: required artifact missing: %s\n' "$path"
    status=1
  elif [[ ! -f "$path" ]]; then
    printf 'ERROR: required artifact is not a regular file: %s\n' "$path"
    status=1
  else
    stat -c 'OK: regular file size=%s path=%n' "$path"
  fi
done

trace_count=$(
  find "$candidate_root/codex-trace" -type f -name '*.jsonl' -print 2>/dev/null |
    wc -l
)
printf 'STRUCTURED_TRACE_FILE_COUNT: %s\n' "$trace_count"
find "$candidate_root/codex-trace" -printf 'TRACE_ENTRY: %y %p -> %l\n' 2>/dev/null |
  sort

if cmp -s "$candidate_root/prompt.py" "$reference_root/prompt.py"; then
  printf '%s\n' 'OK: candidate prompt.py is byte-identical to trusted prompt.py'
else
  printf '%s\n' 'ERROR: candidate prompt.py differs from trusted prompt.py'
  status=1
fi

if cmp -s "$candidate_root/py2mpy.py" "$reference_root/py2mpy.py"; then
  printf '%s\n' 'OK: candidate py2mpy.py is byte-identical to trusted py2mpy.py'
else
  printf '%s\n' 'ERROR: candidate py2mpy.py differs from trusted py2mpy.py'
  status=1
fi

printf '%s\n' 'TRUSTED_AND_CANDIDATE_HASHES:'
sha256sum \
  "$reference_root/prompt.py" \
  "$candidate_root/prompt.py" \
  "$reference_root/py2mpy.py" \
  "$candidate_root/py2mpy.py" \
  "$reference_root/canonical.py" \
  "$candidate_root/solution.py" \
  "$candidate_root/solution.mpy" \
  "$candidate_root/semantic.k" \
  "$candidate_root/verification.k" \
  "$candidate_root/spec.k" \
  "$candidate_root/prove.sh"

printf '%s\n' 'CANDIDATE_TOP_LEVEL_INVENTORY:'
find "$candidate_root" -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort

printf 'PROVENANCE_CHECK_STATUS: %s\n' "$status"
exit "$status"
