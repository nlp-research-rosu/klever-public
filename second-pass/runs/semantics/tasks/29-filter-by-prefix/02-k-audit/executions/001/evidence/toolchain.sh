#!/usr/bin/env bash
set -u

export PATH="/home/agent/.nix-profile/bin:$PATH"
status=0

printf '%s\n' 'COMMAND: command -v kompile'
command -v kompile
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kompile --version'
kompile --version
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: kprove --version'
kprove --version
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
