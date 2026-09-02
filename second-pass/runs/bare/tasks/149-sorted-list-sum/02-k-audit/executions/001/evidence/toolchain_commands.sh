#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

command -v kompile
command -v krun
command -v kprove
kompile --version
krun --version
kprove --version
python3 --version
