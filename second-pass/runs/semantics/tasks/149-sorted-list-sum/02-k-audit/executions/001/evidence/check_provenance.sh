#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
trusted=/reference
failed=0

echo "semantics_mode=SUPPLIED_SEMANTICS"
if [[ -d "$trusted/reference-semantics" && ! -L "$trusted/reference-semantics" ]]; then
  echo "trusted_reference_semantics=present_directory"
else
  echo "trusted_reference_semantics=INVALID"
  failed=1
fi

for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    echo "$name=present_regular"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    echo "$name=present_wrong_type_or_symlink"
    failed=1
  else
    echo "$name=missing"
  fi
done

trace_count=$(find "$candidate" -maxdepth 1 \
  \( -iname '*trace*.json' -o -iname '*trace*.jsonl' -o -iname '*trace*.log' \) \
  -printf '%f\n' | wc -l)
echo "structured_trace_candidates=$trace_count"

for pair in "prompt.py:prompt.py" "py2mpy.py:py2mpy.py"; do
  trusted_name=${pair%%:*}
  candidate_name=${pair##*:}
  if [[ ! -f "$candidate/$candidate_name" || -L "$candidate/$candidate_name" ]]; then
    echo "$candidate_name=missing_wrong_type_or_symlink"
    failed=1
  elif cmp -s "$trusted/$trusted_name" "$candidate/$candidate_name"; then
    echo "$candidate_name=byte_identical"
  else
    echo "$candidate_name=changed"
    failed=1
  fi
done

if diff -r --no-dereference "$trusted/reference-semantics" \
    "$candidate/reference-semantics"; then
  echo "reference-semantics=recursive_identity_pass"
else
  echo "reference-semantics=recursive_identity_fail"
  failed=1
fi

candidate_symlinks=$(find "$candidate/reference-semantics" -type l -print)
trusted_symlinks=$(find "$trusted/reference-semantics" -type l -print)
if [[ -n "$candidate_symlinks" || -n "$trusted_symlinks" ]]; then
  echo "reference-semantics=symlink_failure"
  printf '%s\n' "$candidate_symlinks" "$trusted_symlinks"
  failed=1
else
  echo "reference-semantics=no_symlinks"
fi

echo "candidate_semantics_manifest:"
find "$candidate/reference-semantics" -printf '%y %P\n' | sort
echo "trusted_semantics_manifest:"
find "$trusted/reference-semantics" -printf '%y %P\n' | sort

exit "$failed"
