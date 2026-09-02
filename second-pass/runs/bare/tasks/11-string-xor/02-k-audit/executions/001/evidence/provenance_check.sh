#!/usr/bin/env bash
set -uo pipefail

status=0

echo 'MODE_BOUNDARY'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  stat -c '%F|%n|%N' /reference/reference-semantics
  status=1
else
  echo '/reference/reference-semantics: ABSENT (required)'
fi

echo 'REQUIRED_ARTIFACT_TYPES'
for name in run-input.json metrics.json codex-last.txt codex-output.log \
            prompt.py py2mpy.py solution.py solution.mpy semantic.k spec.k \
            verification.k prove.sh; do
  if [[ -e "/candidate/$name" || -L "/candidate/$name" ]]; then
    stat -c '%F|mode=%a|size=%s|%n|%N' "/candidate/$name"
    [[ -f "/candidate/$name" && ! -L "/candidate/$name" ]] || status=1
  else
    echo "MISSING|/candidate/$name"
    status=1
  fi
done

echo 'OPTIONAL_VALIDATION_ARTIFACTS'
for name in PROOF.md spec-vacuity.k; do
  if [[ -e "/candidate/$name" || -L "/candidate/$name" ]]; then
    stat -c '%F|mode=%a|size=%s|%n|%N' "/candidate/$name"
  else
    echo "ABSENT|/candidate/$name"
  fi
done

echo 'TRUSTED_FILE_COMPARISONS'
cmp -s /candidate/prompt.py /reference/prompt.py
cmp_prompt=$?
echo "prompt.py cmp exit: $cmp_prompt"
(( cmp_prompt == 0 )) || status=1
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
cmp_translator=$?
echo "py2mpy.py cmp exit: $cmp_translator"
(( cmp_translator == 0 )) || status=1
sha256sum /reference/prompt.py /candidate/prompt.py \
          /reference/py2mpy.py /candidate/py2mpy.py \
          /reference/canonical.py

echo 'UNTRUSTED_CLAIM_FILES'
sha256sum /candidate/run-input.json /candidate/metrics.json \
          /candidate/codex-last.txt /candidate/codex-output.log
sed -n '1,120p' /candidate/run-input.json
sed -n '1,120p' /candidate/metrics.json
sed -n '1,120p' /candidate/codex-last.txt

echo 'STRUCTURED_TRACE'
trace_count=$(find /candidate/codex-trace -type f -name '*.jsonl' | wc -l)
echo "jsonl file count: $trace_count"
find /candidate/codex-trace -type f -name '*.jsonl' -printf '%p|%s bytes\n' | sort
if (( trace_count > 0 )); then
  python3 /audit-output/evidence/trace_summary.py
fi

echo 'SOURCE_TREE_SYMLINKS'
find /candidate -maxdepth 1 -type l -printf '%p -> %l\n'

echo 'CANDIDATE_TOP_LEVEL_INVENTORY'
find /candidate -mindepth 1 -maxdepth 1 -printf '%y|%f|%s bytes|%l\n' | sort

exit "$status"
