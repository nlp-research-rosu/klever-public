#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference

required_claim_files=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
)

for name in "${required_claim_files[@]}"; do
  if [[ -f "$candidate_root/$name" && ! -L "$candidate_root/$name" ]]; then
    printf 'PRESENT regular file: %s\n' "$candidate_root/$name"
  elif [[ -e "$candidate_root/$name" || -L "$candidate_root/$name" ]]; then
    printf 'MISTYPED or symlinked: %s\n' "$candidate_root/$name"
  else
    printf 'MISSING: %s\n' "$candidate_root/$name"
  fi
done

mapfile -t traces < <(
  find -P "$candidate_root" -maxdepth 1 -type f \
    \( -iname '*trace*' -o -iname '*.jsonl' \) -print | LC_ALL=C sort
)
if [[ "${#traces[@]}" -eq 0 ]]; then
  printf 'STRUCTURED_TRACE: absent\n'
else
  printf 'STRUCTURED_TRACE: %s\n' "${traces[@]}"
fi

for pair in \
  "$candidate_root/prompt.py:$reference_root/prompt.py" \
  "$candidate_root/py2mpy.py:$reference_root/py2mpy.py"; do
  candidate_file=${pair%%:*}
  trusted_file=${pair#*:}
  if [[ -L "$candidate_file" ]]; then
    printf 'SYMLINK INTEGRITY FAILURE: %s\n' "$candidate_file"
  elif [[ ! -f "$candidate_file" ]]; then
    printf 'MISSING OR MISTYPED: %s\n' "$candidate_file"
  elif cmp -s "$candidate_file" "$trusted_file"; then
    printf 'BYTE_IDENTICAL: %s == %s\n' "$candidate_file" "$trusted_file"
  else
    printf 'BYTE_MISMATCH: %s != %s\n' "$candidate_file" "$trusted_file"
  fi
done

printf 'SHA256 trusted/candidate sources:\n'
sha256sum \
  "$reference_root/prompt.py" "$candidate_root/prompt.py" \
  "$reference_root/py2mpy.py" "$candidate_root/py2mpy.py"

printf 'REFERENCE_SEMANTICS_SYMLINKS:\n'
find -P "$reference_root/reference-semantics" -type l -printf '%p -> %l\n'
printf 'CANDIDATE_SEMANTICS_SYMLINKS:\n'
find -P "$candidate_root/reference-semantics" -type l -printf '%p -> %l\n'

set +e
diff -r --no-dereference --brief \
  "$reference_root/reference-semantics" \
  "$candidate_root/reference-semantics"
diff_status=$?
set -e
printf 'REFERENCE_SEMANTICS_DIFF_STATUS: %d\n' "$diff_status"

if [[ "$diff_status" -eq 0 ]]; then
  printf 'REFERENCE_SEMANTICS_TREE: exact recursive match\n'
fi
