#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference
failure=0

check_regular_identity() {
  candidate_path=$1
  reference_path=$2
  label=$3

  if [[ ! -e "$candidate_path" && ! -L "$candidate_path" ]]; then
    printf 'MISSING %s: %s\n' "$label" "$candidate_path"
    failure=1
    return
  fi
  if [[ -L "$candidate_path" ]]; then
    printf 'SYMLINK %s: %s -> %s\n' "$label" "$candidate_path" "$(readlink "$candidate_path")"
    failure=1
    return
  fi
  if [[ ! -f "$candidate_path" ]]; then
    printf 'MISTYPED %s: expected regular file, got %s\n' \
      "$label" "$(stat -c '%F' "$candidate_path")"
    failure=1
    return
  fi
  if cmp -s "$candidate_path" "$reference_path"; then
    printf 'IDENTICAL %s\n' "$label"
  else
    printf 'CHANGED %s\n' "$label"
    failure=1
  fi
  sha256sum "$candidate_path" "$reference_path"
}

check_regular_identity "$candidate_root/prompt.py" "$reference_root/prompt.py" "prompt.py"
check_regular_identity "$candidate_root/py2mpy.py" "$reference_root/py2mpy.py" "py2mpy.py"

candidate_semantics="$candidate_root/reference-semantics"
reference_semantics="$reference_root/reference-semantics"

if [[ ! -d "$candidate_semantics" || -L "$candidate_semantics" ]]; then
  printf 'MISSING_OR_MISTYPED semantics root: %s\n' "$candidate_semantics"
  failure=1
else
  mapfile -t relative_paths < <(
    {
      cd "$candidate_semantics" && find -P . -mindepth 1 -printf '%P\n'
      cd "$reference_semantics" && find -P . -mindepth 1 -printf '%P\n'
    } | LC_ALL=C sort -u
  )

  for relative_path in "${relative_paths[@]}"; do
    candidate_entry="$candidate_semantics/$relative_path"
    reference_entry="$reference_semantics/$relative_path"

    candidate_type=MISSING
    reference_type=MISSING
    if [[ -e "$candidate_entry" || -L "$candidate_entry" ]]; then
      candidate_type=$(stat -c '%F' "$candidate_entry")
    fi
    if [[ -e "$reference_entry" || -L "$reference_entry" ]]; then
      reference_type=$(stat -c '%F' "$reference_entry")
    fi

    if [[ "$candidate_type" != "$reference_type" ]]; then
      printf 'TYPE_OR_PRESENCE_MISMATCH %s candidate=%s reference=%s\n' \
        "$relative_path" "$candidate_type" "$reference_type"
      failure=1
      continue
    fi
    if [[ -L "$candidate_entry" ]]; then
      printf 'SYMLINK semantics entry: %s -> %s\n' \
        "$relative_path" "$(readlink "$candidate_entry")"
      failure=1
      continue
    fi
    if [[ -f "$candidate_entry" ]] && ! cmp -s "$candidate_entry" "$reference_entry"; then
      printf 'CHANGED semantics file: %s\n' "$relative_path"
      sha256sum "$candidate_entry" "$reference_entry"
      failure=1
    fi
  done
fi

if (( failure == 0 )); then
  printf 'SEMANTICS_TREE_IDENTICAL: yes\n'
else
  printf 'SEMANTICS_TREE_IDENTICAL: no\n'
fi

exit "$failure"
