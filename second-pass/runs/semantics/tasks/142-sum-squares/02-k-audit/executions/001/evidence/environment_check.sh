#!/usr/bin/env bash
set -u

for command in kompile kprove krun kast python3; do
  printf 'COMMAND: command -v %s\n' "$command"
  command -v "$command"
  printf 'EXIT_STATUS: %s\n' "$?"
done

printf '%s\n' 'COMMAND: kompile --version'
kompile --version
printf 'EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: kprove --version'
kprove --version
printf 'EXIT_STATUS: %s\n' "$?"
