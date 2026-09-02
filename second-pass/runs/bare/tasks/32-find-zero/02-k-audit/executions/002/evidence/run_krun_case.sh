#!/usr/bin/env bash
set -euo pipefail

case_name=$1
program_file=/tmp/audit-work/32-find-zero/solution.mpy
definition=/tmp/audit-work/32-find-zero/semantic-concrete-haskell-kompiled
program_term=$(<"$program_file")

case "$case_name" in
  linear)
    arguments='list(ListItem(rat(1, 1)) ListItem(rat(2, 1)))'
    ;;
  empty)
    arguments='list(.List)'
    ;;
  zero)
    arguments='list(ListItem(rat(0, 1)) ListItem(rat(1, 1)))'
    ;;
  expansion)
    arguments='list(ListItem(rat(-8, 1)) ListItem(rat(0, 1)) ListItem(rat(0, 1)) ListItem(rat(1, 1)))'
    ;;
  endpoint)
    arguments='list(ListItem(rat(1, 1)) ListItem(rat(1, 1)))'
    ;;
  rounding-witness)
    arguments='list(ListItem(rat(9007199254740993, 1)) ListItem(rat(-18014398509481984, 1)))'
    ;;
  *)
    printf 'unknown case: %s\n' "$case_name" >&2
    exit 64
    ;;
esac

krun --definition "$definition" \
  -cPGM="$program_term ;; Invoke(\"find_zero\", $arguments)" \
  --output pretty
