#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

sed -n '1678,1740p' /usr/include/kframework/builtin/domains.md
