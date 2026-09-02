#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
scratch=/tmp/audit-work/140-fix-spaces

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf 'Stage 1 and translator-fidelity evidence\n'
printf 'Candidate artifact types (l=symlink, f=regular file, d=directory):\n'
run find "$candidate" -printf '%y %p -> %l\n'

printf '\nRequired untrusted provenance artifacts:\n'
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -L "$candidate/$name" ]]; then
    printf '%s: symlink -> %s\n' "$name" "$(readlink "$candidate/$name")"
  elif [[ -f "$candidate/$name" ]]; then
    printf '%s: regular file\n' "$name"
  elif [[ -e "$candidate/$name" ]]; then
    printf '%s: present but not a regular file\n' "$name"
  else
    printf '%s: MISSING\n' "$name"
  fi
done

printf '\nPotential structured generation traces:\n'
run find "$candidate" -maxdepth 2 -type f '(' -iname '*trace*' -o -iname '*.jsonl' -o -iname '*.json' ')' -print

printf '\nTrusted/candidate prompt and translator byte comparisons:\n'
run cmp -s "$candidate/prompt.py" "$reference/prompt.py"
run cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"
run sha256sum "$candidate/prompt.py" "$reference/prompt.py" "$candidate/py2mpy.py" "$reference/py2mpy.py"

printf '\nSupplied-semantics structural and byte comparison:\n'
run diff -r --no-dereference --brief "$candidate/reference-semantics" "$reference/reference-semantics"
run find "$candidate/reference-semantics" -type l -print
run find "$reference/reference-semantics" -type l -print
run bash -c 'cd /candidate/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum'
run bash -c 'cd /reference/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum'

printf '\nTrusted translator regeneration and byte comparison:\n'
printf '$ python3 /reference/py2mpy.py /tmp/audit-work/140-fix-spaces/solution.py > /tmp/audit-work/140-fix-spaces/regenerated-solution.mpy\n'
python3 "$reference/py2mpy.py" "$scratch/solution.py" > "$scratch/regenerated-solution.mpy"
status=$?
printf '[exit %d]\n' "$status"
run cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
run sha256sum "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
