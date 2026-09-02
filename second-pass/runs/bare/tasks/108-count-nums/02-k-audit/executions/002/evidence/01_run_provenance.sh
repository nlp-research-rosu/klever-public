#!/usr/bin/env bash
set -u
trap 'status=$?; printf "EXIT_STATUS=%s\n" "$status"' EXIT
set -x
python3 /audit-output/evidence/01_provenance_check.py
