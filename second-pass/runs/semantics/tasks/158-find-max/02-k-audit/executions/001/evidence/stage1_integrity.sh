#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

printf 'Candidate top-level inventory (type, path, symlink target):\n'
find -P "$candidate" -mindepth 1 -maxdepth 1 -printf '%y %p -> %l\n' | LC_ALL=C sort

printf '\nRequired provenance artifacts:\n'
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    printf 'OK regular file: %s\n' "$candidate/$name"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    printf 'BAD type or symlink: %s\n' "$candidate/$name"
    stat -c '  mode=%F symlink=%N' "$candidate/$name"
  else
    printf 'MISSING: %s\n' "$candidate/$name"
  fi
done

printf '\nPossible structured generation traces:\n'
find -P "$candidate" -maxdepth 2 -type f \
  \( -iname '*trace*.json' -o -iname '*trace*.jsonl' -o -iname '*trace*.log' \) \
  -print | LC_ALL=C sort

printf '\nTrusted-mode boundary:\n'
if [[ -d "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  printf 'OK trusted supplied semantics is a real directory\n'
else
  printf 'INFRASTRUCTURE BREACH: trusted supplied semantics missing or not a real directory\n'
fi

printf '\nRequired candidate source artifact types:\n'
for name in prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    printf 'OK regular file: %s\n' "$candidate/$name"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    printf 'BAD type or symlink: %s\n' "$candidate/$name"
  else
    printf 'MISSING: %s\n' "$candidate/$name"
  fi
done

printf '\nSymlinks anywhere in candidate supplied-semantics tree:\n'
find -P "$candidate/reference-semantics" -type l -printf '%p -> %l\n' | LC_ALL=C sort

printf '\nPrompt comparison:\n'
cmp -s "$candidate/prompt.py" "$reference/prompt.py"
prompt_status=$?
printf 'cmp candidate/prompt.py reference/prompt.py: %d\n' "$prompt_status"
if (( prompt_status != 0 )); then
  diff -u "$reference/prompt.py" "$candidate/prompt.py" || true
fi

printf '\nTranslator comparison:\n'
cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"
translator_status=$?
printf 'cmp candidate/py2mpy.py reference/py2mpy.py: %d\n' "$translator_status"
if (( translator_status != 0 )); then
  diff -u "$reference/py2mpy.py" "$candidate/py2mpy.py" || true
fi

printf '\nSupplied-semantics recursive comparison:\n'
diff -r --no-dereference "$reference/reference-semantics" "$candidate/reference-semantics"
semantics_status=$?
printf 'diff supplied semantics status: %d\n' "$semantics_status"

printf '\nSHA-256 inventory for trusted and candidate semantics:\n'
(
  cd "$reference/reference-semantics" &&
  find -P . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
) > /tmp/audit-work/reference-semantics.sha256
(
  cd "$candidate/reference-semantics" &&
  find -P . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
) > /tmp/audit-work/candidate-semantics.sha256
diff -u /tmp/audit-work/reference-semantics.sha256 /tmp/audit-work/candidate-semantics.sha256
hash_status=$?
printf 'relative-path SHA-256 inventory diff status: %d\n' "$hash_status"

if (( prompt_status == 0 && translator_status == 0 && semantics_status == 0 && hash_status == 0 )); then
  exit 0
fi
exit 1
