#!/usr/bin/env bash
set -euo pipefail

printf '$ cp -a /reference/reference-semantics /tmp/audit-work/source/reference-semantics\n'
cp -a /reference/reference-semantics /tmp/audit-work/source/reference-semantics
printf '[exit 0]\n'

for name in solution.py solution.mpy verification.k spec.k; do
  printf '$ cp -a /candidate/%s /tmp/audit-work/source/%s\n' "$name" "$name"
  cp -a "/candidate/$name" "/tmp/audit-work/source/$name"
  printf '[exit 0]\n'
done

for name in canonical.py prompt.py py2mpy.py; do
  printf '$ cp -a /reference/%s /tmp/audit-work/source/%s\n' "$name" "$name"
  cp -a "/reference/$name" "/tmp/audit-work/source/$name"
  printf '[exit 0]\n'
done

printf '\nScratch source manifest:\n'
find /tmp/audit-work/source -mindepth 1 -maxdepth 3 -printf '%y %P %s bytes\n' | sort
