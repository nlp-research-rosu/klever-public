#!/usr/bin/env bash
set -uo pipefail

echo 'COMMAND: find /candidate -printf "%y %p -> %l\n" | sort'
find /candidate -printf '%y %p -> %l\n' | sort
find_status=$?
echo "EXIT_STATUS(find): ${find_status}"

echo 'COMMAND: cmp -s /reference/prompt.py /candidate/prompt.py'
cmp -s /reference/prompt.py /candidate/prompt.py
prompt_status=$?
echo "EXIT_STATUS(prompt cmp): ${prompt_status}"

echo 'COMMAND: cmp -s /reference/py2mpy.py /candidate/py2mpy.py'
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
echo "EXIT_STATUS(translator cmp): ${translator_status}"

echo 'COMMAND: diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
semantics_status=$?
echo "EXIT_STATUS(semantics diff): ${semantics_status}"

echo 'COMMAND: test required generation-record artifacts'
missing_status=0
for artifact in run-input.json metrics.json codex-last.txt codex-output.log; do
  if test -e "/candidate/${artifact}"; then
    printf 'PRESENT regular=%s symlink=%s %s\n' \
      "$(test -f "/candidate/${artifact}" && echo yes || echo no)" \
      "$(test -L "/candidate/${artifact}" && echo yes || echo no)" \
      "${artifact}"
  else
    echo "MISSING ${artifact}"
    missing_status=1
  fi
done
echo "EXIT_STATUS(required-artifact check): ${missing_status}"

echo 'COMMAND: sha256sum trusted and candidate source artifacts'
sha256sum \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k
hash_status=$?
echo "EXIT_STATUS(sha256sum): ${hash_status}"

if (( find_status != 0 || prompt_status != 0 || translator_status != 0 ||
      semantics_status != 0 || hash_status != 0 )); then
  exit 1
fi
exit 0
