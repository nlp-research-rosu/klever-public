#!/usr/bin/env bash
set -euo pipefail

command -v kup || true
command -v kompile
command -v krun
command -v kprove
kompile --version
krun --version
kprove --version
