#!/usr/bin/env bash
set +e

printf 'COMMAND: python3 trusted/py2mpy.py solution.py > solution.regenerated.mpy\n'
python3 trusted/py2mpy.py solution.py > solution.regenerated.mpy
status=$?
printf 'EXIT STATUS: %s\n' "$status"

printf 'COMMAND: cmp -s solution.regenerated.mpy candidate-source/solution.mpy\n'
cmp -s solution.regenerated.mpy candidate-source/solution.mpy
status=$?
printf 'EXIT STATUS: %s\n' "$status"

printf 'COMMAND: sha256sum solution.regenerated.mpy candidate-source/solution.mpy\n'
sha256sum solution.regenerated.mpy candidate-source/solution.mpy
status=$?
printf 'EXIT STATUS: %s\n' "$status"

printf 'COMMAND: python3 /audit-output/evidence/differential_test.py\n'
python3 /audit-output/evidence/differential_test.py
status=$?
printf 'EXIT STATUS: %s\n' "$status"
exit "$status"
