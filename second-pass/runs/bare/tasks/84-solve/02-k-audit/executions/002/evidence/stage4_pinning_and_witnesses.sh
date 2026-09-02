#!/usr/bin/env bash
set -uo pipefail
export PATH="/root/.nix-profile/bin:$PATH"

work=/tmp/audit-work/84-solve
definition="$work/verification-kompiled"
concrete_definition="$work/concrete-kompiled"
parsed="$work/parsed-solution.json"
embedded="$work/embedded-solution.json"
status=0

printf 'COMMAND kast solution.mpy --definition verification-kompiled --module MPY-SYNTAX --sort Pgm --output json\n'
kast "$work/solution.mpy" \
  --definition "$definition" \
  --module MPY-SYNTAX \
  --sort Pgm \
  --output json \
  --output-file "$parsed"
parsed_exit=$?
printf 'PARSED_KAST_EXIT %d\n' "$parsed_exit"

printf 'COMMAND kast --expression solutionProgram --definition verification-kompiled --module VERIFICATION --sort Pgm --expand-macros --output json\n'
kast \
  --expression solutionProgram \
  --definition "$definition" \
  --module VERIFICATION \
  --sort Pgm \
  --expand-macros \
  --output json \
  --output-file "$embedded"
embedded_exit=$?
printf 'EMBEDDED_KAST_EXIT %d\n' "$embedded_exit"

cmp -s "$parsed" "$embedded"
identity_exit=$?
printf 'CONSTRUCTOR_JSON_BYTE_IDENTITY_EXIT %d\n' "$identity_exit"
sha256sum "$parsed" "$embedded"
if [[ "$parsed_exit" -ne 0 || "$embedded_exit" -ne 0 || "$identity_exit" -ne 0 ]]; then
  status=1
fi

# One witness from each range claim.  Every claim has an unconditional,
# ground start term; these inputs witness one checkInput computation inside
# each range.
witnesses=(0 1000 2000 3000 4000 5000 6000 7000 8000 9000 10000)
for value in "${witnesses[@]}"; do
  canonical=$(
    PYTHONPATH=/reference python3 -c \
      'import sys; from canonical import solve; print(solve(int(sys.argv[1])))' \
      "$value"
  )
  canonical_exit=$?
  candidate=$(
    PYTHONPATH=/candidate python3 -c \
      'import sys; from solution import solve; print(solve(int(sys.argv[1])))' \
      "$value"
  )
  candidate_exit=$?
  output=$(krun "$work/solution.mpy" \
    --definition "$concrete_definition" -cN="$value" 2>&1)
  krun_exit=$?
  printf 'WITNESS %s CANONICAL %s CANDIDATE %s CANONICAL_EXIT %d CANDIDATE_EXIT %d KRUN_EXIT %d\n' \
    "$value" "$canonical" "$candidate" \
    "$canonical_exit" "$candidate_exit" "$krun_exit"
  if [[ "$canonical_exit" -ne 0 || "$candidate_exit" -ne 0 || "$krun_exit" -ne 0 ]]; then
    status=1
    continue
  fi
  if [[ "$canonical" != "$candidate" ]]; then
    printf 'PYTHON_MISMATCH %s\n' "$value"
    status=1
  elif grep -Fq "VStr ( \"$canonical\" ) ~> .K" <<<"$output"; then
    printf 'THREE_WAY_MATCH %s\n' "$value"
  else
    printf 'K_MISMATCH %s\n' "$value"
    printf '%s\n' "$output"
    status=1
  fi
done

printf 'WITNESS_COUNT %d\n' "${#witnesses[@]}"
printf 'OVERALL_EXIT %d\n' "$status"
exit "$status"
