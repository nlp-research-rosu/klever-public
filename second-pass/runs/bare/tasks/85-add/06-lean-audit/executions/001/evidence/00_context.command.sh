#!/usr/bin/env bash
set -euxo pipefail
pwd
printf 'AUDIT_MODE=%s\n' "${AUDIT_MODE-}"
sha256sum /audit-input.json
sed -n '1,260p' /audit-input.json
find /reference -maxdepth 2 -type f -printf '%p\n' | sort
if [[ -e /candidate ]]; then
  find /candidate -maxdepth 3 -printf '%y %p\n' | sort
else
  printf '/candidate absent\n'
fi
