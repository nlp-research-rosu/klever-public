#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference
overall=0

required_candidate=(
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
if [[ -e "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  echo "FAIL: forbidden trusted reference semantics exists"
  overall=1
else
  echo "PASS: /reference/reference-semantics is absent"
fi

echo "Required candidate artifact types"
for name in "${required_candidate[@]}"; do
  path="$candidate/$name"
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'PASS regular-file %s\n' "$path"
  else
    printf 'FAIL missing-mistyped-or-symlinked %s\n' "$path"
    overall=1
  fi
done

echo "Structured trace files and symlinks"
find "$candidate/codex-trace" -type f -printf 'TRACE regular-file %s bytes %p\n' | sort
find "$candidate" -type l -printf 'SYMLINK %p -> %l\n' | sort

echo "Trusted/candidate prompt and translator hashes"
sha256sum \
  "$candidate/prompt.py" "$reference/prompt.py" \
  "$candidate/py2mpy.py" "$reference/py2mpy.py"
echo "Candidate source artifact hashes"
sha256sum \
  "$candidate/solution.py" "$candidate/solution.mpy" \
  "$candidate/semantic.k" "$candidate/verification.k" \
  "$candidate/spec.k" "$candidate/prove.sh"

if cmp "$candidate/prompt.py" "$reference/prompt.py"; then
  echo "prompt_byte_identity=PASS"
else
  echo "prompt_byte_identity=FAIL"
  overall=1
fi
if cmp "$candidate/py2mpy.py" "$reference/py2mpy.py"; then
  echo "translator_byte_identity=PASS"
else
  echo "translator_byte_identity=FAIL"
  overall=1
fi

echo "Untrusted generation claims: run-input.json"
sed -n '1,240p' "$candidate/run-input.json"
echo "Untrusted generation claims: metrics.json"
sed -n '1,240p' "$candidate/metrics.json"
echo "Untrusted generation claims: codex-last.txt"
sed -n '1,240p' "$candidate/codex-last.txt"
echo "Untrusted generation log boundary excerpts"
sed -n '1,40p' "$candidate/codex-output.log"
tail -40 "$candidate/codex-output.log"

exit "$overall"
