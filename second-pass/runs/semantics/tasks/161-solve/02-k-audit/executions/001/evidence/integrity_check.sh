#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
failure=0

echo "== candidate tree (physical walk) =="
find -P "$candidate" -printf '%y %P -> %l\n' | LC_ALL=C sort

echo "== required proof/program artifacts =="
for rel in solution.py solution.mpy spec.k verification.k prompt.py py2mpy.py reference-semantics; do
  if [ -e "$candidate/$rel" ] || [ -L "$candidate/$rel" ]; then
    stat -c '%F %n' "$candidate/$rel"
  else
    echo "MISSING $candidate/$rel"
    failure=1
  fi
done

echo "== expected provenance claims =="
for rel in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [ -e "$candidate/$rel" ] || [ -L "$candidate/$rel" ]; then
    stat -c '%F %n' "$candidate/$rel"
  else
    echo "ABSENT $candidate/$rel"
  fi
done
find -P "$candidate" -maxdepth 2 \
  \( -iname '*trace*' -o -iname '*trajectory*' -o -iname '*generation*.json*' \) \
  -printf 'TRACE_CANDIDATE %y %p -> %l\n' | LC_ALL=C sort

echo "== symlink check =="
symlinks=$(find -P "$candidate" -type l -print)
if [ -n "$symlinks" ]; then
  printf '%s\n' "$symlinks"
  failure=1
else
  echo "NO_SYMLINKS"
fi

echo "== prompt identity =="
if cmp -s "$candidate/prompt.py" "$reference/prompt.py"; then
  echo "IDENTICAL prompt.py"
else
  echo "DIFFERENT prompt.py"
  failure=1
  diff -u "$reference/prompt.py" "$candidate/prompt.py" || true
fi

echo "== translator identity =="
if cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"; then
  echo "IDENTICAL py2mpy.py"
else
  echo "DIFFERENT py2mpy.py"
  failure=1
  diff -u "$reference/py2mpy.py" "$candidate/py2mpy.py" || true
fi

echo "== supplied-semantics tree identity =="
if [ ! -d "$reference/reference-semantics" ] || [ -L "$reference/reference-semantics" ]; then
  echo "INFRASTRUCTURE_BREACH trusted reference-semantics missing, mistyped, or symlinked"
  exit 70
fi
if diff -r --no-dereference \
    "$reference/reference-semantics" "$candidate/reference-semantics"; then
  echo "IDENTICAL reference-semantics"
else
  echo "DIFFERENT reference-semantics"
  failure=1
fi

echo "== trusted semantics manifest =="
find -P "$reference/reference-semantics" -type f -print0 \
  | LC_ALL=C sort -z \
  | xargs -0 sha256sum
echo "== candidate semantics manifest =="
find -P "$candidate/reference-semantics" -type f -print0 \
  | LC_ALL=C sort -z \
  | xargs -0 sha256sum

exit "$failure"
