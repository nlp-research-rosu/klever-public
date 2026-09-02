#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/tool-versions.log
{
  echo '$ python3 --version'
  python3 --version
  echo "EXIT_STATUS=$?"
  echo '$ kompile --version'
  kompile --version
  echo "EXIT_STATUS=$?"
  echo '$ kprove --version'
  kprove --version
  echo "EXIT_STATUS=$?"
  echo '$ krun --version'
  krun --version
  echo "EXIT_STATUS=$?"
} >"$log" 2>&1
