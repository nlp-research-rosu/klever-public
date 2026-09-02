#!/usr/bin/env bash
set -uo pipefail

kprove spec.k \
  --definition scan-nototal-kompiled \
  --spec-module SPEC
status=$?
printf 'scan_nototal_kprove_exit=%s\n' "$status"
exit "$status"
