#!/usr/bin/env bash
set -euo pipefail

definition=/reference/k-proof/verification-kompiled/definition.kore
symbols=(
  "Lbl'Unds'-Int'Unds'"
  "Lbl'Unds'andBool'Unds'"
  "Lbl'Unds-LT-'Int'Unds'"
  "Lbl'Unds-LT-Eqls'Int'Unds'"
  "Lbl'UndsPerc'Int'Unds'"
  "Lbl'UndsPlus'Int'Unds'"
  "Lbl'UndsSlsh'Int'Unds'"
  "Lbl'UndsStar'Int'Unds'"
)

for symbol in "${symbols[@]}"; do
  printf 'SYMBOL %s\n' "$symbol"
  rg -n -F "symbol $symbol" "$definition"
done
