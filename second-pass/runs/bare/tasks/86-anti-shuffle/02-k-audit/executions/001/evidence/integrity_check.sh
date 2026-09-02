#!/usr/bin/env bash
set -uo pipefail

status=0

printf 'reference tree:\n'
find /reference -maxdepth 3 -printf '%y %p -> %l\n' | sort

printf '\ncandidate source-level tree (compiled trees pruned):\n'
find /candidate \
  \( -path /candidate/semantic-kompiled -o \
     -path /candidate/verification-kompiled -o \
     -path /candidate/__pycache__ \) -prune -o \
  -printf '%y %p -> %l\n' | sort

printf '\nrequired generated-semantics boundary:\n'
if [[ -e /reference/reference-semantics || \
      -L /reference/reference-semantics ]]; then
  printf 'ERROR: forbidden /reference/reference-semantics exists\n'
  status=1
else
  printf 'OK: /reference/reference-semantics is absent\n'
fi

printf '\ntrusted/candidate provenance comparisons:\n'
for pair in \
  '/reference/prompt.py:/candidate/prompt.py' \
  '/reference/py2mpy.py:/candidate/py2mpy.py'
do
  trusted=${pair%%:*}
  submitted=${pair#*:}
  if cmp -s "$trusted" "$submitted"; then
    printf 'IDENTICAL: %s %s\n' "$trusted" "$submitted"
  else
    printf 'DIFFERENT: %s %s\n' "$trusted" "$submitted"
    status=1
  fi
done

printf '\nsource hashes:\n'
sha256sum \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log

printf '\nsymlinks below candidate:\n'
symlink_list=$(find /candidate -type l -print)
if [[ -n "$symlink_list" ]]; then
  printf '%s\n' "$symlink_list"
fi
symlink_count=$(printf '%s' "$symlink_list" | awk 'NF { count += 1 } END { print count + 0 }')
printf 'symlink_count=%d\n' "$symlink_count"
if (( symlink_count != 0 )); then
  status=1
fi

exit "$status"
