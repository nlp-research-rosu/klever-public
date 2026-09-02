#!/usr/bin/env bash
set -euo pipefail

task_dir=/tmp/audit-work/75-is-multiply-prime
cd "$task_dir"

echo "SUBMITTED CONSTRUCTORS"
rg -o '[A-Za-z][A-Za-z0-9]*\(' solution.regenerated.mpy \
  | sed 's/($//' \
  | sort \
  | uniq -c

echo "VERIFICATION LOCAL EXECUTABLE DECLARATIONS/RULES"
rg -n '^\s*(syntax|rule|claim|context|configuration)\b|\[(function|total|functional|simplification|concrete|symbol|no-evaluators|priority|owise)' \
  verification.k

echo "PROOF IMPORT BOUNDARY"
rg -n '^(requires|module|\s+imports)' verification.k reference-semantics/semantics.k

echo "SUPPLIED OPAQUE/CONCRETE BOUNDARIES"
rg -n '\[(function, total, symbol|concrete\]|no-evaluators)' \
  reference-semantics/semantics/*.k

echo "OPAQUE SYMBOL NAMES IN SUBMITTED PROGRAM, WRAPPER, OR SPEC"
if rg -n \
  'intFloatDiv|divII|floatMod|floatLt|absF|floorFI|toF|ceilF|subF|divF|addF|mulF|powF|gtF|eqF|decStrToF|divFloatIntV|intToF|truncF|roundF|roundFN|sqrtF|sortVS|sortKeyVS|md5hexCodes' \
  solution.regenerated.mpy verification.k spec.k
then
  echo "UNEXPECTED_OPAQUE_DEPENDENCY=1"
  exit 1
else
  echo "UNEXPECTED_OPAQUE_DEPENDENCY=0"
fi
