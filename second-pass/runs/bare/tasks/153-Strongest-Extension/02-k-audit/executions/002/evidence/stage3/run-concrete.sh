#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/153-strongest-extension
definition="$scratch/semantic-kompiled"
overall=0

run_case() {
  local label=$1
  local class_term=$2
  local extensions_term=$3
  echo "CASE $label"
  echo "\$ krun solution.mpy --definition semantic-kompiled -cCLASS=$class_term -cEXTENSIONS=$extensions_term"
  krun "$scratch/solution.mpy" --definition "$definition" \
    -cCLASS="$class_term" -cEXTENSIONS="$extensions_term"
  local status=$?
  echo "exit_status=$status"
  if [[ $status -ne 0 ]]; then
    overall=1
  fi
}

run_case prompt-worked '"Slices"' \
  'strVal("SErviNGSliCes");strVal("Cheese");strVal("StuFfed")'
run_case singleton '"C"' 'strVal("Zz")'
run_case empty-name '"C"' 'strVal("")'
run_case greater '"C"' 'strVal("abc");strVal("AB");strVal("A-b")'
run_case equal '"C"' 'strVal("AA");strVal("BB")'
run_case unicode-letter '"C"' 'strVal("A");strVal("ÉÉ")'
run_case unicode-cased-nonletter '"C"' 'strVal("A");strVal("ⅣⅣ")'
run_case empty-list '"C"' ''

echo '$ python3 concrete-oracle.py canonical.py solution.py'
python3 /audit-output/evidence/stage3/concrete-oracle.py \
  "$scratch/canonical.py" "$scratch/solution.py"
oracle_status=$?
echo "exit_status=$oracle_status"
if [[ $oracle_status -ne 0 ]]; then
  overall=1
fi

exit "$overall"
