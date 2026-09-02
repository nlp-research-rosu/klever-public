#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruct-001
evidence=/audit-output/evidence
definition=$scratch/runtime-fresh-kompiled
status=0

run_to_log() {
  name=$1
  shift
  log=$evidence/"$name".log
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$log" 2>&1
  rc=$?
  printf '%s exit=%d log=%s\n' "$name" "$rc" "$log"
  if (( rc != 0 )); then
    status=1
  fi
}

cd "$scratch" || exit 2

printf '$ python3 %q\n' "$evidence/extract_claim_program.py"
python3 "$evidence/extract_claim_program.py"
rc=$?
printf 'extract_claim_program exit=%d\n' "$rc"
if (( rc != 0 )); then
  status=1
fi

run_to_log \
  stage4_kast_solution \
  kast solution.mpy --definition "$definition" --sort Module --output kore
run_to_log \
  stage4_kast_claim_program_normalized \
  kast "$evidence/claim_program_extracted_normalized.mpy" \
    --definition "$definition" --sort Module --output kore

printf '$ cmp %q %q\n' \
  "$evidence/stage4_kast_solution.log" \
  "$evidence/stage4_kast_claim_program_normalized.log"
cmp \
  "$evidence/stage4_kast_solution.log" \
  "$evidence/stage4_kast_claim_program_normalized.log"
rc=$?
printf 'constructor_kore_cmp exit=%d\n' "$rc"
if (( rc != 0 )); then
  status=1
fi
sha256sum \
  "$evidence/stage4_kast_solution.log" \
  "$evidence/stage4_kast_claim_program_normalized.log"

printf 'overall=%d\n' "$status"
exit "$status"
