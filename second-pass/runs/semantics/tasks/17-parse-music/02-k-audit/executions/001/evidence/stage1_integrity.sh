#!/usr/bin/env bash
set -u
set -o pipefail
set -x

candidate=/candidate
reference=/reference

for name in run-input.json metrics.json codex-last.txt codex-output.log prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k; do
  if test -e "$candidate/$name"; then
    stat -c '%F %n' "$candidate/$name"
  else
    printf 'MISSING %s\n' "$candidate/$name"
  fi
done

find -P "$candidate" -maxdepth 2 \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*generation*.json' \) \
  -printf '%y %p -> %l\n' | sort

cmp -s "$candidate/prompt.py" "$reference/prompt.py"
prompt_cmp_status=$?
printf 'prompt cmp exit: %d\n' "$prompt_cmp_status"

cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"
translator_cmp_status=$?
printf 'translator cmp exit: %d\n' "$translator_cmp_status"

find -P "$candidate/reference-semantics" -printf '%P\t%y\t%l\n' | sort > /tmp/audit-work/candidate-semantics-tree.tsv
find -P "$reference/reference-semantics" -printf '%P\t%y\t%l\n' | sort > /tmp/audit-work/trusted-semantics-tree.tsv
diff -u /tmp/audit-work/trusted-semantics-tree.tsv /tmp/audit-work/candidate-semantics-tree.tsv
tree_diff_status=$?
printf 'semantics tree/type/link diff exit: %d\n' "$tree_diff_status"

while IFS= read -r trusted_file; do
  rel=${trusted_file#"$reference/reference-semantics/"}
  candidate_file="$candidate/reference-semantics/$rel"
  if test ! -e "$candidate_file"; then
    printf 'MISSING_SEMANTICS_FILE %s\n' "$rel"
  elif test -L "$candidate_file"; then
    printf 'SYMLINKED_SEMANTICS_FILE %s -> %s\n' "$rel" "$(readlink "$candidate_file")"
  elif test ! -f "$candidate_file"; then
    printf 'MISTYPED_SEMANTICS_FILE %s\n' "$rel"
  elif ! cmp -s "$trusted_file" "$candidate_file"; then
    printf 'CHANGED_SEMANTICS_FILE %s\n' "$rel"
  else
    printf 'IDENTICAL_SEMANTICS_FILE %s\n' "$rel"
  fi
done < <(find -P "$reference/reference-semantics" -type f | sort)

while IFS= read -r candidate_entry; do
  rel=${candidate_entry#"$candidate/reference-semantics/"}
  if test ! -e "$reference/reference-semantics/$rel"; then
    printf 'EXTRA_SEMANTICS_ENTRY %s\n' "$rel"
  fi
done < <(find -P "$candidate/reference-semantics" -mindepth 1 | sort)

find -P "$candidate/reference-semantics" -type l -printf 'SYMLINK %P -> %l\n' | sort

sha256sum \
  "$candidate/prompt.py" "$reference/prompt.py" \
  "$candidate/py2mpy.py" "$reference/py2mpy.py" \
  "$candidate/reference-semantics/semantics.k" \
  "$reference/reference-semantics/semantics.k"

exit 0
