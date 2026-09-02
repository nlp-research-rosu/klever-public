#!/usr/bin/env bash
set -u

status=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
  return "$rc"
}

printf 'AUDIT STAGE 1 INVENTORY\n'
printf 'GENERATED_SEMANTICS requires /reference/reference-semantics to be absent.\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'MODE_CONTRADICTION=1\n'
  run stat -c '%F %s bytes %a %n -> %N' /reference/reference-semantics
else
  printf 'MODE_CONTRADICTION=0\n'
fi

printf '\nCandidate entry inventory (type, path, symlink target):\n'
run find /candidate -maxdepth 5 -printf '%y %p -> %l\n'

printf '\nRequired artifact metadata:\n'
required=(
  /candidate/run-input.json
  /candidate/metrics.json
  /candidate/codex-last.txt
  /candidate/codex-output.log
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/semantic.k
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
  /reference/prompt.py
  /reference/canonical.py
  /reference/py2mpy.py
)
for path in "${required[@]}"; do
  if [[ -L "$path" ]]; then
    printf 'SYMLINK '
    status=1
  elif [[ -f "$path" ]]; then
    printf 'REGULAR '
  elif [[ -e "$path" ]]; then
    printf 'MISTYPED '
    status=1
  else
    printf 'MISSING '
    status=1
  fi
  stat -c '%F %s bytes mode=%a %n -> %N' "$path" 2>/dev/null || printf '%s\n' "$path"
done

printf '\nTrace inventory:\n'
run find /candidate/codex-trace -type f -printf '%y %s bytes %p -> %l\n'

printf '\nCryptographic hashes:\n'
run sha256sum "${required[@]}"
run sha256sum /candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-27-52-019f8995-034d-7513-8844-1db16c8e062e.jsonl

printf '\nTrusted equality checks:\n'
run cmp -s /candidate/prompt.py /reference/prompt.py
printf 'candidate prompt byte identity: %s\n' "$([[ $? -eq 0 ]] && printf PASS || printf FAIL)"
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
printf 'candidate translator byte identity: %s\n' "$([[ $? -eq 0 ]] && printf PASS || printf FAIL)"

printf '\nToolchain:\n'
run command -v kompile
run command -v krun
run command -v kprove
run kompile --version
run kprove --version

printf '\nSTAGE1_SCRIPT_STATUS=%d\n' "$status"
exit "$status"
