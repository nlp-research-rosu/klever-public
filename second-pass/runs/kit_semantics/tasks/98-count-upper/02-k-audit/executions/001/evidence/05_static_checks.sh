#!/usr/bin/env bash
set -euo pipefail

diff --recursive --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics
echo "SUPPLIED_SEMANTICS_RECURSIVE_DIFF=PASS"

if find /candidate/reference-semantics -type l -print -quit | grep -q .
then
  echo "unexpected candidate semantics symlink" >&2
  exit 1
fi
echo "SUPPLIED_SEMANTICS_NO_SYMLINKS=PASS"

if rg -n \
  'count_upper|countUpperEven|AEIOU|Name\("remaining"\)' \
  /reference/reference-semantics
then
  echo "task-specific text found in fixed semantics" >&2
  exit 1
fi
echo "FIXED_SEMANTICS_TASK_TEXT_ABSENT=PASS"

if rg -n --fixed-strings \
  -e '<k>' -e 'Call(' -e 'While(' -e 'Assign(' -e 'Return(' \
  /candidate/verification.k
then
  echo "proof-local operational bridge found" >&2
  exit 1
fi
echo "PROOF_LOCAL_OPERATIONAL_BRIDGES=NONE"

echo "PROOF_LOCAL_DECLARATIONS"
rg -n '^\s*(syntax|rule|claim|context)\b' \
  /candidate/verification.k \
  /candidate/spec.k

echo "FIXED_OPAQUE_OR_TOTAL_SYMBOLS"
rg -n 'no-evaluators|\[function, total|\[total' \
  /reference/reference-semantics/semantics.k \
  /reference/reference-semantics/semantics/*.k

echo "CALL_RULE_OVERLAP_CHECK"
rg -n 'rule <k> Call\(' \
  /reference/reference-semantics/semantics/*.k \
  /candidate/verification.k

echo "STATIC_SCREENING=PASS"
