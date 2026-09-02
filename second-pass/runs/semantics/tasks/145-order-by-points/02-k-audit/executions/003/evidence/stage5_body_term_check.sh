#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

printf '%s\n' 'COMMAND: rg -n -F #token("999","Int") body-mutated-kompiled/compiled.txt'
rg -n -F '#token("999","Int")' body-mutated-kompiled/compiled.txt
printf 'MUTATED_TERM_CHECK_EXIT_STATUS: %s\n' "$?"

printf '%s\n' 'COMMAND: rg -n -F #token("999","Int") verification-kompiled/compiled.txt'
rg -n -F '#token("999","Int")' verification-kompiled/compiled.txt
printf 'ORIGINAL_TERM_CHECK_EXIT_STATUS_EXPECTED_1: %s\n' "$?"
