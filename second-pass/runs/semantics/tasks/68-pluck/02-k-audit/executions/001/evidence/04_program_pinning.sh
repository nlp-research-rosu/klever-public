#!/usr/bin/env bash
set +e
cd /tmp/audit-work/68-pluck || exit 90

echo '$ sed -n "53,88p" spec.k | sed "1s/^[[:space:]]*//; s/\\.Stmts//g; s/\\.Exprs//g" > embedded-program.mpy'
sed -n '53,88p' spec.k |
  sed '1s/^[[:space:]]*//; s/\.Stmts//g; s/\.Exprs//g' > embedded-program.mpy
extract_rc=$?
echo "exit=$extract_rc"

echo '$ kast solution.mpy --definition proof-audit-kompiled --sort Module --output kore > solution.kore'
kast solution.mpy \
  --definition proof-audit-kompiled \
  --sort Module \
  --output kore > solution.kore
solution_rc=$?
echo "exit=$solution_rc"

echo '$ kast embedded-program.mpy --definition proof-audit-kompiled --sort Module --output kore > embedded.kore'
kast embedded-program.mpy \
  --definition proof-audit-kompiled \
  --sort Module \
  --output kore > embedded.kore
embedded_rc=$?
echo "exit=$embedded_rc"

echo '$ cmp -s solution.kore embedded.kore'
cmp -s solution.kore embedded.kore
cmp_rc=$?
echo "exit=$cmp_rc"

echo '$ sha256sum solution.kore embedded.kore'
sha256sum solution.kore embedded.kore
hash_rc=$?
echo "exit=$hash_rc"

if (( extract_rc != 0 || solution_rc != 0 || embedded_rc != 0 || cmp_rc != 0 || hash_rc != 0 )); then
  exit 1
fi
