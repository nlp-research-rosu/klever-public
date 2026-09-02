#!/usr/bin/env bash
set -euo pipefail
set -x

find /candidate -printf '%P\t%y\t%l\n' | sort
find /candidate -type f -print0 | sort -z | xargs -0 sha256sum
