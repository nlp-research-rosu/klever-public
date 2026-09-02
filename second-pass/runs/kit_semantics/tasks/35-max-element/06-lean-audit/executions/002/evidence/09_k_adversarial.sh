#!/usr/bin/env bash
set -euo pipefail
set -x

kompile --version
kompile /audit-output/evidence/max-float-test.k \
  --backend llvm \
  --main-module MAX-FLOAT-TEST \
  --syntax-module MAX-FLOAT-TEST-SYNTAX \
  --output-definition /tmp/audit-work/max-float-test-kompiled

krun --definition /tmp/audit-work/max-float-test-kompiled -cPGM=nanLeft
krun --definition /tmp/audit-work/max-float-test-kompiled -cPGM=nanRight

sed -n '730,745p' \
  /opt/runtimeverification-k/k-frontend/src/main/java/org/kframework/compile/ConstantFolding.java
sed -n '1090,1112p' \
  /opt/runtimeverification-k/k-frontend/src/test/java/org/kframework/compile/ConstantFoldingTest.java
