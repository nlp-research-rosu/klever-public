# Audit commands

All paths below were mounted read-only except `/audit-output` and
`/tmp/audit-work`. Candidate/provenance scripts were never executed.

## Producer integrity

The producer bundle aggregate uses the hash routine selected by the trusted
Stage 6 resolver, not Klean's generated-project digest:

```bash
PYTHONPATH=/reference python -c 'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py /reference/generation-tools/source-manifest.json
```

The complete result is in `01b-producer-integrity-contract-hash.log`.
`00-diagnostic-wrong-tree-algorithm.log` preserves the preliminary result from
using `tools.klean_export.tree_digest`, which is not the contract's producer
bundle hash algorithm.

## Rule inventory and classification evidence

```bash
PYTHONPATH=/reference python /audit-output/evidence/reconstruct_inventory.py
python /audit-output/evidence/check_closure_identity.py
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k
nl -ba /reference/k-proof/reference-semantics/semantics/call.k
```

Full/summary results are in `02-inventory-reconstruction-full.log`,
`03-closure-identity.log`, `09-inventory-reconstruction-summary.log`,
`10-functions-semantics.log`, and `11-call-semantics.log`.

## Required Stage 4 preflight

The exact trusted function invocation was:

```bash
LD_PRELOAD=/tmp/audit-work/proc-self-shim.so PYTHONPATH=/reference python -c 'from pathlib import Path; import json; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

The unshimmed sandbox failure is in `05-preflight-check-generation.log`. The
successful exact-function transcript is
`06-preflight-check-generation-shimmed.log`, and its returned object is
`07-preflight-returned.json`.

Lean needs the minimal `proc-self-shim.c` because this audit sandbox reports a
namespace PID with no corresponding `/proc/<pid>/exe`. The shim changes only
such `readlink` requests to `/proc/self/exe`. Its independent clean-build
transcript was produced with:

```bash
bash /audit-output/evidence/run_clean_build_workaround.sh
```

The complete output is `12-lean-sandbox-workaround.log`.

## Independent manifest, hash, obligation, and target checks

```bash
PYTHONPATH=/reference python /audit-output/evidence/independent_manifest_check.py
```

The complete result is `08-independent-manifest-check.log`.
