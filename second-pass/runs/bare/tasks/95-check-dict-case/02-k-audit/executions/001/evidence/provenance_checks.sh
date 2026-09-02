#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

echo "REFERENCE_TREE"
find "$reference" -maxdepth 3 -printf '%y %s %p -> %l\n' | sort
echo "CANDIDATE_TREE"
find "$candidate" -maxdepth 6 -printf '%y %s %p -> %l\n' | sort

echo "TRUSTED_MOUNT_BOUNDARY"
if [[ -e "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  echo "BREACH: generated-semantics mode has reference-semantics"
  mount_status=1
else
  echo "OK: /reference/reference-semantics is absent"
  mount_status=0
fi

required_files=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  program.k
  verification.k
  spec.k
  prove.sh
)

artifact_status=0
echo "REQUIRED_REGULAR_FILES"
for name in "${required_files[@]}"; do
  path="$candidate/$name"
  if [[ -L "$path" ]]; then
    echo "SYMLINK $path"
    artifact_status=1
  elif [[ ! -f "$path" ]]; then
    echo "MISSING_OR_MISTYPED $path"
    artifact_status=1
  else
    stat -c 'OK %F %s bytes %n' "$path"
  fi
done

if [[ -L "$candidate/codex-trace" || ! -d "$candidate/codex-trace" ]]; then
  echo "MISSING_MISTYPED_OR_SYMLINKED $candidate/codex-trace"
  artifact_status=1
else
  echo "OK directory $candidate/codex-trace"
fi

echo "ANY_CANDIDATE_SYMLINKS"
symlinks=$(find "$candidate" -type l -print)
if [[ -n "$symlinks" ]]; then
  printf '%s\n' "$symlinks"
  artifact_status=1
else
  echo "NONE"
fi

echo "TRUSTED_IDENTITY"
cmp "$reference/prompt.py" "$candidate/prompt.py"
prompt_status=$?
echo "prompt.py cmp status: $prompt_status"
cmp "$reference/py2mpy.py" "$candidate/py2mpy.py"
translator_status=$?
echo "py2mpy.py cmp status: $translator_status"
sha256sum \
  "$reference/prompt.py" "$candidate/prompt.py" \
  "$reference/py2mpy.py" "$candidate/py2mpy.py"

echo "CANDIDATE_BUILT_OUTPUT_IGNORED"
if [[ -d "$candidate/verification-kompiled" ]]; then
  echo "/candidate/verification-kompiled exists and is not used"
else
  echo "NONE"
fi

(( mount_status == 0 && artifact_status == 0 &&
   prompt_status == 0 && translator_status == 0 ))
