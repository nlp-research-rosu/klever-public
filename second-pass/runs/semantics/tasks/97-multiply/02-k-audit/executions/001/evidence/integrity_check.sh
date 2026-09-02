#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
trusted=/reference
overall=0

printf 'CANDIDATE INVENTORY\n'
find "$candidate" -printf '%y %p -> %l\n' | LC_ALL=C sort

printf '\nTRUSTED INVENTORY\n'
find "$trusted" -printf '%y %p -> %l\n' | LC_ALL=C sort

printf '\nREQUIRED GENERATION ARTIFACTS\n'
for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$artifact" && ! -L "$candidate/$artifact" ]]; then
    printf 'PRESENT regular %s\n' "$artifact"
  elif [[ -e "$candidate/$artifact" || -L "$candidate/$artifact" ]]; then
    printf 'MISTYPED_OR_SYMLINKED %s\n' "$artifact"
    overall=1
  else
    printf 'MISSING %s\n' "$artifact"
    overall=1
  fi
done

trace_count=$(find "$candidate" -maxdepth 1 \( -iname '*trace*' -o -iname '*generation*.json' -o -iname '*generation*.jsonl' \) -printf '%f\n' | wc -l)
printf 'STRUCTURED_TRACE_CANDIDATES %s\n' "$trace_count"
find "$candidate" -maxdepth 1 \( -iname '*trace*' -o -iname '*generation*.json' -o -iname '*generation*.jsonl' \) -printf '%y %f -> %l\n' | LC_ALL=C sort

printf '\nSYMLINK CHECK\n'
symlink_count=$(find "$candidate" -type l -printf '%p -> %l\n' | tee /dev/stderr | wc -l)
printf 'CANDIDATE_SYMLINK_COUNT %s\n' "$symlink_count"
if (( symlink_count != 0 )); then
  overall=1
fi

printf '\nPROMPT IDENTITY\n'
cmp -s "$candidate/prompt.py" "$trusted/prompt.py"
status=$?
printf 'cmp candidate/prompt.py reference/prompt.py: %s\n' "$status"
(( status == 0 )) || overall=1

printf '\nTRANSLATOR IDENTITY\n'
cmp -s "$candidate/py2mpy.py" "$trusted/py2mpy.py"
status=$?
printf 'cmp candidate/py2mpy.py reference/py2mpy.py: %s\n' "$status"
(( status == 0 )) || overall=1

printf '\nSUPPLIED SEMANTICS RECURSIVE DIFF\n'
diff -r --no-dereference "$trusted/reference-semantics" "$candidate/reference-semantics"
status=$?
printf 'diff recursive status: %s\n' "$status"
(( status == 0 )) || overall=1

printf '\nSOURCE HASHES\n'
find "$candidate" "$trusted" -type f \
  \( -name '*.py' -o -name '*.mpy' -o -name '*.k' -o -name '*.json' -o -name '*.txt' -o -name '*.log' \) \
  -print0 | LC_ALL=C sort -z | xargs -0 sha256sum

printf '\nINTEGRITY_SCRIPT_STATUS %s\n' "$overall"
exit "$overall"
