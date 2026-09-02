#!/usr/bin/env bash
set -euo pipefail

candidate=/candidate
trusted=/reference

required_candidate=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k
)

echo "semantics_mode=SUPPLIED_SEMANTICS"
if [[ ! -d "$trusted/reference-semantics" || -L "$trusted/reference-semantics" ]]; then
  echo "INFRASTRUCTURE BREACH: trusted reference-semantics is missing, mistyped, or symlinked"
  exit 70
fi

failed=0
for name in "${required_candidate[@]}"; do
  path="$candidate/$name"
  if [[ ! -e "$path" ]]; then
    echo "MISSING required candidate artifact: $path"
    failed=1
  elif [[ -L "$path" ]]; then
    echo "SYMLINKED required candidate artifact: $path -> $(readlink "$path")"
    failed=1
  elif [[ ! -f "$path" ]]; then
    echo "MISTYPED required candidate artifact (not regular file): $path"
    failed=1
  else
    echo "REGULAR required candidate artifact: $path"
  fi
done

if [[ ! -d "$candidate/reference-semantics" || -L "$candidate/reference-semantics" ]]; then
  echo "MISSING/MISTYPED/SYMLINKED candidate reference-semantics tree"
  failed=1
fi

trace_count=$(find "$candidate/codex-trace" -type f -name '*.jsonl' 2>/dev/null | wc -l)
echo "structured_trace_jsonl_count=$trace_count"
if [[ "$trace_count" -eq 0 ]]; then
  echo "MISSING structured generation trace"
  failed=1
fi

if find "$candidate/reference-semantics" "$trusted/reference-semantics" -type l -print -quit | grep -q .; then
  echo "SYMLINK found in candidate or trusted semantics tree"
  find "$candidate/reference-semantics" "$trusted/reference-semantics" -type l -printf '%p -> %l\n'
  failed=1
else
  echo "semantics_symlinks=none"
fi

candidate_types=$(mktemp)
trusted_types=$(mktemp)
trap 'rm -f -- "$candidate_types" "$trusted_types"' EXIT
(cd "$candidate/reference-semantics" && find . -printf '%y %P\n' | LC_ALL=C sort) > "$candidate_types"
(cd "$trusted/reference-semantics" && find . -printf '%y %P\n' | LC_ALL=C sort) > "$trusted_types"
if diff -u "$trusted_types" "$candidate_types"; then
  echo "semantics_entry_names_and_types=identical"
else
  echo "semantics_entry_names_and_types=DIFFERENT"
  failed=1
fi

if diff -qr --no-dereference "$trusted/reference-semantics" "$candidate/reference-semantics"; then
  echo "semantics_recursive_content=identical"
else
  echo "semantics_recursive_content=DIFFERENT"
  failed=1
fi

if cmp -s "$candidate/prompt.py" "$trusted/prompt.py"; then
  echo "prompt_byte_identity=yes"
else
  echo "prompt_byte_identity=NO"
  failed=1
fi

if cmp -s "$candidate/py2mpy.py" "$trusted/py2mpy.py"; then
  echo "translator_byte_identity=yes"
else
  echo "translator_byte_identity=NO"
  failed=1
fi

sha256sum \
  "$candidate/prompt.py" "$trusted/prompt.py" \
  "$candidate/py2mpy.py" "$trusted/py2mpy.py" \
  "$candidate/solution.py" "$candidate/solution.mpy" \
  "$candidate/spec.k" "$candidate/verification.k" \
  "$candidate/run-input.json" "$candidate/metrics.json" \
  "$candidate/codex-last.txt" "$candidate/codex-output.log"
find "$candidate/codex-trace" -type f -name '*.jsonl' -exec sha256sum {} +

python3 -m json.tool "$candidate/run-input.json" >/dev/null
python3 -m json.tool "$candidate/metrics.json" >/dev/null
echo "json_parse=success"

if [[ "$failed" -ne 0 ]]; then
  exit 1
fi
