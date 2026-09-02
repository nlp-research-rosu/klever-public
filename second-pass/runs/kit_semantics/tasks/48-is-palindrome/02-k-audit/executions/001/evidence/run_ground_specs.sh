#!/usr/bin/env bash
set -u

work=/tmp/audit-work/48-is-palindrome-audit
definition="$work/verification-review4-kompiled"
cd "$work" || exit 90

run_case() {
  file="$1"
  module="$2"
  label="$3"
  printf 'COMMAND: kprove %s --definition %s --spec-module %s --claims %s.%s\n' \
    "$file" "$definition" "$module" "$module" "$label"
  kprove "$file" \
    --definition "$definition" \
    --spec-module "$module" \
    --claims "$module.$label"
  status=$?
  printf 'EXIT_STATUS=%s\n' "$status"
  return "$status"
}

printf 'COMMAND: python3 /audit-output/evidence/instantiate_ground_specs.py\n'
python3 /audit-output/evidence/instantiate_ground_specs.py
status=$?
printf 'EXIT_STATUS=%s\n' "$status"
[[ "$status" -eq 0 ]] || exit "$status"

run_case spec-ground-empty.k SPEC-GROUND-EMPTY ground-empty || exit $?
run_case spec-ground-aba.k SPEC-GROUND-ABA ground-aba || exit $?
run_case spec-ground-ab.k SPEC-GROUND-AB ground-ab || exit $?
run_case spec-ground-emoji.k SPEC-GROUND-EMOJI ground-emoji || exit $?
printf 'GROUND_KPROVE_RESULT=PASS\n'
