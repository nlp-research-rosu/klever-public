#!/usr/bin/env bash
set -o pipefail
printf 'COMMAND: env | grep ^AUDIT_MODE=\n'
env | grep '^AUDIT_MODE='
printf '\nCOMMAND: sha256sum generation producer sources\n'
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
printf '\nCOMMAND: python3 -m json.tool --sort-keys /reference/generation-tools/source-manifest.json\n'
python3 -m json.tool --sort-keys /reference/generation-tools/source-manifest.json
printf '\nCOMMAND: python3 -m json.tool --sort-keys /reference/klean-generation/generator-manifest.json\n'
python3 -m json.tool --sort-keys /reference/klean-generation/generator-manifest.json
printf '\nCOMMAND: python3 -m json.tool --sort-keys /audit-input.json\n'
python3 -m json.tool --sort-keys /audit-input.json
printf '\nCOMMAND: filesystem presence checks\n'
for path in \
  /reference/k-proof \
  /reference/k-audit \
  /reference/lemma-discovery.json \
  /reference/klean-generation \
  /reference/generation-tools \
  /reference/tools \
  /reference/klean-toolchain.lock.json \
  /candidate
do
  if test -e "$path"; then
    stat -c 'PRESENT %F %A %U:%G %s %n' "$path"
  else
    printf 'ABSENT %s\n' "$path"
  fi
done
