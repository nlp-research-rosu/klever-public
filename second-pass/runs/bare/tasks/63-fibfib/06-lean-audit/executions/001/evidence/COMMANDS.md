# Audit command record

The corresponding files contain the complete merged stdout/stderr and exit
status captured with `script -q -e -c`.

## Producer provenance

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
```

Result: exit 0. See `01-producer-provenance.txt`.

## Canonical inventory and explicit ordered bijection

```sh
PYTHONPATH=/reference python3 \
  /audit-output/evidence/inventory_bijection_check.py
```

Result: exit 0, five structural checks passed, six canonical rules
reconstructed, zero failures. See `25-explicit-inventory-bijection.txt`.

The full trusted inventory and trust-boundary validator were also run:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
```

Result: exit 0. See `05-inventory-reconstruction-and-bijection.txt`.

## Independent operational check and mutations

```sh
python3 /audit-output/evidence/independent_semantics_check.py
```

Result: exit 0; exact transition/summary agreement for `n = 0..15`, all
one-step invariant checks passed, and counterfactual initial-state and
sequential-assignment mutations were detected. See
`23-independent-semantics-check.txt`.

## Mandatory Stage 4 preflight

Initial command:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Result: exit 1 at `lake clean` because Lean could not resolve
`/proc/<getpid()>/exe` in the audit PID namespace. See
`07-rerun-check-generation.txt` and `08` through `18` for the diagnosis.

The local compatibility shim was built and tested:

```sh
cc -shared -fPIC -Wall -Wextra -O2 \
  -o /tmp/audit-work/proc_self_exe_shim.so \
  /audit-output/evidence/proc_self_exe_shim.c -ldl
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so lean --print-prefix
```

Result: exit 0; Lean 4.22.0, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. See
`19-build-and-test-proc-shim.txt`.

Successful mandatory rerun:

```sh
export LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Result: exit 0, status `KLEAN_NO_OBLIGATIONS`, zero obligations, null target,
and successful `lake clean`/`lake build`. See
`21-rerun-check-generation-success.txt`.

## Independent hashes, obligation bijection, and target absence

```sh
AUDIT_MODE=CLASSIFICATION_ONLY python3 \
  /audit-output/evidence/independent_integrity_check.py
```

Result: exit 0, 65 checks passed and zero failed. See
`24-independent-integrity-check.txt`.

The direct target and forbidden-token scan was:

```sh
rg -n 'targetStatement|sorry|admit|unsafe|^[[:space:]]*(axiom|opaque)[[:space:]]' \
  /reference/klean-generation/generated
```

Result: no `targetStatement`, `sorry`, `admit`, or `unsafe`; the displayed
axioms match the generated trust inventory. See
`22-stage4-exact-manifests-and-scans.txt`.

## Trusted final mechanical gate

```sh
export LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so
PYTHONPATH=/reference python3 /reference/tools/klean_final_gate.py \
  --frozen-k /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --generation /reference/klean-generation \
  --toolchain-lock /reference/klean-toolchain.lock.json \
  --audit-input /audit-input.json
```

Result: exit 0, status `PASS`, mode `CLASSIFICATION_ONLY`, preflight status
`KLEAN_NO_OBLIGATIONS`, null target, and null candidate hash. See
`28-trusted-final-mechanical-gate.txt`.
