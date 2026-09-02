#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference

printf 'CANDIDATE_TREE_TYPES\n'
find "$candidate_root" -mindepth 1 -printf '%y %p -> %l\n' | sort

printf 'REFERENCE_TREE_TYPES\n'
find "$reference_root" -mindepth 1 -printf '%y %p -> %l\n' | sort

printf 'SYMLINK_CHECK\n'
find "$candidate_root" -type l -print

printf 'REQUIRED_ARTIFACT_CHECK\n'
for audit_required in \
  run-input.json metrics.json codex-last.txt codex-output.log codex-trace \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k spec.k
do
  audit_path="$candidate_root/$audit_required"
  if [[ -e "$audit_path" ]]; then
    stat -c '%F %a %s %n' "$audit_path"
  else
    printf 'MISSING %s\n' "$audit_path"
  fi
done

printf 'TRUSTED_IDENTITY_CHECKS\n'
cmp -s "$candidate_root/prompt.py" "$reference_root/prompt.py"
printf 'prompt.py cmp status=%d\n' "$?"
cmp -s "$candidate_root/py2mpy.py" "$reference_root/py2mpy.py"
printf 'py2mpy.py cmp status=%d\n' "$?"
sha256sum \
  "$candidate_root/prompt.py" "$reference_root/prompt.py" \
  "$candidate_root/py2mpy.py" "$reference_root/py2mpy.py"

printf 'GENERATED_SEMANTICS_BOUNDARY\n'
if [[ -e "$reference_root/reference-semantics" || -L "$reference_root/reference-semantics" ]]; then
  printf 'BREACH trusted reference-semantics exists\n'
  exit 70
else
  printf 'OK trusted reference-semantics absent\n'
fi
if [[ -e "$candidate_root/reference-semantics" || -L "$candidate_root/reference-semantics" ]]; then
  printf 'FAIL unexpected candidate reference-semantics exists\n'
else
  printf 'OK candidate reference-semantics absent\n'
fi

printf 'UNTRUSTED_METADATA_CONTENTS\n'
for audit_metadata in run-input.json metrics.json codex-last.txt; do
  printf 'FILE %s\n' "$candidate_root/$audit_metadata"
  sed -n '1,240p' "$candidate_root/$audit_metadata"
done

printf 'UNTRUSTED_LOG_HEAD_TAIL\n'
sed -n '1,40p' "$candidate_root/codex-output.log"
tail -n 40 "$candidate_root/codex-output.log"

printf 'TRACE_FILE_LIST\n'
find "$candidate_root/codex-trace" -mindepth 1 -maxdepth 3 \
  -printf '%y %s %p -> %l\n' | sort

exit 0
