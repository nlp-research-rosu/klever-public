#!/usr/bin/env bash
set -u

printf '%s\n' "COMMAND: stat -c '%s' /candidate/spec.json"
stat -c '%s' /candidate/spec.json
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' "COMMAND: rg -o 'finishLoop' /candidate/spec.json"
rg -o 'finishLoop' /candidate/spec.json
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' "COMMAND: rg -n 'finishLoop' /candidate/spec.k /candidate/verification.k"
rg -n 'finishLoop' /candidate/spec.k /candidate/verification.k
printf 'EXIT_STATUS: %s (1 means absent)\n' "$?"

printf '%s\n' "COMMAND: rg -c '^#Top$' /candidate/prove.log"
rg -c '^#Top$' /candidate/prove.log
printf 'EXIT_STATUS: %s\n' "$?"
