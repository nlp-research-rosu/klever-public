#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: print every immutable Stage 4 Lean source with line numbers'
while IFS= read -r source; do
  printf '\n--- %s ---\n' "$source"
  nl -ba "$source"
done < <(
  find /reference/klean-generation/generated \
    -type f -name '*.lean' -printf '%p\n' | sort
)
