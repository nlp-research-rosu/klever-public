#!/usr/bin/env bash
set -euo pipefail
set -x

kompile --version
sha256sum \
  /opt/runtimeverification-k/k-distribution/include/kframework/builtin/domains.md \
  /reference/k-proof/semantic.k \
  /reference/k-proof/verification.k \
  /reference/k-proof/solution.py
nl -ba /opt/runtimeverification-k/k-distribution/include/kframework/builtin/domains.md \
  | sed -n '1115,1145p;1209,1270p;1324,1335p'
nl -ba /reference/k-proof/semantic.k | sed -n '71,101p'
nl -ba /reference/k-proof/verification.k | sed -n '33,54p'
nl -ba /reference/k-proof/solution.py
