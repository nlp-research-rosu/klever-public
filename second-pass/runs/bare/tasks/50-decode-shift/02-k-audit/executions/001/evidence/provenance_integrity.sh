#!/usr/bin/env bash
set -u

status=0
required_candidate=(
  /candidate/run-input.json
  /candidate/metrics.json
  /candidate/codex-last.txt
  /candidate/codex-output.log
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/semantic.k
  /candidate/spec.k
  /candidate/verification.k
)
trusted=(
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
)

for path in "${required_candidate[@]}" "${trusted[@]}"; do
  if [[ ! -e "$path" ]]; then
    printf 'MISSING\t%s\n' "$path"
    status=1
  elif [[ -L "$path" ]]; then
    printf 'SYMLINK\t%s -> %s\n' "$path" "$(readlink "$path")"
    status=1
  elif [[ ! -f "$path" ]]; then
    printf 'MISTYPED\t%s\n' "$path"
    status=1
  else
    printf 'REGULAR_FILE\t%s\t%s bytes\n' "$path" "$(stat -c %s "$path")"
  fi
done

trace_count=$(find /candidate/codex-trace -type f -name '*.jsonl' | wc -l)
printf 'STRUCTURED_TRACE_COUNT\t%s\n' "$trace_count"
if (( trace_count == 0 )); then
  status=1
fi

if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'MODE_BREACH\t/reference/reference-semantics exists in GENERATED_SEMANTICS mode\n'
  status=1
else
  printf 'MODE_OK\t/reference/reference-semantics absent\n'
fi

cmp -s /reference/prompt.py /candidate/prompt.py
prompt_status=$?
printf 'PROMPT_BYTE_CMP_STATUS\t%s\n' "$prompt_status"
(( prompt_status == 0 )) || status=1

cmp -s /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
printf 'TRANSLATOR_BYTE_CMP_STATUS\t%s\n' "$translator_status"
(( translator_status == 0 )) || status=1

sha256sum /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/spec.k /candidate/verification.k

exit "$status"
