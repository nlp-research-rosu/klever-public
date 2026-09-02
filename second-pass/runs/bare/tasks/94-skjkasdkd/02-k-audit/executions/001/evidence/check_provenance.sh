#!/usr/bin/env bash
set -uo pipefail

candidate=/candidate
reference=/reference

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

required_reference=(
  canonical.py
  prompt.py
  py2mpy.py
)

status=0
echo "GENERATED_SEMANTICS boundary"
if [[ -e "$reference/reference-semantics" || -L "$reference/reference-semantics" ]]; then
  echo "FAIL: forbidden /reference/reference-semantics exists"
  status=1
else
  echo "PASS: /reference/reference-semantics is absent"
fi

echo "Required candidate artifact types"
for name in "${required_candidate[@]}"; do
  path="$candidate/$name"
  if [[ -L "$path" ]]; then
    echo "FAIL symlink: $path -> $(readlink "$path")"
    status=1
  elif [[ -f "$path" ]]; then
    echo "PASS regular: $path"
  elif [[ -e "$path" ]]; then
    echo "FAIL mistyped: $path"
    status=1
  else
    echo "FAIL missing: $path"
    status=1
  fi
done

echo "Required trusted artifact types"
for name in "${required_reference[@]}"; do
  path="$reference/$name"
  if [[ -L "$path" ]]; then
    echo "FAIL trusted symlink: $path -> $(readlink "$path")"
    status=1
  elif [[ -f "$path" ]]; then
    echo "PASS regular: $path"
  elif [[ -e "$path" ]]; then
    echo "FAIL trusted mistyped: $path"
    status=1
  else
    echo "FAIL trusted missing: $path"
    status=1
  fi
done

echo "Structured trace files"
trace_count=0
while IFS= read -r -d '' trace; do
  trace_count=$((trace_count + 1))
  if [[ -L "$trace" ]]; then
    echo "FAIL trace symlink: $trace -> $(readlink "$trace")"
    status=1
  elif [[ -f "$trace" ]]; then
    echo "PASS trace regular: $trace"
  else
    echo "FAIL trace mistyped: $trace"
    status=1
  fi
done < <(find "$candidate/codex-trace" -type f -print0 2>/dev/null)
echo "TRACE_COUNT: $trace_count"
if [[ "$trace_count" -eq 0 ]]; then
  echo "NOTE: no structured generation trace present"
fi

echo "Candidate tree inventory"
find "$candidate" -printf '%y %m %s %p -> %l\n' | sort

echo "Trusted tree inventory"
find "$reference" -printf '%y %m %s %p -> %l\n' | sort

echo "Integrity comparisons"
if cmp -s "$candidate/prompt.py" "$reference/prompt.py"; then
  echo "PASS byte-identical prompt.py"
else
  cmp "$candidate/prompt.py" "$reference/prompt.py" || true
  echo "FAIL changed prompt.py"
  status=1
fi
if cmp -s "$candidate/py2mpy.py" "$reference/py2mpy.py"; then
  echo "PASS byte-identical py2mpy.py"
else
  cmp "$candidate/py2mpy.py" "$reference/py2mpy.py" || true
  echo "FAIL changed py2mpy.py"
  status=1
fi

echo "SHA-256"
sha256sum \
  "$reference/canonical.py" \
  "$reference/prompt.py" \
  "$reference/py2mpy.py" \
  "$candidate/prompt.py" \
  "$candidate/py2mpy.py" \
  "$candidate/solution.py" \
  "$candidate/solution.mpy" \
  "$candidate/semantic.k" \
  "$candidate/verification.k" \
  "$candidate/spec.k"

exit "$status"
