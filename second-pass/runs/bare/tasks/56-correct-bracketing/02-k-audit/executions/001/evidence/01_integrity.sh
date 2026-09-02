#!/usr/bin/env bash
set -u

echo 'AUDITOR COMMAND: sha256sum trusted and candidate prompt/translator'
sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: cmp -s /reference/prompt.py /candidate/prompt.py'
cmp -s /reference/prompt.py /candidate/prompt.py
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: cmp -s /reference/py2mpy.py /candidate/py2mpy.py'
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics'
test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: enumerate candidate root entries and source symlinks'
find /candidate -mindepth 1 -maxdepth 1 -printf '%y\t%f\t%l\n' | sort
find /candidate -type l -printf 'SYMLINK\t%p\t%l\n' | sort
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: stat required candidate artifacts'
for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k \
  verification.k spec.k prove.sh
do
  stat -c '%F\t%a\t%n' "/candidate/$artifact"
done
status=$?
echo "EXIT STATUS: $status"

echo 'AUDITOR COMMAND: enumerate structured trace files'
find /candidate/codex-trace -type f -printf '%y\t%p\t%l\n' | sort
status=$?
echo "EXIT STATUS: $status"
