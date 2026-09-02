# Audit command index

The numbered evidence files contain complete stdout/stderr for the commands
below. Read-only inspection commands are also preserved in their corresponding
numbered files.

## Producer and tree authentication

```bash
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json

PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; from tools.klean_export import tree_digest; ...'
```

Results: `01-producer-authentication.txt`,
`04-tree-hash-recomputation.txt`, `24-independent-hash-reconciliation.txt`,
and `41-generator-image-id-reconciliation.txt`.

## Canonical K inventory and Stage 3 trust-boundary check

```bash
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True, ensure_ascii=False))'

PYTHONPATH=/reference python3 -c \
  'from tools.lemma_discovery_contract import validate_trust_boundary; ...'
```

Results: `06-reconstructed-rule-inventory.json` and
`09-inventory-bijection-and-classification-check.txt`.

## Trusted deterministic-generation preflight

The sandbox exposes namespace PID `2` while lacking `/proc/2/exe`. Lean 4.22
uses `/proc/<getpid>/exe`, so the first unmodified invocations failed before
loading any project. The source and hashes of a narrowly scoped `readlink`
preload correction are in `18-lean-proc-shim-validation.txt`.

```bash
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean-proc-self-shim.so \
  /tmp/audit-work/lean-proc-self-shim.c -ldl

export LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(result)
PY
```

Results: initial environment failures in
`10-rerun-check-generation.json` and
`12-rerun-check-generation-with-pinned-path.json`; corrected successful
result in `19-rerun-check-generation-success.json`.

## Fresh proof build

Fresh project:
`/tmp/audit-work/lean-proof-audit.6hDcA5`.
Only the candidate's four source/metadata files were copied to the root; the
immutable generated project was copied to `Base`.

```bash
cd /tmp/audit-work/lean-proof-audit.6hDcA5
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so lake clean
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so lake build
```

Complete output: `27-fresh-lake-clean-build-complete.txt`.

## Proof identity and axioms

```bash
cd /tmp/audit-work/lean-proof-audit.6hDcA5
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  lake env lean AxiomAudit.lean
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  lake env lean IdentityAudit.lean
```

The first file contains exactly:

```lean
import Proof
#print axioms Proof.final
```

Results: `29-print-axioms-Proof-final.txt` and
`32-proof-identity.txt`.

## Operational-bridge witnesses

```bash
cd /tmp/audit-work/lean-proof-audit.6hDcA5
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  lake env lean OperationalBridgeAudit.lean

krun /tmp/audit-work/int2string-adversarial.mpy \
  --definition /reference/k-proof/runtime-kompiled
krun /tmp/audit-work/strtocodes-ascii-adversarial.mpy \
  --definition /reference/k-proof/runtime-kompiled
krun /tmp/audit-work/strtocodes-nonascii-adversarial.mpy \
  --definition /reference/k-proof/runtime-kompiled
krun /tmp/audit-work/strtocodes-mixed-nonascii-adversarial.mpy \
  --definition /reference/k-proof/runtime-kompiled
```

Results: `36-fixed-k-semantics-int2string-adversarial.txt` through
`40-operational-bridge-ascii-boundary.txt`.
