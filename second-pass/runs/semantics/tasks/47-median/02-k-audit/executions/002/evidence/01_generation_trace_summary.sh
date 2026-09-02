#!/usr/bin/env bash
set -uo pipefail

echo "COMMAND python3 /audit-output/evidence/01_generation_trace_summary.py"
python3 /audit-output/evidence/01_generation_trace_summary.py
status=$?
echo "TRACE_SUMMARY_EXIT=$status"
exit "$status"
