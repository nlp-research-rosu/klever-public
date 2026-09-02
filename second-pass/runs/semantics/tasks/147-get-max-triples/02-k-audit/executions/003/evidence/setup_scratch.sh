#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/147-get-max-triples-clean
printf '$ test ! -e %s\n' "$scratch"
test ! -e "$scratch"
printf '[exit 0]\n'

printf '$ mkdir -p %s\n' "$scratch"
mkdir -p "$scratch"
printf '[exit 0]\n'

printf '$ cp candidate proof sources and trusted inputs to scratch\n'
cp -a /candidate/solution.py "$scratch/"
cp -a /candidate/solution.mpy "$scratch/"
cp -a /candidate/spec.k "$scratch/"
cp -a /candidate/verification.k "$scratch/"
cp -a /candidate/prove.sh "$scratch/"
cp -a /candidate/concrete_tests.py "$scratch/"
cp -a /candidate/concrete_tests.mpy "$scratch/"
cp -a /candidate/reference-semantics "$scratch/"
cp -a /reference/canonical.py "$scratch/"
cp -a /reference/prompt.py "$scratch/"
cp -a /reference/py2mpy.py "$scratch/"
cp -a /audit-output/evidence/differential_test.py "$scratch/"
cp -a /audit-output/evidence/compare_program_term.py "$scratch/"
printf '[exit 0]\n'

printf '$ find scratch -maxdepth 3 -printf type/path/link\n'
find "$scratch" -maxdepth 3 -printf '%y %p -> %l\n' | sort
printf '[exit 0]\n'

printf '$ find scratch for forbidden candidate caches or compiled definitions\n'
if find "$scratch" -type d \( -name '*-kompiled' -o -name '__pycache__' \) -print | grep -q .; then
  find "$scratch" -type d \( -name '*-kompiled' -o -name '__pycache__' \) -print
  printf '[exit 1]\n'
  exit 1
fi
printf '[exit 0; none found]\n'
