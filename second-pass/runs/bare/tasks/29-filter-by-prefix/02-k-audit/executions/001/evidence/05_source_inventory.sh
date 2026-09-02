#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: find candidate top-level K source files'
find /candidate -maxdepth 1 -type f -name '*.k' -printf '%f %s bytes\n' | sort
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: enumerate module/import/configuration/syntax/rule/claim declarations'
rg -n \
  '^[[:space:]]*(requires|module|endmodule|imports|configuration|syntax|rule|claim)([[:space:]]|$)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: enumerate attributes relevant to proof soundness'
rg -n \
  '\[(function|functional|total|simplification|concrete|priority|opaque|trusted|label)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
printf 'EXIT: %s\n' "$?"
