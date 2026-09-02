#!/usr/bin/env bash
set -euo pipefail

lake_home=/tmp/audit-work/lake-home
lean_root=/opt/elan/toolchains/leanprover--lean4---v4.22.0

mkdir -p "${lake_home}/.lake/build/bin" "${lake_home}/.lake/build/lib"
ln -s "${lean_root}/bin/lake" "${lake_home}/.lake/build/bin/lake"
ln -s "${lean_root}/lib/lean" "${lake_home}/.lake/build/lib/lean"

debug_dir="$(mktemp -d /tmp/audit-work/lake-repaired.XXXXXX)"
cp -a /reference/klean-generation/generated/. "${debug_dir}/"
(
  cd "${debug_dir}"
  env \
    LAKE_HOME="${lake_home}" \
    LEAN_SYSROOT="${lean_root}" \
    lake clean
  env \
    LAKE_HOME="${lake_home}" \
    LEAN_SYSROOT="${lean_root}" \
    lake build
)
