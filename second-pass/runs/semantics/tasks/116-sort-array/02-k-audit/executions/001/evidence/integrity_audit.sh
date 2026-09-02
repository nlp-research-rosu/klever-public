#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference
status=0

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "$candidate/$artifact" || -L "$candidate/$artifact" ]]; then
    printf 'PRESENT_REQUIRED_PROVENANCE: %s\n' "$artifact"
    stat -c 'TYPE=%F MODE=%A SIZE=%s PATH=%n' "$candidate/$artifact"
  else
    printf 'MISSING_REQUIRED_PROVENANCE: %s\n' "$artifact"
  fi
done

printf 'STRUCTURED_TRACE_CANDIDATES:\n'
find -P "$candidate" -maxdepth 1 -type f \
  \( -iname '*trace*.json' -o -iname '*trace*.jsonl' -o -iname '*trace*.log' \) \
  -printf '%f\n' | sort

for pair in \
  "$reference/prompt.py:$candidate/prompt.py" \
  "$reference/py2mpy.py:$candidate/py2mpy.py"; do
  trusted=${pair%%:*}
  submitted=${pair#*:}
  if [[ -L "$submitted" ]]; then
    printf 'INTEGRITY_FAILURE_SYMLINK: %s -> %s\n' "$submitted" "$(readlink "$submitted")"
    status=1
  elif [[ ! -f "$submitted" ]]; then
    printf 'INTEGRITY_FAILURE_MISSING_OR_MISTYPED: %s\n' "$submitted"
    status=1
  elif cmp -s "$trusted" "$submitted"; then
    printf 'BYTE_IDENTICAL: %s %s\n' "$trusted" "$submitted"
    sha256sum "$trusted" "$submitted"
  else
    printf 'INTEGRITY_FAILURE_CHANGED: %s %s\n' "$trusted" "$submitted"
    diff -u "$trusted" "$submitted" || true
    status=1
  fi
done

if [[ ! -d "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  printf 'INFRASTRUCTURE_BREACH_TRUSTED_SEMANTICS_TYPE: %s\n' \
    "$reference/reference-semantics"
  exit 2
fi

printf 'CANDIDATE_SEMANTICS_SYMLINKS:\n'
find -P "$candidate/reference-semantics" -type l -printf '%p -> %l\n' | sort
if find -P "$candidate/reference-semantics" -type l -print -quit | grep -q .; then
  status=1
fi

set +e
diff -r --no-dereference --brief \
  "$reference/reference-semantics" "$candidate/reference-semantics"
semantics_diff=$?
set -e
printf 'SEMANTICS_RECURSIVE_DIFF_STATUS: %s\n' "$semantics_diff"
if [[ "$semantics_diff" -ne 0 ]]; then
  status=1
else
  printf 'SEMANTICS_TREE_BYTE_AND_ENTRY_IDENTICAL: yes\n'
fi

printf 'CANDIDATE_TOP_LEVEL_TYPES:\n'
find -P "$candidate" -maxdepth 1 -mindepth 1 \
  -printf '%y %f -> %l\n' | sort

exit "$status"
