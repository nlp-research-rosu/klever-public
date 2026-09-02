#!/usr/bin/env bash
set -eu

scratch=/tmp/audit-work/audit-113
printf '$ mkdir -p %q\n' "$scratch"
mkdir -p "$scratch"

for name in solution.py solution.mpy spec.k verification.k concrete_tests.py concrete_tests.mpy; do
  printf '$ cp -p %q %q\n' "/candidate/$name" "$scratch/$name"
  cp -p "/candidate/$name" "$scratch/$name"
done

printf '$ cp -p %q %q\n' /reference/py2mpy.py "$scratch/py2mpy.py"
cp -p /reference/py2mpy.py "$scratch/py2mpy.py"

printf '$ cp -a %q %q\n' /reference/reference-semantics "$scratch/reference-semantics"
cp -a /reference/reference-semantics "$scratch/reference-semantics"

printf '$ find -P %q -printf ...\n' "$scratch"
find -P "$scratch" -printf '%y %m %s %p -> %l\n' | sort
printf 'EXIT_STATUS=0\n'
