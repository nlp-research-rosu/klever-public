#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/50-decode-shift
src="$scratch/candidate-src"
trusted_translator="$scratch/trusted/py2mpy.py"
mutation_source=/audit-output/evidence/solution-body-mutation.py
mutation_mpy="$src/solution-body-mutation.mpy"

original_norm=$(tr -d '[:space:]' < "$src/solution.mpy")
spec_norm=$(tr -d '[:space:]' < "$src/spec.k")
original_count=$(awk -v text="$spec_norm" -v needle="$original_norm" '
  BEGIN {
    count = 0
    while ((position = index(text, needle)) != 0) {
      count++
      text = substr(text, position + length(needle))
    }
    print count
  }
')
printf 'ORIGINAL_MPY_NORMALIZED_OCCURRENCES_IN_SPEC\t%s\n' "$original_count"

python3 "$trusted_translator" "$mutation_source" > "$mutation_mpy"
translate_status=$?
printf 'MUTATION_TRANSLATOR_EXIT_STATUS\t%s\n' "$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

mutation_norm=$(tr -d '[:space:]' < "$mutation_mpy")
mutation_count=$(awk -v text="$spec_norm" -v needle="$mutation_norm" '
  BEGIN {
    count = 0
    while ((position = index(text, needle)) != 0) {
      count++
      text = substr(text, position + length(needle))
    }
    print count
  }
')
printf 'MUTATED_MPY_NORMALIZED_OCCURRENCES_IN_SPEC\t%s\n' "$mutation_count"

printf 'ORIGINAL_KRUN_COMMAND\tkrun solution.mpy --definition semantic-concrete-kompiled -cINPUT=cons(102,nil)\n'
original_output=$(krun "$src/solution.mpy" \
  --definition "$src/semantic-concrete-kompiled" \
  '-cINPUT=cons(102,nil)')
original_status=$?
printf 'ORIGINAL_KRUN_EXIT_STATUS\t%s\n' "$original_status"
printf '%s\n' "$original_output"

printf 'MUTATED_KRUN_COMMAND\tkrun solution-body-mutation.mpy --definition semantic-concrete-kompiled -cINPUT=cons(102,nil)\n'
mutation_output=$(krun "$mutation_mpy" \
  --definition "$src/semantic-concrete-kompiled" \
  '-cINPUT=cons(102,nil)')
mutation_status=$?
printf 'MUTATED_KRUN_EXIT_STATUS\t%s\n' "$mutation_status"
printf '%s\n' "$mutation_output"

test "$original_count" -eq 1 || exit 1
test "$mutation_count" -eq 0 || exit 1
test "$original_status" -eq 0 || exit 1
test "$mutation_status" -eq 0 || exit 1
printf '%s' "$original_output" | rg -Fq 'cons ( 97 , nil )'
printf '%s' "$mutation_output" | rg -Fq 'cons ( 98 , nil )'
