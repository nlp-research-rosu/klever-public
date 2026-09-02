#!/usr/bin/env bash
set +e

candidate=/candidate
reference=/reference

printf 'Trusted-mode prerequisite:\n'
if [[ -d "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  printf 'OK: trusted supplied semantics directory is present and not a symlink\n'
else
  printf 'ERROR: trusted supplied semantics directory missing, mistyped, or symlinked\n'
fi

printf '\nRequired candidate artifacts and types:\n'
required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k
)
for name in "${required[@]}"; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    printf 'OK regular file: %s\n' "$name"
  elif [[ -L "$candidate/$name" ]]; then
    printf 'ERROR symlink: %s -> %s\n' "$name" "$(readlink "$candidate/$name")"
  elif [[ -e "$candidate/$name" ]]; then
    printf 'ERROR wrong type: %s\n' "$name"
  else
    printf 'ERROR missing: %s\n' "$name"
  fi
done

printf '\nStructured generation traces:\n'
find -P "$candidate/codex-trace" -type f -printf '%p\n' 2>/dev/null | sort

printf '\nSymlinks anywhere in candidate source tree (compiled outputs pruned):\n'
find -P "$candidate" \
  \( -path "$candidate/runtime-kompiled" -o -path "$candidate/verification-kompiled" -o -path "$candidate/__pycache__" \) -prune \
  -o -type l -printf '%p -> %l\n'

printf '\nCandidate prompt against trusted prompt:\n'
cmp -s "$candidate/prompt.py" "$reference/prompt.py"
printf 'cmp exit: %d\n' "$?"

printf '\nCandidate translator against trusted translator:\n'
cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"
printf 'cmp exit: %d\n' "$?"

printf '\nCandidate supplied semantics against trusted tree:\n'
diff --no-dereference -r "$candidate/reference-semantics" "$reference/reference-semantics"
printf 'diff exit: %d\n' "$?"

printf '\nSHA-256 provenance summary:\n'
sha256sum \
  "$candidate/prompt.py" "$reference/prompt.py" \
  "$candidate/py2mpy.py" "$reference/py2mpy.py" \
  "$candidate/solution.py" "$candidate/solution.mpy" \
  "$candidate/spec.k" "$candidate/verification.k"

printf '\nTop-level source artifact inventory:\n'
find -P "$candidate" -maxdepth 1 -printf '%y %f -> %l\n' | sort
