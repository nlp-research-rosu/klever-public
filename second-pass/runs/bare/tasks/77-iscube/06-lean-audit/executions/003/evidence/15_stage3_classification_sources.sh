#!/usr/bin/env bash
set -euo pipefail
set -x

nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/prove.sh
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/semantic.k
