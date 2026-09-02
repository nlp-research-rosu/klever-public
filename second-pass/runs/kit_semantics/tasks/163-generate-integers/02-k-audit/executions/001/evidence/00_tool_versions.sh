#!/usr/bin/env bash
set -uo pipefail

printf '%s\n' 'COMMAND: kompile --version'
kompile --version
printf 'STATUS [kompile version]: %s\n' "$?"

printf '%s\n' 'COMMAND: kprove --version'
kprove --version
printf 'STATUS [kprove version]: %s\n' "$?"

printf '%s\n' 'COMMAND: krun --version'
krun --version
printf 'STATUS [krun version]: %s\n' "$?"

printf '%s\n' 'COMMAND: python3 --version'
python3 --version
printf 'STATUS [python version]: %s\n' "$?"
