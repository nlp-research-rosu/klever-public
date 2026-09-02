#!/usr/bin/env bash
set -u

expected_candidate=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  solution-program.k
  verification.k
  spec.k
  definition.k
  prove.sh
)

printf 'Rendered mode: GENERATED_SEMANTICS\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'MODE_BOUNDARY: BREACH: /reference/reference-semantics exists\n'
else
  printf 'MODE_BOUNDARY: OK: /reference/reference-semantics is absent\n'
fi

printf 'Trusted mount entries:\n'
find /reference -maxdepth 2 -printf '%y %p -> %l\n' | sort

printf 'Required candidate source/control artifacts:\n'
for name in "${expected_candidate[@]}"; do
  path="/candidate/$name"
  if [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
  elif [[ -f "$path" ]]; then
    stat -c 'REGULAR %n size=%s mode=%a' "$path"
  elif [[ -e "$path" ]]; then
    stat -c 'MISTYPED %n type=%F mode=%a' "$path"
  else
    printf 'MISSING %s\n' "$path"
  fi
done

printf 'All candidate symlinks (must be empty):\n'
find /candidate -type l -printf '%p -> %l\n' | sort

printf 'Structured trace files:\n'
find /candidate/codex-trace -type f -printf '%y %p size=%s\n' | sort

printf 'Prompt byte comparison:\n'
cmp /candidate/prompt.py /reference/prompt.py
printf 'prompt_cmp_status=%d\n' "$?"

printf 'Translator byte comparison:\n'
cmp /candidate/py2mpy.py /reference/py2mpy.py
printf 'translator_cmp_status=%d\n' "$?"

printf 'Relevant SHA-256 values:\n'
sha256sum \
  /reference/prompt.py \
  /candidate/prompt.py \
  /reference/py2mpy.py \
  /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/solution-program.k \
  /candidate/verification.k \
  /candidate/spec.k

printf 'Untrusted control JSON syntax:\n'
python3 -m json.tool /candidate/run-input.json
python3 -m json.tool /candidate/metrics.json

printf 'Untrusted final claim:\n'
sed -n '1,200p' /candidate/codex-last.txt

printf 'Untrusted generation log size and bounded endpoints:\n'
wc -l -c /candidate/codex-output.log
sed -n '1,80p' /candidate/codex-output.log
tail -n 80 /candidate/codex-output.log
