#!/usr/bin/env bash
set -euo pipefail

sha256sum \
  /reference/k-proof/verification.k \
  /reference/k-proof/spec.k \
  /reference/k-proof/solution.py \
  /reference/k-proof/solution.mpy \
  /reference/k-proof/prompt.py
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/prompt.py
nl -ba /reference/tools/k_rule_inventory.py
