#!/usr/bin/env bash
set -uo pipefail

root=/tmp/audit-work/fresh
sources=("$root/reference-semantics" "$root/verification.k")

echo "OPAQUE OR EXTERNALLY INTERPRETED DECLARATIONS"
rg -n 'no-evaluators|symbol\(' "${sources[@]}" || true

echo "FUNCTIONAL DECLARATIONS"
if ! rg -n '\bfunctional\b' "${sources[@]}"; then
  echo "NONE"
fi

echo "TOTAL DECLARATIONS"
rg -n '^\s*syntax .*\btotal\b' "${sources[@]}" || true

echo "PRIORITY RULE ATTRIBUTES"
rg -n '\[priority\(' "${sources[@]}" || true

echo "SIMPLIFICATION RULE ATTRIBUTES"
rg -n '\[simplification\]' "${sources[@]}" || true
