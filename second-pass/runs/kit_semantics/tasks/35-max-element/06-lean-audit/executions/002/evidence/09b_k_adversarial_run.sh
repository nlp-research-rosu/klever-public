#!/usr/bin/env bash
set -euo pipefail
set -x

test -d /tmp/audit-work/max-float-test-kompiled
krun --definition /tmp/audit-work/max-float-test-kompiled -cPGM=nanLeft
krun --definition /tmp/audit-work/max-float-test-kompiled -cPGM=nanRight

sed -n '730,745p' \
  /opt/runtimeverification-k/k-frontend/src/main/java/org/kframework/compile/ConstantFolding.java
sed -n '1090,1112p' \
  /opt/runtimeverification-k/k-frontend/src/test/java/org/kframework/compile/ConstantFoldingTest.java
