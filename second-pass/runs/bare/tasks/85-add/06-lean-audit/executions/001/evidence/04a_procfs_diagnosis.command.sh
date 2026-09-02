#!/usr/bin/env bash
set -uxo pipefail
command -v lean
command -v lake
printf 'shell_pid=%s\n' "$$"
ls -l "/proc/$$/exe"
readlink "/proc/$$/exe"
lean --version
printf 'lean_exit=%s\n' "$?"
lake --version
audit_diag_dir=$(mktemp -d /tmp/audit-work/lean-proc-diagnosis.XXXXXX)
cp -a /reference/klean-generation/generated/. "$audit_diag_dir"/
(
  cd "$audit_diag_dir"
  lake clean
)
printf 'lake_clean_exit=%s\n' "$?"
