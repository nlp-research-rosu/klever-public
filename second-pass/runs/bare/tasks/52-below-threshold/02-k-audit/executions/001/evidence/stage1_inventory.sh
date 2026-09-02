#!/usr/bin/env bash
set -u

required_candidate_files=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  verification.k
  spec.k
  prove.sh
)

echo "GENERATED_SEMANTICS boundary"
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  echo "CONTRADICTION: /reference/reference-semantics exists"
  stat -c '%F | %n | %N' /reference/reference-semantics
else
  echo "OK: /reference/reference-semantics is absent"
fi

echo "Trusted input types and hashes"
for path in /reference/canonical.py /reference/prompt.py /reference/py2mpy.py; do
  stat -c '%F | %s bytes | %n | %N' "$path"
  sha256sum "$path"
done

echo "Required candidate artifact types and hashes"
for rel_path in "${required_candidate_files[@]}"; do
  path="/candidate/$rel_path"
  if [[ -L "$path" ]]; then
    echo "SYMLINK | $path | $(readlink "$path")"
  elif [[ -f "$path" ]]; then
    stat -c '%F | %s bytes | %n | %N' "$path"
    sha256sum "$path"
  elif [[ -e "$path" ]]; then
    stat -c 'MISTYPED: %F | %s bytes | %n | %N' "$path"
  else
    echo "MISSING | $path"
  fi
done

echo "Structured trace candidates"
find -P /candidate/codex-trace -type f -printf '%y | %s bytes | %p | %l\n' 2>&1 | sort

echo "All candidate symlinks"
find -P /candidate -type l -printf '%p -> %l\n' 2>&1 | sort

echo "Trusted/candidate byte comparisons"
set +e
cmp -s /reference/prompt.py /candidate/prompt.py
prompt_status=$?
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
set -e
echo "prompt.py cmp status: $prompt_status"
echo "py2mpy.py cmp status: $translator_status"

echo "K toolchain"
for tool in kompile kprove krun kast kore-exec; do
  command -v "$tool"
done
kompile --version
kprove --version
krun --version
