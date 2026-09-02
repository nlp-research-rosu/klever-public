#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
trusted=/reference

echo "SEMANTICS_MODE SUPPLIED_SEMANTICS"
if [[ -d "$trusted/reference-semantics" ]]; then
  echo "TRUSTED_MODE_BOUNDARY OK reference-semantics is present"
else
  echo "TRUSTED_MODE_BOUNDARY BREACH reference-semantics is absent"
  exit 2
fi

for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    echo "PROVENANCE_PRESENT $name"
    sed -n '1,200p' "$candidate/$name"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    echo "PROVENANCE_MISTYPED $name"
  else
    echo "PROVENANCE_MISSING $name"
  fi
done

trace_count=0
for name in generation-trace.json trace.json structured-generation-trace.json; do
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    trace_count=$((trace_count + 1))
    echo "STRUCTURED_TRACE_PRESENT $name"
    sed -n '1,200p' "$candidate/$name"
  elif [[ -e "$candidate/$name" || -L "$candidate/$name" ]]; then
    echo "STRUCTURED_TRACE_MISTYPED $name"
  fi
done
if [[ "$trace_count" -eq 0 ]]; then
  echo "STRUCTURED_TRACE_ABSENT"
fi

required=(prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k reference-semantics)
for name in "${required[@]}"; do
  if [[ -e "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    echo "REQUIRED_PRESENT $name type=$(stat -c %F "$candidate/$name")"
  elif [[ -L "$candidate/$name" ]]; then
    echo "REQUIRED_SYMLINK $name target=$(readlink "$candidate/$name")"
  else
    echo "REQUIRED_MISSING $name"
  fi
done

if cmp -s "$candidate/prompt.py" "$trusted/prompt.py"; then
  echo "PROMPT_IDENTITY OK"
else
  echo "PROMPT_IDENTITY FAIL"
  diff -u "$trusted/prompt.py" "$candidate/prompt.py" || true
fi

if cmp -s "$candidate/py2mpy.py" "$trusted/py2mpy.py"; then
  echo "TRANSLATOR_IDENTITY OK"
else
  echo "TRANSLATOR_IDENTITY FAIL"
  diff -u "$trusted/py2mpy.py" "$candidate/py2mpy.py" || true
fi

python3 /audit-output/evidence/compare_tree.py \
  "$candidate/reference-semantics" "$trusted/reference-semantics"
tree_status=$?

echo "CANDIDATE_SYMLINKS_BEGIN"
find "$candidate" -type l -printf '%p -> %l\n' | sort
echo "CANDIDATE_SYMLINKS_END"

echo "SOURCE_HASHES_BEGIN"
find "$candidate" -type f ! -path '*/__pycache__/*' -print0 \
  | sort -z \
  | xargs -0 sha256sum
echo "SOURCE_HASHES_END"

exit "$tree_status"
