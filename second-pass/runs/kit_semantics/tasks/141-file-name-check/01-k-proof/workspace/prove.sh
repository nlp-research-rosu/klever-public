#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 test_solution.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

proof_tmp=$(mktemp -d /tmp/file-name-check-proof.XXXXXX)
trap 'rm -rf "$proof_tmp"' EXIT

cp solution.py "$proof_tmp/concrete.py"
printf '%s\n' \
  'assert file_name_check("example.txt") == "Yes"' \
  'assert file_name_check("1example.dll") == "No"' \
  'assert file_name_check("a123.txt") == "Yes"' \
  'assert file_name_check("a1234.txt") == "No"' \
  'assert file_name_check("a.b.txt") == "No"' \
  'assert file_name_check("abc.atxt") == "No"' \
  'assert file_name_check(".txt") == "No"' \
  'assert file_name_check("A0b1c2.dll") == "Yes"' \
  >> "$proof_tmp/concrete.py"
python3 py2mpy.py "$proof_tmp/concrete.py" > "$proof_tmp/concrete.mpy"
krun "$proof_tmp/concrete.mpy" --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kast solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  > "$proof_tmp/solution.kore"
kast proof-program.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  > "$proof_tmp/proof-program.kore"
cmp "$proof_tmp/solution.kore" "$proof_tmp/proof-program.kore"
echo "PROGRAM_IDENTITY_MATCH"

sed '0,/Return(Str("Yes"))/s//Return(Str("No"))/' \
  solution.mpy > "$proof_tmp/mutated-solution.mpy"
kast "$proof_tmp/mutated-solution.mpy" \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  > "$proof_tmp/mutated-solution.kore"
if cmp -s "$proof_tmp/mutated-solution.kore" \
          "$proof_tmp/proof-program.kore"; then
  echo "UNEXPECTED PROGRAM-IDENTITY MATCH"
  exit 1
else
  echo "EXPECTED PROGRAM-IDENTITY FAILURE"
fi

kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-kompiled
kprove lemma-spec.k \
  --definition audit-kompiled \
  --spec-module LEMMA-SPEC

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > "$proof_tmp/vacuity.log" 2>&1
vacuity_status=$?
set -e
sed -n '1,100p' "$proof_tmp/vacuity.log"
if [ "$vacuity_status" -eq 0 ]; then
  echo "UNEXPECTED VACUITY SUCCESS"
  exit 1
fi
if ! rg -q "WarnStuckClaimState" "$proof_tmp/vacuity.log"; then
  echo "VACUITY PROBE FAILED WITHOUT A STUCK CLAIM"
  exit 1
fi
echo "EXPECTED VACUITY FAILURE exit=$vacuity_status"
