#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference
required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy verification.k spec.k
  solution-program.k prove.sh PROOF.md
)

status=0
printf '%s\n' 'Required artifact type checks:'
for name in "${required[@]}"; do
  path="$candidate_root/$name"
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'OK regular non-symlink: %s\n' "$path"
  else
    printf 'FAIL missing/mistyped/symlinked: %s\n' "$path"
    status=1
  fi
done

if [[ -d "$reference_root/reference-semantics" && ! -L "$reference_root/reference-semantics" ]]; then
  printf '%s\n' 'OK rendered SUPPLIED_SEMANTICS agrees with trusted mount presence'
else
  printf '%s\n' 'FAIL rendered SUPPLIED_SEMANTICS contradicts trusted mount'
  status=1
fi

find "$candidate_root" -type l -printf 'FAIL candidate symlink: %p -> %l\n'
if find "$candidate_root" -type l -print -quit | grep -q .; then
  status=1
else
  printf '%s\n' 'OK no symlinks anywhere under /candidate'
fi

cmp -s "$candidate_root/prompt.py" "$reference_root/prompt.py"
prompt_status=$?
printf 'prompt byte comparison exit: %d\n' "$prompt_status"
(( prompt_status == 0 )) || status=1

cmp -s "$candidate_root/py2mpy.py" "$reference_root/py2mpy.py"
translator_status=$?
printf 'translator byte comparison exit: %d\n' "$translator_status"
(( translator_status == 0 )) || status=1

diff --no-dereference -qr "$reference_root/reference-semantics" "$candidate_root/reference-semantics"
semantics_status=$?
printf 'recursive supplied-semantics comparison exit: %d\n' "$semantics_status"
(( semantics_status == 0 )) || status=1

printf 'trusted semantics entries: '
find "$reference_root/reference-semantics" -printf '%y %P\n' | sort | wc -l
printf 'candidate semantics entries: '
find "$candidate_root/reference-semantics" -printf '%y %P\n' | sort | wc -l

printf '%s\n' 'Untrusted provenance-file hashes and sizes:'
sha256sum "$candidate_root/run-input.json" "$candidate_root/metrics.json" \
  "$candidate_root/codex-last.txt" "$candidate_root/codex-output.log"
wc -lc "$candidate_root/run-input.json" "$candidate_root/metrics.json" \
  "$candidate_root/codex-last.txt" "$candidate_root/codex-output.log"

printf '%s\n' 'Claims observed in untrusted prose/log (not accepted as proof):'
rg -o 'RESULT: [^\r\n]*|differential cases: [0-9]+; mismatches: [0-9]+|#Top|EXPECTED FAILURE[^\r\n]*' \
  "$candidate_root/codex-last.txt" "$candidate_root/codex-output.log" | \
  sort | uniq -c | sed -n '1,120p'

exit "$status"
