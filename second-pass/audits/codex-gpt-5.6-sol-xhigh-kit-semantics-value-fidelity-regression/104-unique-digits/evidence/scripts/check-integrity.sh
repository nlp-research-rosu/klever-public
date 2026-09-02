#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
status=0

required_files=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  verification.k
  spec.k
)

printf '%s\n' 'REQUIRED CANDIDATE FILE TYPES'
for relative in "${required_files[@]}"; do
  path="$candidate/$relative"
  if [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
    status=1
  elif [[ -f "$path" ]]; then
    printf 'REGULAR %s\n' "$path"
  elif [[ -e "$path" ]]; then
    printf 'MISTYPED %s\n' "$path"
    status=1
  else
    printf 'MISSING %s\n' "$path"
    status=1
  fi
done

printf '%s\n' 'STRUCTURED TRACE FILES'
find "$candidate/codex-trace" -type f -name '*.jsonl' -printf 'REGULAR %p\n' 2>/dev/null | sort

printf '%s\n' 'TRUSTED MODE BOUNDARY'
if [[ -d "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  printf 'PRESENT_REGULAR_DIRECTORY %s\n' "$reference/reference-semantics"
else
  printf 'MODE_BREACH %s\n' "$reference/reference-semantics"
  status=1
fi

printf '%s\n' 'SEMANTICS SYMLINKS'
candidate_links=$(find "$candidate/reference-semantics" -type l -printf '%p -> %l\n' 2>/dev/null)
if [[ -n "$candidate_links" ]]; then
  printf '%s\n' "$candidate_links"
  status=1
else
  printf '%s\n' NONE
fi

printf '%s\n' 'SEMANTICS ENTRY TYPE MANIFEST DIFF'
candidate_manifest=$(mktemp /tmp/candidate-semantics-manifest.XXXXXX)
reference_manifest=$(mktemp /tmp/reference-semantics-manifest.XXXXXX)
find "$candidate/reference-semantics" -printf '%P\t%y\n' | sort >"$candidate_manifest"
find "$reference/reference-semantics" -printf '%P\t%y\n' | sort >"$reference_manifest"
diff -u "$reference_manifest" "$candidate_manifest"
manifest_status=$?
printf 'MANIFEST_DIFF_EXIT_STATUS: %s\n' "$manifest_status"
if (( manifest_status != 0 )); then
  status=1
fi

printf '%s\n' 'SEMANTICS RECURSIVE CONTENT DIFF'
diff -qr --no-dereference \
  "$reference/reference-semantics" \
  "$candidate/reference-semantics"
content_status=$?
printf 'CONTENT_DIFF_EXIT_STATUS: %s\n' "$content_status"
if (( content_status != 0 )); then
  status=1
fi

printf '%s\n' 'PROMPT AND TRANSLATOR BYTE COMPARISONS'
cmp "$reference/prompt.py" "$candidate/prompt.py"
prompt_status=$?
printf 'PROMPT_CMP_EXIT_STATUS: %s\n' "$prompt_status"
cmp "$reference/py2mpy.py" "$candidate/py2mpy.py"
translator_status=$?
printf 'TRANSLATOR_CMP_EXIT_STATUS: %s\n' "$translator_status"
if (( prompt_status != 0 || translator_status != 0 )); then
  status=1
fi

printf '%s\n' 'SHA256'
sha256sum \
  "$reference/prompt.py" \
  "$candidate/prompt.py" \
  "$reference/py2mpy.py" \
  "$candidate/py2mpy.py" \
  "$reference/canonical.py" \
  "$candidate/solution.py" \
  "$candidate/solution.mpy"

rm -f "$candidate_manifest" "$reference_manifest"
exit "$status"
