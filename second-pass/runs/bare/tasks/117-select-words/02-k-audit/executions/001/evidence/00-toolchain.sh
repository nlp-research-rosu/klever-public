#!/usr/bin/env bash
set -euo pipefail
set -x

command -v kompile
command -v krun
command -v kprove
command -v kast
kompile --version
kprove --version
krun --version
