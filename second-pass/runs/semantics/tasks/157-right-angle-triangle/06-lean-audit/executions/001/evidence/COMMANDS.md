# Command index

All commands were run from `/audit-output`. Mounted inputs under `/reference`,
`/candidate`, and `/audit-input.json` were treated as read-only. The files
named below contain complete command output (including exit status where
`script(1)` was used).

## Mode, producer, and manifests

```sh
env | LC_ALL=C sort
python3 -c 'import json; print(json.dumps(json.load(open("/audit-input.json")), indent=2, sort_keys=True))'
test -e /candidate
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
python3 -c 'import json; ...'  # print source manifest, generator manifest, and audit input
```

Results: `00-environment-and-input.txt`,
`01-producer-hashes-and-manifests.txt`.

## Trusted inventory reconstruction

```sh
PYTHONPATH=/reference python3 -c '
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))
'
```

The trusted implementation was inspected from
`/reference/tools/k_rule_inventory.py`. Results:
`02-trusted-tool-discovery.txt`,
`03-trusted-rule-inventory-code-rest.txt`,
`04-reconstructed-rule-inventory.json.txt`.

## Frozen source, classification, and operational semantics

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/prove.sh
python3 -c 'import json; print(json.dumps(json.load(open("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
rg -n '...' /reference/k-proof/reference-semantics
nl -ba /reference/k-proof/reference-semantics/semantics/core.k
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k
nl -ba /reference/k-proof/reference-semantics/semantics/call.k
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k
nl -ba /reference/k-proof/reference-semantics/semantics/int.k
```

Results: `05-stage1-source-and-stage3.txt`,
`08-operational-semantics-crosswalk.txt`,
`09-focused-operational-crosswalk.txt`.

## Independent manifest, hash, bijection, and target checks

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/independent_integrity_checks.py
```

The exact checker source and result are
`independent_integrity_checks.py` and
`07-independent-integrity-checks.txt`.
Stage 4 sidecars and tree data are in
`06-stage4-sidecars-and-tree.txt`.

## Required fresh Stage 4 preflight

The audit sandbox exposes `/proc/self/exe` but not
`/proc/<namespace-pid>/exe`, while Lean 4.22 asks for the latter. The initial
unmodified call and diagnosis are preserved in files `10` through `24`. The
source for a narrow `readlink` interposer is
`procself_readlink_shim.c`; it changes only an exact
`/proc/<getpid()>/exe` request to `/proc/self/exe`. Validation output is in
`25-toolchain-shim-validation.txt`.

The successful required call was:

```sh
LD_PRELOAD=/tmp/audit-work/libprocself_readlink.so \
PYTHONPATH=/reference \
python3 -c '
import json
from pathlib import Path
from tools.klean_preflight import check_generation
r = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(r, indent=2, sort_keys=True))
'
```

Complete output: `26b-fresh-check-generation-pass.txt`.
`26-fresh-check-generation-pass.txt` preserves an earlier keyword-only
invocation mistake that stopped before any checking. Reconciliation with both
the selected `preflight.json` and `/audit-input.json`:
`28-preflight-reconciliation.txt`.

## Generated-source absence checks

```sh
nl -ba /reference/klean-generation/generated/Klean157RightAngleTriangle.lean
nl -ba /reference/klean-generation/generated/Klean157RightAngleTriangle/Lemmas.lean
rg -n --glob '*.lean' \
  'generatedTarget|theorem|sorry|admit|unsafe|^[[:space:]]*(axiom|opaque)[[:space:]]' \
  /reference/klean-generation/generated
find /reference/klean-generation -maxdepth 4 -type f -printf '%P\n' | LC_ALL=C sort
```

Result: `27-generated-source-absence-checks.txt`.
