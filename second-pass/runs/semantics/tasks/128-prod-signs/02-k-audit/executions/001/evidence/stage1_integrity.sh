#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference
had_issue=0

echo 'MODE_CHECK: SUPPLIED_SEMANTICS'
if [[ -d "$reference/reference-semantics" ]]; then
  echo 'PASS reference/reference-semantics is present'
else
  echo 'INFRASTRUCTURE_BREACH reference/reference-semantics is absent'
  exit 70
fi

echo 'REQUIRED_GENERATION_METADATA'
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    echo "PRESENT regular $candidate/$name"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    echo "MISTYPED_OR_SYMLINKED $candidate/$name"
    had_issue=1
  else
    echo "MISSING $candidate/$name"
    had_issue=1
  fi
done

echo 'REQUIRED_PROOF_ARTIFACT_TYPES'
for name in prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    echo "PASS regular $candidate/$name"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    echo "FAIL mistyped_or_symlinked $candidate/$name"
    had_issue=1
  else
    echo "FAIL missing $candidate/$name"
    had_issue=1
  fi
done

echo 'TRUSTED_PROMPT_COMPARISON'
cmp "$candidate/prompt.py" "$reference/prompt.py"
echo "prompt_cmp_exit=$?"

echo 'TRUSTED_TRANSLATOR_COMPARISON'
cmp "$candidate/py2mpy.py" "$reference/py2mpy.py"
echo "translator_cmp_exit=$?"

echo 'SUPPLIED_SEMANTICS_SYMLINK_CHECK'
find "$candidate/reference-semantics" -type l -print
find "$reference/reference-semantics" -type l -print

echo 'SUPPLIED_SEMANTICS_RECURSIVE_COMPARISON'
diff -qr --no-dereference \
  "$reference/reference-semantics" \
  "$candidate/reference-semantics"
echo "semantics_diff_exit=$?"

echo 'SOURCE_SHA256'
sha256sum \
  "$candidate/prompt.py" "$reference/prompt.py" \
  "$candidate/py2mpy.py" "$reference/py2mpy.py" \
  "$candidate/solution.py" "$candidate/solution.mpy" \
  "$candidate/spec.k" "$candidate/verification.k"

echo "NONFATAL_PROVENANCE_ISSUE=$had_issue"
exit 0
