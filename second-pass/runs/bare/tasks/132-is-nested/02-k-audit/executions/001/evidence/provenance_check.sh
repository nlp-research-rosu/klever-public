#!/usr/bin/env bash
set -uo pipefail

required=(
  prompt.py py2mpy.py solution.py solution.mpy semantic.k spec.k
  verification.k prove.sh run-input.json metrics.json codex-last.txt
  codex-output.log
)

status=0
for name in "${required[@]}"; do
  path="/candidate/$name"
  if [[ ! -e "$path" && ! -L "$path" ]]; then
    printf 'MISSING %s\n' "$path"
    status=1
  elif [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
    status=1
  elif [[ ! -f "$path" ]]; then
    printf 'MISTYPED %s mode=%s\n' "$path" "$(stat -c '%F' "$path")"
    status=1
  else
    printf 'REGULAR %s size=%s sha256=%s\n' \
      "$path" "$(stat -c '%s' "$path")" "$(sha256sum "$path" | cut -d' ' -f1)"
  fi
done

if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'MODE_BREACH /reference/reference-semantics exists\n'
  status=1
else
  printf 'MODE_OK /reference/reference-semantics absent\n'
fi

for name in canonical.py prompt.py py2mpy.py; do
  path="/reference/$name"
  if [[ -L "$path" ]]; then
    printf 'TRUSTED_SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
    status=1
  elif [[ ! -f "$path" ]]; then
    printf 'TRUSTED_MISSING_OR_MISTYPED %s\n' "$path"
    status=1
  else
    printf 'TRUSTED_REGULAR %s size=%s sha256=%s\n' \
      "$path" "$(stat -c '%s' "$path")" "$(sha256sum "$path" | cut -d' ' -f1)"
  fi
done

for name in prompt.py py2mpy.py; do
  if cmp -s "/candidate/$name" "/reference/$name"; then
    printf 'IDENTICAL candidate/%s reference/%s\n' "$name" "$name"
  else
    printf 'CHANGED candidate/%s reference/%s\n' "$name" "$name"
    status=1
  fi
done

trace_count=$(find /candidate/codex-trace -type f -name '*.jsonl' | wc -l)
symlink_count=$(find /candidate -type l | wc -l)
printf 'STRUCTURED_TRACE_FILES %s\n' "$trace_count"
printf 'CANDIDATE_SYMLINKS %s\n' "$symlink_count"
find /candidate/codex-trace -type f -name '*.jsonl' -printf 'TRACE %p size=%s\n' | sort

exit "$status"
