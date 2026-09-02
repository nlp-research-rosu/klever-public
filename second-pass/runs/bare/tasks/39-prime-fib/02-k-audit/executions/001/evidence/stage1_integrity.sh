#!/usr/bin/env bash
set -u
set -o pipefail
set -x

if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  stat -c '%F %N' /reference/reference-semantics
  printf 'INFRASTRUCTURE_BREACH=reference-semantics-present\n'
  exit 90
fi

stat -c '%F %N' /candidate /reference
find -P /candidate -maxdepth 1 -printf '%y\t%f\t%l\n' | sort
find -P /candidate -type l -printf '%p -> %l\n'
find -P /candidate/codex-trace -type f -printf '%p\t%s bytes\n' | sort
find -P /reference -maxdepth 1 -printf '%y\t%f\t%l\n' | sort

sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py

cmp /reference/prompt.py /candidate/prompt.py
printf 'prompt_cmp_exit=%s\n' "$?"
cmp /reference/py2mpy.py /candidate/py2mpy.py
printf 'translator_cmp_exit=%s\n' "$?"

for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k \
  verification.k spec.k concrete-spec.k prove.sh
do
  test -f "/candidate/${artifact}" && test ! -L "/candidate/${artifact}"
  printf 'required_regular_file=%s\n' "${artifact}"
done

printf 'candidate_compiled_directories_ignored=%s\n' \
  "$(find -P /candidate -maxdepth 1 -type d -name '*-kompiled' | wc -l)"
printf 'SCRIPT_EXIT=0\n'
