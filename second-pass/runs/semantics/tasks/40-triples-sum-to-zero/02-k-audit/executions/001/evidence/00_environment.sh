#!/usr/bin/env bash
set -uo pipefail

echo "DATE_UTC $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "WORKDIR $(pwd)"
echo "KOMPILE_PATH $(command -v kompile)"
echo "KPROVE_PATH $(command -v kprove)"
echo "KRUN_PATH $(command -v krun)"
kompile --version
kprove --version
python3 --version
