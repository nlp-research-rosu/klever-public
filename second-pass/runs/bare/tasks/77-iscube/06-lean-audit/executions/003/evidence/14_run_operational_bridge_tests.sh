#!/usr/bin/env bash
set -euo pipefail
set -x

export LD_PRELOAD=/tmp/audit-work/lean-proc-exe-compat.so
cd /tmp/audit-work/77-iscube-proof-audit
lake env lean OperationalBridgeAudit.lean

cd /tmp/audit-work
kompile KBridgeAudit.k \
  --backend llvm \
  --main-module K-BRIDGE-AUDIT \
  --syntax-module K-BRIDGE-AUDIT-SYNTAX \
  --output-definition KBridgeAudit-kompiled
krun --definition KBridgeAudit-kompiled --output pretty /dev/stdin <<'EOF'
check(5,2)
EOF
krun --definition KBridgeAudit-kompiled --output pretty /dev/stdin <<'EOF'
check(2,5)
EOF
krun --definition KBridgeAudit-kompiled --output pretty /dev/stdin <<'EOF'
check(-3,-3)
EOF
krun --definition KBridgeAudit-kompiled --output pretty /dev/stdin <<'EOF'
check(-3,2)
EOF
krun --definition KBridgeAudit-kompiled --output pretty /dev/stdin <<'EOF'
check(1000000000000,-3)
EOF
