#!/usr/bin/env bash
set -uo pipefail

pwd
printf '%s\n' '--- AUDIT_MODE ---'
printenv AUDIT_MODE
printf '%s\n' '--- audit-input.json ---'
python3 -m json.tool /audit-input.json
printf '%s\n' '--- toolchain lock ---'
python3 -m json.tool /reference/klean-toolchain.lock.json
printf '%s\n' '--- generation producer hashes ---'
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
printf '%s\n' '--- generator manifest ---'
python3 -m json.tool /reference/klean-generation/generator-manifest.json
printf '%s\n' '--- generation source manifest ---'
python3 -m json.tool /reference/generation-tools/source-manifest.json
printf '%s\n' '--- stage4 input manifest ---'
python3 -m json.tool /reference/klean-generation/input-manifest.json
printf '%s\n' '--- stage4 export result ---'
python3 -m json.tool /reference/klean-generation/export-result.json
printf '%s\n' '--- stage4 preflight record ---'
python3 -m json.tool /reference/klean-generation/preflight.json
printf '%s\n' '--- trust inventory ---'
python3 -m json.tool /reference/klean-generation/trust-inventory.json
printf '%s\n' '--- mounted files ---'
find /reference/tools -maxdepth 2 -type f -print | sort
find /reference/generation-tools -maxdepth 2 -type f -print | sort
find /reference/k-proof -maxdepth 3 -type f -print | sort
find /reference/klean-generation -maxdepth 4 -type f -print | sort
find /candidate -maxdepth 4 -type f -print 2>/dev/null | sort
