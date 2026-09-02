#!/usr/bin/env bash
set +e

generated=/reference/klean-generation/generated

printf 'COMMAND: find %q -maxdepth 4 -printf %%y\\ %%P\\\\n | sort\n' "$generated"
find "$generated" -maxdepth 4 -printf '%y %P\n' | sort
printf 'EXIT_CODE: %d\n' "$?"

printf 'COMMAND: find %q -type f -print0 | sort -z | xargs -0 sha256sum\n' "$generated"
find "$generated" -type f -print0 | sort -z | xargs -0 sha256sum
printf 'EXIT_CODE: %d\n' "$?"

printf 'COMMAND: python -m json.tool %q\n' "$generated/obligation-map.json"
python -m json.tool "$generated/obligation-map.json"
printf 'EXIT_CODE: %d\n' "$?"

printf 'COMMAND: nl -ba %q\n' \
  "$generated/Klean16CountDistinctCharacters/Lemmas.lean"
nl -ba "$generated/Klean16CountDistinctCharacters/Lemmas.lean"
printf 'EXIT_CODE: %d\n' "$?"

printf 'COMMAND: rg -n %q %q\n' \
  '\b(sorry|admit|unsafe)\b|^\s*(axiom|opaque|theorem)\s+|KleanTarget' \
  "$generated"
rg -n \
  '\b(sorry|admit|unsafe)\b|^\s*(axiom|opaque|theorem)\s+|KleanTarget' \
  "$generated"
scan_status=$?
printf 'EXIT_CODE: %d\n' "$scan_status"

printf 'COMMAND: test ! -e /candidate\n'
test ! -e /candidate
printf 'EXIT_CODE: %d\n' "$?"
