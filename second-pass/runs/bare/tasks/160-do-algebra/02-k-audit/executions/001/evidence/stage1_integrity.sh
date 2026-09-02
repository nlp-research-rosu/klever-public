#!/usr/bin/env bash
set -u

candidate_root=/candidate
reference_root=/reference

echo "== mode boundary =="
if [[ -e "$reference_root/reference-semantics" || -L "$reference_root/reference-semantics" ]]; then
  echo "BREACH: reference-semantics exists in GENERATED_SEMANTICS mode"
  mode_status=1
else
  echo "OK: reference-semantics is absent"
  mode_status=0
fi

echo "== candidate top-level inventory =="
find "$candidate_root" -maxdepth 1 -mindepth 1 -printf '%y %f -> %l\n' | sort

echo "== structured trace inventory =="
find "$candidate_root/codex-trace" -type f -printf '%y %s %p -> %l\n' | sort

echo "== required artifact types =="
required_names=(
  run-input.json metrics.json codex-last.txt codex-output.log
  prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k spec.k
)
artifact_status=0
for required_name in "${required_names[@]}"; do
  required_path="$candidate_root/$required_name"
  if [[ ! -e "$required_path" ]]; then
    echo "MISSING $required_path"
    artifact_status=1
  elif [[ -L "$required_path" ]]; then
    echo "SYMLINK $required_path -> $(readlink "$required_path")"
    artifact_status=1
  elif [[ ! -f "$required_path" ]]; then
    echo "MISTYPED $required_path"
    artifact_status=1
  else
    stat --printf='FILE %n size=%s mode=%a\n' "$required_path"
  fi
done

echo "== trusted/candidate byte comparisons =="
comparison_status=0
for compared_name in prompt.py py2mpy.py; do
  if cmp -s "$candidate_root/$compared_name" "$reference_root/$compared_name"; then
    echo "IDENTICAL $compared_name"
  else
    echo "CHANGED $compared_name"
    comparison_status=1
  fi
done

echo "== sha256 =="
sha256sum \
  "$reference_root/prompt.py" \
  "$reference_root/canonical.py" \
  "$reference_root/py2mpy.py" \
  "$candidate_root/prompt.py" \
  "$candidate_root/py2mpy.py" \
  "$candidate_root/solution.py" \
  "$candidate_root/solution.mpy" \
  "$candidate_root/semantic.k" \
  "$candidate_root/verification.k" \
  "$candidate_root/spec.k"

echo "== run-input claimed hashes =="
sed -n '/"inputs"/,/^[[:space:]]*}/p' "$candidate_root/run-input.json"

if (( mode_status != 0 || artifact_status != 0 || comparison_status != 0 )); then
  exit 1
fi
