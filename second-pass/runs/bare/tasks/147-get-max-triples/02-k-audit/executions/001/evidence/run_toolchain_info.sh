#!/usr/bin/env bash
set -u

echo '$ command -v kompile krun kprove'
command -v kompile krun kprove
status=$?
echo "exit_status=$status"

echo '$ kompile --version'
kompile --version
status=$?
echo "exit_status=$status"

echo '$ kprove --version'
kprove --version
status=$?
echo "exit_status=$status"
exit "$status"
