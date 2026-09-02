#!/usr/bin/env bash
set -euo pipefail

printf 'command -v kompile: '
command -v kompile
printf 'command -v krun: '
command -v krun
printf 'command -v kprove: '
command -v kprove
kompile --version
kprove --version
krun --version
