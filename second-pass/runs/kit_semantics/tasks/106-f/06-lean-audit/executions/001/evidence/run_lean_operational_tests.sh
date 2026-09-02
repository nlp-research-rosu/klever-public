#!/usr/bin/env bash
set -u

project=/tmp/audit-work/stage5-audit.VpzibW
toolchain=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LD_PRELOAD=/tmp/audit-work/lean_proc_compat.so
export PATH="$toolchain/bin:$PATH"
export LEAN="$toolchain/bin/lean"
export LEAN_SYSROOT="$toolchain/"
export LAKE_HOME="$toolchain/"
export LAKE_OVERRIDE_LEAN=1

echo '$ cp /audit-output/evidence/OperationalTests.lean /tmp/audit-work/stage5-audit.VpzibW/OperationalTests.lean'
cp /audit-output/evidence/OperationalTests.lean "$project/OperationalTests.lean"
echo '$ lake env lean OperationalTests.lean'
(cd "$project" && lake env lean OperationalTests.lean)
status=$?
echo "lean_operational_tests_exit=$status"
exit "$status"
