#!/usr/bin/env bash
set -u

echo 'COMMAND: test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics'
test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
echo "EXIT_STATUS: $?"

echo 'COMMAND: find /candidate -maxdepth 1 -printf "%y %f -> %l\n" | sort'
find /candidate -maxdepth 1 -printf '%y %f -> %l\n' | sort
echo "EXIT_STATUS: ${PIPESTATUS[0]}"

echo 'COMMAND: cmp /candidate/prompt.py /reference/prompt.py'
cmp /candidate/prompt.py /reference/prompt.py
echo "EXIT_STATUS: $?"

echo 'COMMAND: cmp /candidate/py2mpy.py /reference/py2mpy.py'
cmp /candidate/py2mpy.py /reference/py2mpy.py
echo "EXIT_STATUS: $?"

echo 'COMMAND: sha256sum prompt and translator pairs'
sha256sum /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py
echo "EXIT_STATUS: $?"

echo 'COMMAND: stat required candidate artifacts'
for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k \
  verification.k spec.k prove.sh; do
  if [[ -f "/candidate/$artifact" && ! -L "/candidate/$artifact" ]]; then
    printf 'OK regular non-symlink: %s\n' "$artifact"
  else
    printf 'INTEGRITY FAILURE: %s\n' "$artifact"
  fi
done
echo 'EXIT_STATUS: 0'

echo 'COMMAND: locate structured trace and reject symlinked trace entries'
find /candidate/codex-trace -printf '%y %p -> %l\n' | sort
trace_bad="$(find /candidate/codex-trace \( -type l -o ! -type d ! -type f \) -print)"
if [[ -n "$trace_bad" ]]; then
  printf 'INTEGRITY FAILURE trace entries:\n%s\n' "$trace_bad"
  echo 'EXIT_STATUS: 1'
else
  echo 'EXIT_STATUS: 0'
fi

echo 'COMMAND: python3 -m json.tool metadata files'
python3 -m json.tool /candidate/run-input.json
metadata_1=$?
python3 -m json.tool /candidate/metrics.json
metadata_2=$?
echo "EXIT_STATUS: run-input=$metadata_1 metrics=$metadata_2"

echo 'UNTRUSTED CLAIM: codex-last.txt'
sed -n '1,120p' /candidate/codex-last.txt
echo 'UNTRUSTED LOG SUMMARY: candidate generation commands/results'
rg -n 'kompile|kprove|krun|#Top|WarnStuck|RESULT:' /candidate/codex-output.log \
  | tail -n 120
echo "EXIT_STATUS: ${PIPESTATUS[0]}"
