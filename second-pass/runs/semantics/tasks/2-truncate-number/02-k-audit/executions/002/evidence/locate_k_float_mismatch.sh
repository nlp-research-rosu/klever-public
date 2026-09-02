#!/usr/bin/env bash
set -u

work=/tmp/audit-work/truncate2-reconstruction
source_file=${1:-$work/auditor-k-float-tests.py}
translator=$work/trusted-py2mpy.py
definition=$work/auditor-runtime-kompiled

run_prefix() {
  local count=$1
  local source_prefix=$work/auditor-float-prefix.py
  local mpy_prefix=$work/auditor-float-prefix.mpy
  sed -n "1,$((3 + count))p" "$source_file" > "$source_prefix"
  python3 "$translator" "$source_prefix" > "$mpy_prefix"
  krun "$mpy_prefix" --definition "$definition" > "$work/auditor-float-prefix.out" 2>&1
}

low=1
high=$(sed -n '4,$p' "$source_file" | wc -l)
echo "case_count=$high"

if run_prefix "$high"; then
  echo "full_suite_status=PASS"
  exit 0
else
  echo "full_suite_status=FAIL"
fi

while (( low < high )); do
  mid=$(((low + high) / 2))
  if run_prefix "$mid"; then
    echo "prefix_cases=$mid status=PASS"
    low=$((mid + 1))
  else
    echo "prefix_cases=$mid status=FAIL"
    high=$mid
  fi
done

first_failure=$low
if (( first_failure > 1 )); then
  if run_prefix $((first_failure - 1)); then
    echo "preceding_prefix_cases=$((first_failure - 1)) status=PASS"
  else
    echo "preceding_prefix_cases=$((first_failure - 1)) status=UNEXPECTED_FAIL"
    exit 2
  fi
fi

echo "first_failing_case=$first_failure"
sed -n "$((3 + first_failure))p" "$source_file"

if run_prefix "$first_failure"; then
  echo "failing_prefix_rerun=UNEXPECTED_PASS"
  exit 3
else
  rc=$?
  echo "failing_prefix_rerun=EXPECTED_FAIL exit=$rc"
  tail -n 35 "$work/auditor-float-prefix.out"
fi
