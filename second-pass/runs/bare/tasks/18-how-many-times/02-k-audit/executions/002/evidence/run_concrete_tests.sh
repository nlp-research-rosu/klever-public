#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/build/semantic-kompiled
translator=/tmp/audit-work/reference/py2mpy.py
test_root=/tmp/audit-work/concrete-tests

names=(
  normal_overlap
  single_char_overlap
  empty_string
  empty_pattern
  both_empty
  pattern_longer
  equal_match
  equal_nonmatch
)
expected=(3 3 0 4 1 0 1 0)

failures=0
for index in "${!names[@]}"; do
  name=${names[$index]}
  wanted=${expected[$index]}
  py_path="${test_root}/${name}.py"
  mpy_path="${test_root}/${name}.mpy"

  printf 'CASE: %s EXPECTED_PYTHON_INT: %s\n' "$name" "$wanted"
  printf 'COMMAND: python3 %q %q > %q\n' "$translator" "$py_path" "$mpy_path"
  python3 "$translator" "$py_path" >"$mpy_path"
  translate_status=$?
  printf 'TRANSLATE_EXIT_STATUS: %d\n' "$translate_status"
  if (( translate_status != 0 )); then
    failures=$((failures + 1))
    continue
  fi

  printf 'COMMAND: krun %q --definition %q\n' "$mpy_path" "$definition"
  output=$(krun "$mpy_path" --definition "$definition" 2>&1)
  run_status=$?
  printf '%s\n' "$output"
  printf 'KRUN_EXIT_STATUS: %d\n' "$run_status"
  if (( run_status != 0 )) || ! grep -Eq "intVal[[:space:]]*\\([[:space:]]*${wanted}[[:space:]]*\\)" <<<"$output"; then
    failures=$((failures + 1))
    printf 'RESULT_CHECK: FAIL\n'
  else
    printf 'RESULT_CHECK: PASS\n'
  fi
done

printf 'TOTAL_CASES: %d\n' "${#names[@]}"
printf 'FAILURES: %d\n' "$failures"
exit "$failures"
