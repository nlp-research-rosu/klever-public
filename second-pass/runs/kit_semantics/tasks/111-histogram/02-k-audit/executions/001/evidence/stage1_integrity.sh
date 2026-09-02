#!/usr/bin/env bash
set -u

required_paths=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/runtime-metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace
  /candidate
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
)

echo "Required path status:"
for artifact_path in "${required_paths[@]}"; do
  if [ -e "$artifact_path" ]; then
    stat --printf='%F | mode=%A | size=%s | %n\n' "$artifact_path"
  else
    echo "MISSING | $artifact_path"
  fi
done

echo
echo "Required-path symlinks:"
find \
  /candidate \
  /reference/reference-semantics \
  /generation-evidence/codex-trace \
  -type l -printf '%p -> %l\n'

echo
echo "Campaign block equality:"
python3 /audit-output/evidence/stage1_json_check.py

echo
echo "Mounted regular-file SHA-256 values:"
sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt

echo
echo "Candidate/trusted prompt comparison:"
cmp --silent /candidate/prompt.py /reference/prompt.py
echo "cmp exit: $?"

echo
echo "Candidate/trusted translator comparison:"
cmp --silent /candidate/py2mpy.py /reference/py2mpy.py
echo "cmp exit: $?"

echo
echo "Reference-semantics type manifests:"
find /reference/reference-semantics -mindepth 1 \
  -printf '%P|%y|%m|%s\n' | LC_ALL=C sort
echo "-- candidate --"
find /candidate/reference-semantics -mindepth 1 \
  -printf '%P|%y|%m|%s\n' | LC_ALL=C sort

echo
echo "Recursive candidate/trusted semantics comparison:"
diff --recursive --brief --no-dereference \
  /reference/reference-semantics /candidate/reference-semantics
echo "diff exit: $?"

echo
echo "Candidate top-level tree (depth <= 3):"
find /candidate -mindepth 1 -maxdepth 3 \
  -printf '%P|%y|%m|%s\n' | LC_ALL=C sort

echo
echo "Structured trace tree:"
find /generation-evidence/codex-trace -mindepth 1 \
  -printf '%P|%y|%m|%s\n' | LC_ALL=C sort
