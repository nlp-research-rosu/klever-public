#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
trusted=/reference

echo 'COMMAND: find /reference -printf "%y %P -> %l\n" | sort'
find "$trusted" -printf '%y %P -> %l\n' | sort
echo "EXIT: $?"

echo 'COMMAND: find /candidate -printf "%y %P -> %l\n" | sort'
find "$candidate" -printf '%y %P -> %l\n' | sort
echo "EXIT: $?"

for name in run-input.json metrics.json codex-last.txt codex-output.log generation-trace.json structured-generation-trace.json trace.json; do
  if [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    stat -c "PRESENT: %F %n -> %N" "$candidate/$name"
  else
    echo "MISSING: $candidate/$name"
  fi
done

for pair in 'prompt.py prompt.py' 'py2mpy.py py2mpy.py'; do
  set -- $pair
  echo "COMMAND: cmp -s $candidate/$1 $trusted/$2"
  cmp -s "$candidate/$1" "$trusted/$2"
  status=$?
  echo "EXIT: $status"
  sha256sum "$candidate/$1" "$trusted/$2"
done

echo 'COMMAND: diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -r --no-dereference "$trusted/reference-semantics" "$candidate/reference-semantics"
status=$?
echo "EXIT: $status"

echo 'COMMAND: compare recursive entry type and SHA-256 inventories'
reference_inventory=$(mktemp)
candidate_inventory=$(mktemp)
(
  cd "$trusted/reference-semantics" || exit 1
  find . -printf '%y %P\n' | sort
  find . -type f -print0 | sort -z | xargs -0 sha256sum
) >"$reference_inventory"
(
  cd "$candidate/reference-semantics" || exit 1
  find . -printf '%y %P\n' | sort
  find . -type f -print0 | sort -z | xargs -0 sha256sum
) >"$candidate_inventory"
diff -u "$reference_inventory" "$candidate_inventory"
status=$?
echo "EXIT: $status"
