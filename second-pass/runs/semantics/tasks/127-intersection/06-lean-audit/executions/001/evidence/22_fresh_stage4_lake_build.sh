#!/usr/bin/env bash
set -u

audit_stage4_dir=/tmp/audit-work/stage4-lake-debug
printf '%s\n' 'COMMAND: reproduce Lake build in a fresh generated-project copy'
if test -e "$audit_stage4_dir"; then
  printf 'ERROR: fresh directory exists: %s\n' "$audit_stage4_dir"
  exit 97
fi
cp -a /reference/klean-generation/generated "$audit_stage4_dir"
cd "$audit_stage4_dir" || exit 98
printf '\n[project files]\n'
find . -maxdepth 3 -type f -printf '%p\n' | sort
printf '\n[lean-toolchain]\n'
sed -n '1,20p' lean-toolchain
printf '\n[lakefile.toml]\n'
sed -n '1,200p' lakefile.toml
printf '\n[lake clean]\n'
lake clean
clean_code=$?
printf 'EXIT_CODE=%s\n' "$clean_code"
if test "$clean_code" -ne 0; then exit "$clean_code"; fi
printf '\n[lake build]\n'
lake build
build_code=$?
printf 'EXIT_CODE=%s\n' "$build_code"
exit "$build_code"
