#!/usr/bin/env bash
set -euo pipefail

printf 'AUDIT_MODE=%s\n' "${AUDIT_MODE-}"
sha256sum /audit-input.json
python3 -m json.tool /audit-input.json
sha256sum \
  /reference/k-proof/verification.k \
  /reference/k-proof/spec.k \
  /reference/k-proof/semantic.k \
  /reference/k-proof/solution.py \
  /reference/k-proof/solution.mpy \
  /reference/k-proof/prove.sh \
  /reference/lemma-discovery.json
