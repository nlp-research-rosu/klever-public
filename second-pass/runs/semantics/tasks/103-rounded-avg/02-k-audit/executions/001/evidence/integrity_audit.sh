#!/usr/bin/env bash
set +e

candidate=/candidate
reference=/reference

printf '%s\n' '== Required provenance artifacts =='
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    printf 'PRESENT regular %s\n' "$name"
  elif [[ -L "$candidate/$name" ]]; then
    printf 'INVALID symlink %s -> %s\n' "$name" "$(readlink "$candidate/$name")"
  elif [[ -e "$candidate/$name" ]]; then
    printf 'INVALID non-regular %s\n' "$name"
  else
    printf 'MISSING %s\n' "$name"
  fi
done

trace_count=$(find "$candidate" -maxdepth 1 \
  \( -iname '*trace*.json' -o -iname '*trace*.jsonl' -o -iname '*trace*.log' \) \
  -printf '%f\n' | sort)
if [[ -n "$trace_count" ]]; then
  printf 'STRUCTURED_TRACE_CANDIDATES:\n%s\n' "$trace_count"
else
  printf '%s\n' 'STRUCTURED_TRACE: absent'
fi

printf '%s\n' '== Trusted-file byte comparisons =='
for name in prompt.py py2mpy.py; do
  cmp -s "$candidate/$name" "$reference/$name"
  status=$?
  printf 'cmp candidate/%s reference/%s: %d\n' "$name" "$name" "$status"
  sha256sum "$candidate/$name" "$reference/$name"
done

printf '%s\n' '== Supplied semantics entry/type/content comparison =='
if [[ ! -d "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  printf '%s\n' 'INFRASTRUCTURE_BREACH: trusted reference-semantics absent or symlinked'
  exit 90
fi
if [[ ! -d "$candidate/reference-semantics" || -L "$candidate/reference-semantics" ]]; then
  printf '%s\n' 'INTEGRITY_FAILURE: candidate reference-semantics absent, non-directory, or symlinked'
  exit 10
fi

candidate_entries=$(mktemp)
reference_entries=$(mktemp)
find "$candidate/reference-semantics" -mindepth 1 \
  -printf '%P\t%y\t%l\n' | LC_ALL=C sort > "$candidate_entries"
find "$reference/reference-semantics" -mindepth 1 \
  -printf '%P\t%y\t%l\n' | LC_ALL=C sort > "$reference_entries"
diff -u "$reference_entries" "$candidate_entries"
entry_diff=$?
printf 'ENTRY_TYPE_LINK_DIFF_EXIT: %d\n' "$entry_diff"

content_failure=0
while IFS= read -r -d '' trusted_file; do
  relative=${trusted_file#"$reference/reference-semantics/"}
  candidate_file="$candidate/reference-semantics/$relative"
  if [[ ! -f "$candidate_file" || -L "$candidate_file" ]]; then
    printf 'MISSING_OR_MISTYPED_FILE %s\n' "$relative"
    content_failure=1
    continue
  fi
  cmp -s "$trusted_file" "$candidate_file"
  status=$?
  printf 'FILE_CMP %s %d\n' "$relative" "$status"
  if [[ "$status" -ne 0 ]]; then
    content_failure=1
    sha256sum "$trusted_file" "$candidate_file"
  fi
done < <(find "$reference/reference-semantics" -type f -print0 | LC_ALL=C sort -z)
printf 'CONTENT_FAILURE: %d\n' "$content_failure"

rm -f "$candidate_entries" "$reference_entries"
if [[ "$entry_diff" -ne 0 || "$content_failure" -ne 0 ]]; then
  exit 11
fi
exit 0
