#!/usr/bin/env bash
set -u

command -v lake
readlink -f "$(command -v lake)"
lake --version
printenv | sort | rg '^(PATH|LEAN|ELAN|LAKE|HOME|XDG|NIX)' || true
nl -ba /reference/klean-generation/generated/lakefile.toml
nl -ba /reference/klean-generation/generated/lean-toolchain

debug_dir="$(mktemp -d /tmp/audit-work/lake-diagnostic.XXXXXX)"
cp -a /reference/klean-generation/generated/. "${debug_dir}/"

(
  cd "${debug_dir}"
  lake clean
)
plain_exit=$?
echo "plain_lake_clean_exit=${plain_exit}"

(
  cd "${debug_dir}"
  LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
    /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake clean
)
configured_exit=$?
echo "configured_lake_clean_exit=${configured_exit}"
