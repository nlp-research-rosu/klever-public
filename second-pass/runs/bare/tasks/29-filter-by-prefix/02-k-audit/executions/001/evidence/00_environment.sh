#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: pwd'
pwd
printf 'EXIT: %s\n\n' "$?"

for tool in python3 kompile krun kprove
do
  printf 'COMMAND: command -v %s\n' "$tool"
  command -v "$tool"
  printf 'EXIT: %s\n' "$?"
done
printf '\n'

printf '%s\n' 'COMMAND: python3 --version'
python3 --version
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: kompile --version'
kompile --version
printf 'EXIT: %s\n\n' "$?"

printf '%s\n' 'COMMAND: kprove --version'
kprove --version
printf 'EXIT: %s\n' "$?"
