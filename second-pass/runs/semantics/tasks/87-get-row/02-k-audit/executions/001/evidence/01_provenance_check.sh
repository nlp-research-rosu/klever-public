#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
status=0

echo "AUDIT COMMAND: bash /audit-output/evidence/01_provenance_check.sh"
echo "Candidate top-level inventory:"
find "$candidate" -maxdepth 1 -printf '%y %M %s %f -> %l\n' | LC_ALL=C sort

echo
echo "Required/untrusted generation artifacts:"
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    stat --printf='%F %s %n\n' "$candidate/$name"
  else
    echo "MISSING $candidate/$name"
  fi
done

echo
echo "Structured trace candidates:"
find "$candidate" -maxdepth 2 \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*trajectory*' \) \
  -printf '%y %M %s %p -> %l\n' | LC_ALL=C sort

echo
echo "Trusted/candidate prompt identity:"
if cmp -s "$candidate/prompt.py" "$reference/prompt.py"; then
  echo "IDENTICAL prompt.py"
else
  echo "MISMATCH prompt.py"
  diff -u "$reference/prompt.py" "$candidate/prompt.py" || true
  status=1
fi

echo
echo "Trusted/candidate translator identity:"
if cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"; then
  echo "IDENTICAL py2mpy.py"
else
  echo "MISMATCH py2mpy.py"
  diff -u "$reference/py2mpy.py" "$candidate/py2mpy.py" || true
  status=1
fi

echo
echo "Supplied-semantics recursive identity and entry types:"
if diff --no-dereference -r "$reference/reference-semantics" \
    "$candidate/reference-semantics"; then
  echo "IDENTICAL reference-semantics/"
else
  echo "MISMATCH reference-semantics/"
  status=1
fi

echo
echo "Candidate supplied-semantics inventory:"
find "$candidate/reference-semantics" \
  -printf '%y %M %s %P -> %l\n' | LC_ALL=C sort

echo
echo "Candidate symlinks anywhere:"
find "$candidate" -type l -printf '%p -> %l\n' | LC_ALL=C sort

echo
echo "SHA-256 of audit-relevant candidate sources:"
sha256sum \
  "$candidate/prompt.py" \
  "$candidate/py2mpy.py" \
  "$candidate/solution.py" \
  "$candidate/solution.mpy" \
  "$candidate/spec.k" \
  "$candidate/verification.k"

echo
echo "SCRIPT_EXIT=$status"
exit "$status"
