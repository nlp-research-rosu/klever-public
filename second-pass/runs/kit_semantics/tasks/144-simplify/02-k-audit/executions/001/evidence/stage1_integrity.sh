#!/usr/bin/env bash
set -u

status=0

check_regular() {
  path="$1"
  if [ ! -f "$path" ] || [ -L "$path" ]; then
    echo "BAD_REQUIRED_TYPE $path"
    status=1
  else
    echo "REGULAR $path"
  fi
}

echo "COMMAND: bash /audit-output/evidence/stage1_integrity.sh"
echo "audit campaign lock semantic comparison:"
if python3 /audit-output/evidence/check_manifest.py; then
  echo "MANIFEST_CHECK yes"
else
  echo "MANIFEST_CHECK no"
  status=1
fi

echo "required pipeline-v3 records:"
for path in \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py
do
  check_regular "$path"
done

if [ ! -d /generation-evidence/codex-trace ] || [ -L /generation-evidence/codex-trace ]; then
  echo "BAD_REQUIRED_TYPE /generation-evidence/codex-trace"
  status=1
else
  echo "DIRECTORY /generation-evidence/codex-trace"
fi

if [ ! -d /reference/reference-semantics ] || [ -L /reference/reference-semantics ]; then
  echo "BAD_REQUIRED_TYPE /reference/reference-semantics"
  status=1
else
  echo "DIRECTORY /reference/reference-semantics"
fi

echo "declared single-file hashes:"
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

echo "structured trace file hashes:"
find /generation-evidence/codex-trace -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum

echo "candidate input identity:"
cmp -s /candidate/prompt.py /reference/prompt.py
echo "prompt_cmp_exit=$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
echo "translator_cmp_exit=$?"

echo "supplied semantics symlinks:"
find /candidate/reference-semantics /reference/reference-semantics -type l -print

echo "supplied semantics recursive comparison:"
if diff -r --no-dereference \
  /candidate/reference-semantics \
  /reference/reference-semantics; then
  echo "SEMANTICS_TREE_MATCH yes"
else
  echo "SEMANTICS_TREE_MATCH no"
  status=1
fi

echo "independent trusted semantics content manifest:"
(
  cd /reference/reference-semantics
  find . -type f -print0 | sort -z | xargs -0 sha256sum
)

echo "candidate proof-artifact types:"
for path in \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/PROOF.md
do
  check_regular "$path"
done

echo "required-record symlinks under provenance mounts:"
find \
  /candidate \
  /reference \
  /generation-evidence \
  -type l -print

echo "EXIT_STATUS: $status"
exit "$status"
