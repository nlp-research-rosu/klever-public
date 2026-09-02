#!/usr/bin/env bash
set -u

CAND=/candidate
REF=/reference

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return 0
}

printf 'PROVENANCE_REQUIRED_FILES\n'
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "$CAND/$name" || -L "$CAND/$name" ]]; then
    stat -c '%F %n' "$CAND/$name"
  else
    printf 'MISSING %s\n' "$CAND/$name"
  fi
done

printf '\nSTRUCTURED_TRACE_CANDIDATES\n'
find "$CAND" -maxdepth 2 \( -iname '*trace*' -o -iname '*.jsonl' \) \
  -printf '%y %p -> %l\n' | sort

printf '\nFULL_CANDIDATE_INVENTORY\n'
find "$CAND" -printf '%y %p -> %l\n' | sort

printf '\nREFERENCE_INVENTORY\n'
find "$REF" -printf '%y %p -> %l\n' | sort

printf '\nSYMLINK_CHECKS\n'
run find "$CAND/reference-semantics" -type l -printf '%p -> %l\n'
run find "$REF/reference-semantics" -type l -printf '%p -> %l\n'

printf '\nSEMANTICS_TREE_COMPARISON\n'
run diff -ruN --no-dereference "$REF/reference-semantics" "$CAND/reference-semantics"

printf '\nPROMPT_AND_TRANSLATOR_COMPARISONS\n'
run cmp "$REF/prompt.py" "$CAND/prompt.py"
run cmp "$REF/py2mpy.py" "$CAND/py2mpy.py"

printf '\nSOURCE_TYPES\n'
run stat -c '%F %a %n' \
  "$CAND/prompt.py" "$CAND/py2mpy.py" "$CAND/solution.py" \
  "$CAND/solution.mpy" "$CAND/spec.k" "$CAND/verification.k" \
  "$CAND/reference-semantics" "$REF/prompt.py" "$REF/py2mpy.py" \
  "$REF/canonical.py" "$REF/reference-semantics"

printf '\nSOURCE_HASHES\n'
run sha256sum \
  "$REF/prompt.py" "$CAND/prompt.py" \
  "$REF/py2mpy.py" "$CAND/py2mpy.py" \
  "$REF/canonical.py" "$CAND/solution.py" "$CAND/solution.mpy" \
  "$CAND/spec.k" "$CAND/verification.k"
