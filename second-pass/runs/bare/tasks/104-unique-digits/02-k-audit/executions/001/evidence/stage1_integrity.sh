#!/usr/bin/env bash
set -u

status=0

printf '%s\n' 'MODE CHECK'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf '%s\n' 'FAIL: /reference/reference-semantics exists in GENERATED_SEMANTICS mode'
  status=1
else
  printf '%s\n' 'PASS: /reference/reference-semantics is absent'
fi

printf '%s\n' 'TRUSTED/CANDIDATE TYPES AND SYMLINK TARGETS'
find /reference -maxdepth 3 -printf '%y %m %p -> %l\n' | sort
find /candidate -maxdepth 6 -printf '%y %m %p -> %l\n' | sort

printf '%s\n' 'REQUIRED SOURCE ARTIFACTS'
required=(
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
  prove.sh
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
)
for name in "${required[@]}"; do
  path="/candidate/$name"
  if [[ ! -e "$path" && ! -L "$path" ]]; then
    printf 'MISSING %s\n' "$path"
    status=1
  elif [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
    status=1
  elif [[ ! -f "$path" ]]; then
    printf 'MISTYPED %s\n' "$path"
    status=1
  else
    printf 'REGULAR %s\n' "$path"
  fi
done

trace_count=$(find /candidate/codex-trace -type f -name '*.jsonl' | wc -l)
printf 'STRUCTURED_TRACE_COUNT %s\n' "$trace_count"
if [[ "$trace_count" -eq 0 ]]; then
  status=1
fi
if find /candidate/codex-trace -type l | grep -q .; then
  printf '%s\n' 'SYMLINK FOUND IN STRUCTURED TRACE'
  status=1
fi

printf '%s\n' 'BYTE IDENTITY'
if cmp -s /candidate/prompt.py /reference/prompt.py; then
  printf '%s\n' 'PASS candidate prompt == trusted prompt'
else
  printf '%s\n' 'FAIL candidate prompt != trusted prompt'
  status=1
fi
if cmp -s /candidate/py2mpy.py /reference/py2mpy.py; then
  printf '%s\n' 'PASS candidate translator == trusted translator'
else
  printf '%s\n' 'FAIL candidate translator != trusted translator'
  status=1
fi

printf '%s\n' 'SHA256'
sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k \
  /candidate/prove.sh /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log \
  /candidate/codex-trace/2026/07/22/*.jsonl

printf '%s\n' 'TOOLCHAIN'
for tool in kup kompile krun kprove kore-exec; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf '%s=%s\n' "$tool" "$(command -v "$tool")"
  else
    printf '%s=MISSING\n' "$tool"
  fi
done
kompile --version
krun --version
kprove --version

exit "$status"
