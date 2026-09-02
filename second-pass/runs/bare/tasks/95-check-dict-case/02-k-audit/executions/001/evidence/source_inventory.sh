#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/candidate-src

for file in semantic.k program.k verification.k spec.k; do
  echo "===== $file (numbered source) ====="
  nl -ba "$scratch/$file"
done

echo "===== declarations, rules, claims, and attributes ====="
rg -n \
  '^\s*(syntax|configuration|rule|claim)|\[(function|functional|total|simplification|priority|priorities|owise)' \
  "$scratch/semantic.k" "$scratch/program.k" \
  "$scratch/verification.k" "$scratch/spec.k"

echo "===== source counts ====="
for file in semantic.k program.k verification.k spec.k; do
  printf '%s rules=' "$file"
  rg -c '^\s*rule\b' "$scratch/$file" || true
  printf '%s claims=' "$file"
  rg -c '^\s*claim\b' "$scratch/$file" || true
  printf '%s syntax-statements=' "$file"
  rg -c '^\s*syntax\b' "$scratch/$file" || true
done

echo "===== priority/simplification/owise scan ====="
rg -n '\b(priority|priorities|simplification|owise)\b' \
  "$scratch/semantic.k" "$scratch/program.k" \
  "$scratch/verification.k" "$scratch/spec.k" || true
