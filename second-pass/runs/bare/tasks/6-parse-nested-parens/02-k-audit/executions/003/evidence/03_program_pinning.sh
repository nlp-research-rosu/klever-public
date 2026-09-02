#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/candidate
definition=/tmp/audit-work/runs/verification-kompiled
extracted="$scratch/extracted-solution-program.mpy"
submitted_json=/tmp/audit-work/runs/submitted-program.json
extracted_json=/tmp/audit-work/runs/extracted-proof-program.json

echo "COMMAND[extract]: awk extracts the RHS of 'rule solutionProgram =>' from $scratch/verification.k"
awk '
  /rule solutionProgram =>/ {
    active = 1
    sub(/^.*=>[[:space:]]*/, "")
    if (length($0)) print
    next
  }
  active && /^endmodule/ { exit }
  active { print }
' "$scratch/verification.k" >"$extracted"
extract_status=$?
echo "EXIT[extract]: $extract_status"

# K rule syntax admits internal List units such as .Exprs and .Stmts.  The
# external program parser spells those same units as empty delimited lists.
sed -i \
  -e 's/ListExpr(\.Exprs)/ListExpr()/g' \
  -e 's/\.Stmts),/),/g' \
  "$extracted"
normalize_status=$?
echo "COMMAND[normalize]: sed internal empty-list units to program-syntax empty lists"
echo "EXIT[normalize]: $normalize_status"

echo "COMMAND[kast-submitted]: kast $scratch/solution.mpy --definition $definition --module MPY-VERIFICATION --sort Program --output json --output-file $submitted_json"
kast "$scratch/solution.mpy" \
  --definition "$definition" \
  --module MPY-VERIFICATION \
  --sort Program \
  --output json \
  --output-file "$submitted_json"
submitted_status=$?
echo "EXIT[kast-submitted]: $submitted_status"

echo "COMMAND[kast-proof-rhs]: kast $extracted --definition $definition --module MPY-VERIFICATION --sort Program --output json --output-file $extracted_json"
kast "$extracted" \
  --definition "$definition" \
  --module MPY-VERIFICATION \
  --sort Program \
  --output json \
  --output-file "$extracted_json"
proof_status=$?
echo "EXIT[kast-proof-rhs]: $proof_status"

sha256sum "$submitted_json" "$extracted_json"
cmp --silent "$submitted_json" "$extracted_json"
compare_status=$?
echo "COMMAND[compare]: cmp --silent $submitted_json $extracted_json"
echo "EXIT[compare]: $compare_status"

if [[ "$extract_status" -ne 0 || "$normalize_status" -ne 0 || "$submitted_status" -ne 0 || "$proof_status" -ne 0 || "$compare_status" -ne 0 ]]; then
  echo "CONSTRUCTOR_PINNING=FAIL"
  exit 1
fi
echo "CONSTRUCTOR_PINNING=PASS"
