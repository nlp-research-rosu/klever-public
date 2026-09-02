#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

echo "GENERATED_SEMANTICS boundary"
if [[ -e "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  echo "BREACH: /reference/reference-semantics exists"
else
  echo "OK: /reference/reference-semantics is absent"
fi

echo
echo "Candidate artifact tree (type, path, symlink target)"
find "$candidate" -maxdepth 6 -printf '%y %p -> %l\n' | sort

echo
echo "Required artifact type checks"
required=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy
  semantic.k verification.k spec.k prove.sh
)
for rel in "${required[@]}"; do
  path="$candidate/$rel"
  if [[ -L "$path" ]]; then
    echo "SYMLINK $rel -> $(readlink "$path")"
  elif [[ -f "$path" ]]; then
    echo "REGULAR_FILE $rel"
  elif [[ -e "$path" ]]; then
    echo "MISTYPED $rel"
  else
    echo "MISSING $rel"
  fi
done

echo
echo "Trusted-file identity"
sha256sum \
  "$candidate/prompt.py" "$reference/prompt.py" \
  "$candidate/py2mpy.py" "$reference/py2mpy.py"
cmp -s "$candidate/prompt.py" "$reference/prompt.py"
echo "prompt_cmp_exit=$?"
cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"
echo "translator_cmp_exit=$?"

echo
echo "Untrusted run-input.json"
sed -n '1,200p' "$candidate/run-input.json"
echo
echo "Untrusted metrics.json"
sed -n '1,200p' "$candidate/metrics.json"
echo
echo "Untrusted codex-last.txt"
sed -n '1,200p' "$candidate/codex-last.txt"

echo
echo "Untrusted large-log and structured-trace metadata"
sha256sum "$candidate/codex-output.log"
wc -lc "$candidate/codex-output.log"
trace_count=0
while IFS= read -r -d '' trace; do
  trace_count=$((trace_count + 1))
  sha256sum "$trace"
  wc -lc "$trace"
done < <(find "$candidate/codex-trace" -type f -name '*.jsonl' -print0)
echo "structured_trace_file_count=$trace_count"

echo
echo "Untrusted generation claims found in output"
rg -n 'RESULT:|#Top|exited [0-9]+|timed.out|kprove spec.k|kompile verification.k' \
  "$candidate/codex-output.log" | tail -n 120
