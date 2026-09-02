#!/usr/bin/env bash
set +e

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
}

run find /candidate -maxdepth 4 -printf '%y %p -> %l\n'
run find /reference -maxdepth 4 -printf '%y %p -> %l\n'

for name in run-input.json metrics.json codex-last.txt codex-output.log generation-trace.json trace.json PROOF.md; do
  if [[ -e "/candidate/$name" || -L "/candidate/$name" ]]; then
    run stat -c '%F %n' "/candidate/$name"
  else
    printf '\nMISSING: /candidate/%s\n' "$name"
  fi
done

run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
run find /candidate/reference-semantics -printf '%y %P -> %l\n'
run find /reference/reference-semantics -printf '%y %P -> %l\n'

mapfile -t candidate_semantics_files < <(find /candidate/reference-semantics -type f -print | sort)
mapfile -t reference_semantics_files < <(find /reference/reference-semantics -type f -print | sort)
run sha256sum \
  /candidate/prompt.py \
  /reference/prompt.py \
  /candidate/py2mpy.py \
  /reference/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /reference/canonical.py \
  "${candidate_semantics_files[@]}" \
  "${reference_semantics_files[@]}"

run command -v kompile
run command -v kprove
run kompile --version
run kprove --version
