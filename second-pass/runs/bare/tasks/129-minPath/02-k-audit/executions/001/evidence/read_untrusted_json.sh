#!/usr/bin/env bash
set +e

printf '%s\n' '=== run-input.json ==='
python3 -m json.tool /candidate/run-input.json
run_input_status=$?
printf 'RUN_INPUT_JSON_EXIT=%s\n' "$run_input_status"

printf '%s\n' '=== metrics.json ==='
python3 -m json.tool /candidate/metrics.json
metrics_status=$?
printf 'METRICS_JSON_EXIT=%s\n' "$metrics_status"

if [ "$run_input_status" -eq 0 ] && [ "$metrics_status" -eq 0 ]; then
  exit 0
fi
exit 1
