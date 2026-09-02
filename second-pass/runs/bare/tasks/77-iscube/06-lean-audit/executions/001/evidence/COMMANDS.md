# Audit commands

The result of each command is in the named adjacent log.
The `lake` proof commands ran from
`/tmp/audit-work/77-iscube-proof-audit`; the other commands ran from
`/audit-output`.

```sh
PYTHONPATH=/reference \
  python /audit-output/evidence/reconstruct_inventory.py
# inventory-reconstruction.log

PYTHONPATH=/reference \
  python /audit-output/evidence/recompute_hashes.py
# recomputed-hashes-final.log

gcc -shared -fPIC -Wall -Wextra -Werror \
  /audit-output/evidence/readlink_self_shim.c \
  -o /tmp/audit-work/readlink_self_shim.so
# readlink-shim-rebuild.log

LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so \
PYTHONPATH=/reference \
  python /audit-output/evidence/run_preflight.py
# preflight-rerun-success.log

LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so \
  lake clean
# proof-lake-clean.log

LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so \
  lake build
# proof-lake-build.log

LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so \
  lake env lean AxiomAudit.lean
# proof-print-axioms-success.log

PYTHONPATH=/reference \
  python /audit-output/evidence/reconcile_axioms.py
# axiom-reconciliation.log

LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so \
  lake env lean ProofIdentity.lean
# proof-identity-check.log

LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/readlink_self_shim.so \
  lake env lean BridgeAudit.lean
# operational-bridge-and-mutation-checks.log

python /audit-output/evidence/domain_lemma_checks.py
# domain-lemma-adversarial-checks.log
```
