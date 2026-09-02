# Material audit commands

All mounted candidate and provenance paths remained read-only. Commands that
needed build output used fresh directories below `/tmp/audit-work`.

```sh
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.k_rule_inventory import inventory_verification; import json; print(json.dumps(inventory_verification(Path("/reference/k-proof")), sort_keys=True, indent=2))'

sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py

PYTHONPATH=/reference LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  python3 -c \
  'from pathlib import Path; from tools.klean_preflight import check_generation; import json; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")), sort_keys=True, indent=2))'

kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition outer-connection-kompiled
kprove outer-connection-spec.k --definition outer-connection-kompiled \
  --spec-module OUTER-CONNECTION-SPEC

PYTHONPATH=/reference \
  python3 /audit-output/evidence/46-independent-hash-and-bijection-audit.py

LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so lake build

LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  PYTHONPATH=/reference \
  python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation --candidate /candidate

LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  lake env lean AxiomAndTypeAudit.lean
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  lake env lean OperationalBridgeAudit.lean

LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  PYTHONPATH=/reference \
  python3 /reference/tools/klean_final_gate.py \
  --frozen-k /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --generation /reference/klean-generation \
  --candidate /candidate \
  --toolchain-lock /reference/klean-toolchain.lock.json \
  --audit-input /audit-input.json \
  --output /audit-output/evidence/58-trusted-final-mechanical-gate.json
```

The `LD_PRELOAD` shim changes only `readlink("/proc/<current-pid>/exe")` to
`readlink("/proc/self/exe")`. The audit sandbox exposes the latter but hides
the former. Evidence `14` through `36` records the diagnosis, shim source,
binary hash, and Lean version validation. It does not modify Lean, Lake,
generated sources, or the proof candidate.
