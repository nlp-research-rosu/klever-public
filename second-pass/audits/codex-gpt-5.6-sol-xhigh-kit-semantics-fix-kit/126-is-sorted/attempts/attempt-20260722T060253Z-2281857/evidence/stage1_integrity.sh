#!/usr/bin/env bash
set +e

candidate=/candidate
reference=/reference
status=0

required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy verification.k spec.k
  prove.sh PROOF.md
)

for name in "${required[@]}"; do
  path="$candidate/$name"
  if [[ ! -e "$path" && ! -L "$path" ]]; then
    printf 'REQUIRED MISSING %s\n' "$name"
    status=1
  elif [[ -L "$path" ]]; then
    printf 'REQUIRED SYMLINK %s -> %s\n' "$name" "$(readlink "$path")"
    status=1
  elif [[ ! -f "$path" ]]; then
    printf 'REQUIRED WRONG_TYPE %s type=%s\n' "$name" "$(stat -c %F "$path")"
    status=1
  else
    printf 'REQUIRED OK %s sha256=%s\n' "$name" "$(sha256sum "$path" | cut -d' ' -f1)"
  fi
done

for name in canonical.py prompt.py py2mpy.py; do
  path="$reference/$name"
  if [[ ! -f "$path" || -L "$path" ]]; then
    printf 'TRUSTED REQUIRED INVALID %s\n' "$path"
    status=1
  else
    printf 'TRUSTED OK %s sha256=%s\n' "$name" "$(sha256sum "$path" | cut -d' ' -f1)"
  fi
done

trace_count=$(find "$candidate/codex-trace" -type f -name '*.jsonl' 2>/dev/null | wc -l)
printf 'STRUCTURED_TRACE_COUNT %s\n' "$trace_count"
if [[ "$trace_count" -eq 0 ]]; then
  printf 'STRUCTURED_TRACE MISSING\n'
  status=1
fi
if find "$candidate/codex-trace" -type l -print -quit 2>/dev/null | grep -q .; then
  printf 'STRUCTURED_TRACE SYMLINK_FOUND\n'
  status=1
fi

for pair in "prompt.py:prompt.py" "py2mpy.py:py2mpy.py"; do
  c_name=${pair%%:*}
  r_name=${pair##*:}
  if cmp -s "$candidate/$c_name" "$reference/$r_name"; then
    printf 'IDENTITY OK candidate/%s reference/%s\n' "$c_name" "$r_name"
  else
    printf 'IDENTITY FAIL candidate/%s reference/%s\n' "$c_name" "$r_name"
    diff -u "$reference/$r_name" "$candidate/$c_name"
    status=1
  fi
done

if [[ ! -d "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  printf 'MODE_BREACH trusted supplied semantics missing_or_symlink\n'
  status=2
elif [[ ! -d "$candidate/reference-semantics" || -L "$candidate/reference-semantics" ]]; then
  printf 'SEMANTICS_INTEGRITY FAIL candidate tree missing_or_symlink\n'
  status=1
else
  if find "$reference/reference-semantics" "$candidate/reference-semantics" -type l -print -quit | grep -q .; then
    printf 'SEMANTICS_INTEGRITY FAIL symlinked entry\n'
    find "$reference/reference-semantics" "$candidate/reference-semantics" -type l -printf '%p -> %l\n'
    status=1
  fi

  tmp_a=$(mktemp)
  tmp_b=$(mktemp)
  (
    cd "$reference/reference-semantics" || exit 1
    find . -mindepth 1 -printf '%y %P\n' | sort
  ) > "$tmp_a"
  (
    cd "$candidate/reference-semantics" || exit 1
    find . -mindepth 1 -printf '%y %P\n' | sort
  ) > "$tmp_b"
  if diff -u "$tmp_a" "$tmp_b"; then
    printf 'SEMANTICS_ENTRY_SET OK\n'
  else
    printf 'SEMANTICS_ENTRY_SET FAIL\n'
    status=1
  fi
  rm -f "$tmp_a" "$tmp_b"

  if diff -r --no-dereference "$reference/reference-semantics" "$candidate/reference-semantics"; then
    printf 'SEMANTICS_BYTE_IDENTITY OK\n'
  else
    printf 'SEMANTICS_BYTE_IDENTITY FAIL\n'
    status=1
  fi
fi

exit "$status"
