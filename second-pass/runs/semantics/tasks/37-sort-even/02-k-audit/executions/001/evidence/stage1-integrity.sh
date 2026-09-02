#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
status=0

echo '$ find /candidate -maxdepth 3 -printf "%y %p -> %l\n" | sort'
find "$candidate" -maxdepth 3 -printf '%y %p -> %l\n' | sort
echo "exit=$?"

echo '$ find /reference -maxdepth 4 -printf "%y %p -> %l\n" | sort'
find "$reference" -maxdepth 4 -printf '%y %p -> %l\n' | sort
echo "exit=$?"

for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  echo "$ test -f /candidate/$artifact"
  if test -f "$candidate/$artifact"; then
    echo present
    sed -n '1,240p' "$candidate/$artifact"
    artifact_status=0
  else
    echo missing
    artifact_status=1
  fi
  echo "exit=$artifact_status"
done

echo '$ find /candidate -maxdepth 4 -iname "*trace*" -printf "%y %p -> %l\n"'
find "$candidate" -maxdepth 4 -iname '*trace*' -printf '%y %p -> %l\n'
echo "exit=$?"

echo '$ cmp -s /candidate/prompt.py /reference/prompt.py'
cmp -s "$candidate/prompt.py" "$reference/prompt.py"
cmp_status=$?
echo "exit=$cmp_status"
status=$((status | cmp_status))

echo '$ cmp -s /candidate/py2mpy.py /reference/py2mpy.py'
cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"
cmp_status=$?
echo "exit=$cmp_status"
status=$((status | cmp_status))

echo '$ diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -qr --no-dereference "$reference/reference-semantics" "$candidate/reference-semantics"
diff_status=$?
echo "exit=$diff_status"
status=$((status | diff_status))

echo '$ find /candidate/reference-semantics -type l -print'
find "$candidate/reference-semantics" -type l -print
symlinks=$(find "$candidate/reference-semantics" -type l -print -quit)
if test -n "$symlinks"; then
  symlink_status=1
else
  symlink_status=0
fi
echo "candidate_semantics_symlink_check_exit=$symlink_status"
status=$((status | symlink_status))

echo '$ sha256sum candidate/trusted prompt, translator, and semantics trees'
sha256sum "$candidate/prompt.py" "$reference/prompt.py" \
  "$candidate/py2mpy.py" "$reference/py2mpy.py"
find "$candidate/reference-semantics" -type f -print0 |
  sort -z |
  xargs -0 sha256sum
find "$reference/reference-semantics" -type f -print0 |
  sort -z |
  xargs -0 sha256sum
echo "exit=$?"

echo "integrity_comparison_exit=$status"
exit "$status"
