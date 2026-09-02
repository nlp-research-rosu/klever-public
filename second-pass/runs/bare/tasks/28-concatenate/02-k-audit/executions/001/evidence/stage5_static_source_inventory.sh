#!/usr/bin/env bash
set -euxo pipefail

find /tmp/audit-work/fresh -maxdepth 1 -type f -name '*.k' -printf '%f\n' | sort
nl -ba /tmp/audit-work/fresh/semantic.k
nl -ba /tmp/audit-work/fresh/verification.k
nl -ba /tmp/audit-work/fresh/spec.k
nl -ba /tmp/audit-work/fresh/solution.mpy
rg -n \
  '^\s*(syntax|rule|claim|configuration|requires|module|imports)|\[(function|total|functional|simplification|priority|owise|anywhere|concrete)' \
  /tmp/audit-work/fresh/semantic.k \
  /tmp/audit-work/fresh/verification.k \
  /tmp/audit-work/fresh/spec.k
