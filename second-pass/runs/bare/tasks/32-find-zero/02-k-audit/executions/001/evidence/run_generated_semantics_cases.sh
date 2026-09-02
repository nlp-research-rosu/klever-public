#!/usr/bin/env bash
set -u

source_dir=${1:-/tmp/audit-work/32-find-zero-audit}
definition=${2:-/tmp/audit-work/32-find-zero-audit/audit-semantic-kompiled}
translated_program=$(<"${source_dir}/solution.mpy")

labels=(
  prompt-linear
  prompt-cubic
  midpoint-root
  expansion-positive
  expansion-negative
)

expressions=(
  'Invoke("find_zero", list(ListItem(rat(1, 1)) ListItem(rat(2, 1))))'
  'Invoke("find_zero", list(ListItem(rat(-6, 1)) ListItem(rat(11, 1)) ListItem(rat(-6, 1)) ListItem(rat(1, 1))))'
  'Invoke("find_zero", list(ListItem(rat(0, 1)) ListItem(rat(1, 1))))'
  'Invoke("find_zero", list(ListItem(rat(-8, 1)) ListItem(rat(0, 1)) ListItem(rat(0, 1)) ListItem(rat(1, 1))))'
  'Invoke("find_zero", list(ListItem(rat(8, 1)) ListItem(rat(0, 1)) ListItem(rat(0, 1)) ListItem(rat(1, 1))))'
)

sha256sum "${source_dir}/solution.mpy"
overall_status=0
for index in "${!labels[@]}"; do
  pgm="${translated_program} ;; ${expressions[$index]}"
  printf '\nCASE: %s\n' "${labels[$index]}"
  printf 'COMMAND: krun --definition %q -cPGM=%q --output pretty\n' \
    "$definition" "$pgm"
  krun --definition "$definition" -cPGM="$pgm" --output pretty
  case_status=$?
  printf 'CASE_EXIT_STATUS: %d\n' "$case_status"
  if [[ "$case_status" -ne 0 ]]; then
    overall_status=$case_status
  fi
done

exit "$overall_status"
