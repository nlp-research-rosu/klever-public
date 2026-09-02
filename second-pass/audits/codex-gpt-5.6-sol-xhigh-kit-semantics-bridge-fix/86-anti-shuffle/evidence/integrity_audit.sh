#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
status=0

required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy verification.k spec.k prove.sh PROOF.md
)

for name in "${required[@]}"; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    printf 'REQUIRED_OK regular_non_symlink %s\n' "$name"
  else
    printf 'REQUIRED_FAIL %s\n' "$name"
    status=1
  fi
done

mapfile -t traces < <(find "$candidate/codex-trace" -type f -name '*.jsonl' -print 2>/dev/null)
printf 'STRUCTURED_TRACE_COUNT %s\n' "${#traces[@]}"
if ((${#traces[@]} == 0)); then
  status=1
fi

if [[ ! -d "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  printf 'MODE_BOUNDARY_FAIL trusted supplied semantics missing or symlinked\n'
  status=1
else
  printf 'MODE_BOUNDARY_OK trusted supplied semantics is a directory\n'
fi

candidate_links=$(find "$candidate/reference-semantics" -type l -print | wc -l)
printf 'CANDIDATE_SEMANTICS_SYMLINK_COUNT %s\n' "$candidate_links"
if ((candidate_links != 0)); then
  status=1
fi

diff --no-dereference -qr \
  "$reference/reference-semantics" "$candidate/reference-semantics"
semantics_status=$?
printf 'SEMANTICS_RECURSIVE_DIFF_EXIT %s\n' "$semantics_status"
if ((semantics_status != 0)); then
  status=1
fi

cmp -s "$reference/prompt.py" "$candidate/prompt.py"
prompt_status=$?
printf 'PROMPT_BYTE_CMP_EXIT %s\n' "$prompt_status"
if ((prompt_status != 0)); then
  status=1
fi

cmp -s "$reference/py2mpy.py" "$candidate/py2mpy.py"
translator_status=$?
printf 'TRANSLATOR_BYTE_CMP_EXIT %s\n' "$translator_status"
if ((translator_status != 0)); then
  status=1
fi

sha256sum \
  "$reference/prompt.py" "$candidate/prompt.py" \
  "$reference/py2mpy.py" "$candidate/py2mpy.py"

printf 'INTEGRITY_AUDIT_EXIT %s\n' "$status"
exit "$status"
