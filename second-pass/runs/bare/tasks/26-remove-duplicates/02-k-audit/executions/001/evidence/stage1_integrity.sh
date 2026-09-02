#!/usr/bin/env bash
set -u

failure=0

check_regular_nonsymlink() {
  local path=$1
  if [[ ! -e "$path" ]]; then
    printf 'MISSING %s\n' "$path"
    failure=1
  elif [[ -L "$path" ]]; then
    printf 'SYMLINK %s -> %s\n' "$path" "$(readlink "$path")"
    failure=1
  elif [[ ! -f "$path" ]]; then
    printf 'WRONG-TYPE %s\n' "$path"
    failure=1
  else
    printf 'OK regular %s\n' "$path"
  fi
}

printf 'Rendered mode: GENERATED_SEMANTICS\n'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf 'MODE-BREACH reference semantics unexpectedly exists\n'
  failure=1
else
  printf 'OK /reference/reference-semantics is absent\n'
fi

for path in \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh
do
  check_regular_nonsymlink "$path"
done

if cmp -s /candidate/prompt.py /reference/prompt.py; then
  printf 'IDENTICAL candidate prompt.py and trusted prompt.py\n'
else
  printf 'CHANGED candidate prompt.py\n'
  failure=1
fi

if cmp -s /candidate/py2mpy.py /reference/py2mpy.py; then
  printf 'IDENTICAL candidate py2mpy.py and trusted py2mpy.py\n'
else
  printf 'CHANGED candidate py2mpy.py\n'
  failure=1
fi

printf 'Candidate root inventory:\n'
find /candidate -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n' | sort

printf 'Candidate symlinks at any depth:\n'
find /candidate -type l -printf '%p -> %l\n' | sort

printf 'Structured trace files:\n'
find /candidate/codex-trace -type f -printf '%y %s %p\n' 2>/dev/null | sort

printf 'Source hashes:\n'
sha256sum \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k

exit "$failure"
