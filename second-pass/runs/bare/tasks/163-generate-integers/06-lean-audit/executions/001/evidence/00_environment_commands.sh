#!/usr/bin/env bash
set -uo pipefail
trap 'rc=$?; printf "\nEXIT_CODE=%s\n" "$rc"' EXIT

printf 'AUDIT_MODE=%s\n' "${AUDIT_MODE-<unset>}"
python3 -m json.tool /audit-input.json
find /candidate -maxdepth 3 -type f -printf '%P\n' 2>&1 | sort
find /reference/k-proof -maxdepth 2 -type f -printf '%P\n' | sort
find /reference/klean-generation -maxdepth 3 -type f -printf '%P\n' | sort
find /reference/generation-tools -maxdepth 3 -type f -printf '%P\n' | sort
