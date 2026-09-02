#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  return "$status"
}

printf '%s\n' '## Required untrusted generation artifacts'
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -e "/candidate/$name" || -L "/candidate/$name" ]]; then
    run stat -c '%F %n -> %N' "/candidate/$name"
  else
    printf 'MISSING: /candidate/%s\n' "$name"
  fi
done
printf '\n'

printf '%s\n' '## Artifact type inventory'
run find /candidate -maxdepth 4 -printf '%y %p -> %l\n'
run find /reference -maxdepth 4 -printf '%y %p -> %l\n'

printf '%s\n' '## Trusted file comparisons'
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff --no-dereference -qr /candidate/reference-semantics /reference/reference-semantics

printf '%s\n' '## Hash manifests'
run bash -c 'find /candidate/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum'
run bash -c 'find /reference/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum'

printf '%s\n' '## Trusted retranslation'
run python3 /reference/py2mpy.py /tmp/audit-work/115-max-fill/solution.py
python3 /reference/py2mpy.py /tmp/audit-work/115-max-fill/solution.py \
  > /tmp/audit-work/115-max-fill/solution.trusted.mpy
translation_status=$?
printf 'COMMAND: python3 /reference/py2mpy.py /tmp/audit-work/115-max-fill/solution.py > /tmp/audit-work/115-max-fill/solution.trusted.mpy\n'
printf 'EXIT_STATUS: %s\n\n' "$translation_status"
run cmp -s /tmp/audit-work/115-max-fill/solution.trusted.mpy /tmp/audit-work/115-max-fill/solution.mpy
run sha256sum /tmp/audit-work/115-max-fill/solution.trusted.mpy /tmp/audit-work/115-max-fill/solution.mpy
