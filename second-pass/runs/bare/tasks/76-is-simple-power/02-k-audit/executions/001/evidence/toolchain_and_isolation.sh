#!/usr/bin/env bash
set -euo pipefail

printf 'kompile_path=%s\n' "$(command -v kompile)"
printf 'kprove_path=%s\n' "$(command -v kprove)"
printf 'krun_path=%s\n' "$(command -v krun)"
kompile --version
kprove --version

echo "Scratch source roots and freshly built definitions"
find /tmp/audit-work/source -maxdepth 1 -printf '%y %p\n' | sort

echo "Only these scratch compiled definitions are present; both use fresh-* names"
find /tmp/audit-work/source -maxdepth 1 \
  \( -name '*-kompiled' -o -name build \) -printf '%p\n' | sort
