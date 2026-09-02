#!/usr/bin/env bash
set -euo pipefail
trap 'status=$?; printf "[audit] exit_status=%s\n" "$status"' EXIT
set -x

python3 /audit-output/evidence/compare_k_python.py
