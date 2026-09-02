#!/usr/bin/env bash
set -uo pipefail

candidate_root=/candidate
reference_root=/reference
overall_status=0

check_regular() {
  local path=$1
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'REGULAR_OK %s\n' "$path"
  else
    printf 'REGULAR_FAIL %s\n' "$path"
    overall_status=1
  fi
}

for required in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy \
  verification.k spec.k prove.sh PROOF.md; do
  check_regular "$candidate_root/$required"
done

for trusted in canonical.py prompt.py py2mpy.py; do
  check_regular "$reference_root/$trusted"
done

if [[ -d "$reference_root/reference-semantics" &&
      ! -L "$reference_root/reference-semantics" ]]; then
  printf 'SUPPLIED_SEMANTICS_MOUNT_OK %s\n' \
    "$reference_root/reference-semantics"
else
  printf 'SUPPLIED_SEMANTICS_MOUNT_FAIL %s\n' \
    "$reference_root/reference-semantics"
  overall_status=1
fi

candidate_links=$(find "$candidate_root" -type l -print)
reference_links=$(find "$reference_root" -type l -print)
printf 'CANDIDATE_SYMLINKS_BEGIN\n%s\nCANDIDATE_SYMLINKS_END\n' \
  "$candidate_links"
printf 'REFERENCE_SYMLINKS_BEGIN\n%s\nREFERENCE_SYMLINKS_END\n' \
  "$reference_links"
if [[ -n "$candidate_links" || -n "$reference_links" ]]; then
  overall_status=1
fi

cmp /reference/prompt.py /candidate/prompt.py
prompt_status=$?
printf 'PROMPT_CMP_STATUS %d\n' "$prompt_status"
(( prompt_status == 0 )) || overall_status=1

cmp /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
printf 'TRANSLATOR_CMP_STATUS %d\n' "$translator_status"
(( translator_status == 0 )) || overall_status=1

diff -qr --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics
semantics_status=$?
printf 'SEMANTICS_TREE_DIFF_STATUS %d\n' "$semantics_status"
(( semantics_status == 0 )) || overall_status=1

printf 'STRUCTURED_TRACES_BEGIN\n'
find /candidate/codex-trace -type f -printf '%y %p %s bytes\n' 2>&1 | sort
trace_status=${PIPESTATUS[0]}
printf 'STRUCTURED_TRACES_END\n'
(( trace_status == 0 )) || overall_status=1

printf 'OVERALL_STATUS %d\n' "$overall_status"
exit "$overall_status"
