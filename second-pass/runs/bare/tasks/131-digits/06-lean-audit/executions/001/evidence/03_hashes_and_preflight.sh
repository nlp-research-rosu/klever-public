#!/usr/bin/env bash
set -euxo pipefail

export PYTHONPATH=/reference
test "$AUDIT_MODE" = CLASSIFICATION_ONLY
python /audit-output/evidence/03_hashes_and_preflight.py
sha256sum /reference/klean-generation/generated/obligation-map.json
sed -n '1,320p' /reference/klean-generation/generated/obligation-map.json
sed -n '1,320p' /reference/klean-toolchain.lock.json
