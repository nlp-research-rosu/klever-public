#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference

echo "SUPPLIED_SEMANTICS mount:"
stat -c '%F %n' "$reference_root/reference-semantics"

echo "Candidate required artifact types:"
for artifact in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k
do
  if [ -e "$candidate_root/$artifact" ] || [ -L "$candidate_root/$artifact" ]; then
    stat -c '%F %n' "$candidate_root/$artifact"
  else
    echo "MISSING $candidate_root/$artifact"
  fi
done

echo "Structured generation traces:"
find -P "$candidate_root/codex-trace" -type f -printf '%y %p\n' | sort

echo "Symlinks anywhere in candidate reference-semantics:"
find -P "$candidate_root/reference-semantics" -type l -printf '%p -> %l\n' | sort

echo "Symlinks anywhere in trusted reference-semantics:"
find -P "$reference_root/reference-semantics" -type l -printf '%p -> %l\n' | sort

echo "Recursive supplied-semantics comparison:"
set +e
diff -r --no-dereference \
  "$reference_root/reference-semantics" \
  "$candidate_root/reference-semantics"
semantics_status=$?
set -e
echo "SEMANTICS_DIFF_EXIT_STATUS=$semantics_status"

set +e
cmp -s "$reference_root/prompt.py" "$candidate_root/prompt.py"
prompt_status=$?
cmp -s "$reference_root/py2mpy.py" "$candidate_root/py2mpy.py"
translator_status=$?
set -e
echo "PROMPT_CMP_EXIT_STATUS=$prompt_status"
echo "TRANSLATOR_CMP_EXIT_STATUS=$translator_status"

echo "Trusted/candidate SHA-256 pairs:"
sha256sum \
  "$reference_root/prompt.py" "$candidate_root/prompt.py" \
  "$reference_root/py2mpy.py" "$candidate_root/py2mpy.py"

if [ "$semantics_status" -ne 0 ] \
  || [ "$prompt_status" -ne 0 ] \
  || [ "$translator_status" -ne 0 ]; then
  exit 1
fi
