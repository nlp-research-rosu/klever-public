#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
scratch=/tmp/audit-work

echo '$ find /candidate -maxdepth 2 -mindepth 1 -printf ... | sort'
find "$candidate" -maxdepth 2 -mindepth 1 -printf '%y\t%m\t%s\t%p\t%l\n' | sort
echo "exit=$?"

echo '$ find /candidate -type l -printf ...'
find "$candidate" -type l -printf '%p -> %l\n'
symlink_find_status=$?
echo "exit=$symlink_find_status"

echo '$ compare candidate and reference semantics entry types and symlink targets'
find "$candidate/reference-semantics" -printf '%P\t%y\t%l\n' | sort > "$scratch/candidate-semantics-types.txt"
candidate_find_status=$?
find "$reference/reference-semantics" -printf '%P\t%y\t%l\n' | sort > "$scratch/reference-semantics-types.txt"
reference_find_status=$?
diff -u "$scratch/reference-semantics-types.txt" "$scratch/candidate-semantics-types.txt"
types_diff_status=$?
echo "candidate_find_exit=$candidate_find_status reference_find_exit=$reference_find_status diff_exit=$types_diff_status"

echo '$ diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -r --no-dereference "$reference/reference-semantics" "$candidate/reference-semantics"
semantics_diff_status=$?
echo "exit=$semantics_diff_status"

for pair in \
  "$reference/prompt.py $candidate/prompt.py" \
  "$reference/py2mpy.py $candidate/py2mpy.py"
do
  set -- $pair
  echo "\$ cmp -s $1 $2"
  cmp -s "$1" "$2"
  status=$?
  echo "exit=$status"
  sha256sum "$1" "$2"
done

echo '$ check required untrusted generation records'
for name in run-input.json metrics.json codex-last.txt codex-output.log
do
  if test -f "$candidate/$name"; then
    echo "PRESENT regular-file $candidate/$name"
  elif test -e "$candidate/$name" || test -L "$candidate/$name"; then
    printf 'MISTYPED %s: ' "$candidate/$name"
    stat -c '%F' "$candidate/$name"
  else
    echo "MISSING $candidate/$name"
  fi
done
find "$candidate" -maxdepth 2 \( -iname '*trace*' -o -iname '*.jsonl' \) -printf 'TRACE_CANDIDATE %y %p -> %l\n'
echo "exit=$?"

if test "$types_diff_status" -eq 0 &&
   test "$semantics_diff_status" -eq 0
then
  echo 'SEMANTICS_INTEGRITY=IDENTICAL'
else
  echo 'SEMANTICS_INTEGRITY=FAIL'
fi
