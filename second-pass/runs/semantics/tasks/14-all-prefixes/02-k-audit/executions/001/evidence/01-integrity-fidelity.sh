#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/proof-audit.Dl0nBZ

run_status() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
}

printf '## Mount and artifact types\n'
run_status stat -c '%F %n' /reference/reference-semantics
run_status stat -c '%F %n' /candidate
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  printf '$ test -e /candidate/%s -o -L /candidate/%s\n' "$name" "$name"
  if test -e "/candidate/$name" || test -L "/candidate/$name"; then
    stat -c '%F %n' "/candidate/$name"
    printf '[exit 0]\n'
  else
    printf 'MISSING /candidate/%s\n' "$name"
    printf '[exit 1]\n'
  fi
done

printf '\n## Symlink checks\n'
printf '$ find /candidate -type l -printf ...\n'
find /candidate -type l -printf '%p -> %l\n'
printf '[exit %d]\n' "$?"
printf '$ find /reference/reference-semantics -type l -printf ...\n'
find /reference/reference-semantics -type l -printf '%p -> %l\n'
printf '[exit %d]\n' "$?"

printf '\n## Trusted/candidate comparisons\n'
run_status cmp /candidate/prompt.py /reference/prompt.py
run_status cmp /candidate/py2mpy.py /reference/py2mpy.py
run_status diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics

printf '\n## Candidate inventory\n'
printf '$ find /candidate -printf ... | sort\n'
find /candidate -printf '%y %P -> %l\n' | sort
printf '[pipeline exit %d]\n' "$?"

printf '\n## Trusted translation regeneration\n'
printf '$ python3 /reference/py2mpy.py %s > %s\n' \
  "$SCRATCH/candidate/solution.py" "$SCRATCH/regenerated-solution.mpy"
python3 /reference/py2mpy.py "$SCRATCH/candidate/solution.py" \
  > "$SCRATCH/regenerated-solution.mpy"
printf '[exit %d]\n' "$?"
run_status cmp "$SCRATCH/regenerated-solution.mpy" "$SCRATCH/candidate/solution.mpy"
run_status sha256sum \
  "$SCRATCH/regenerated-solution.mpy" \
  "$SCRATCH/candidate/solution.mpy" \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py

