# Audit commands

The mounted candidate and provenance files were treated as data only. The only
executed code outside trusted `/reference/tools` was authored audit code under
`/audit-output/evidence` or `/tmp/audit-work`.

## Inventory and Stage 3

```bash
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")),indent=2,sort_keys=True))'
```

Result: `01-reconstructed-inventory.json`.

```bash
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json")),indent=2,sort_keys=True))'
```

Result: `06-stage3-contract-validation.json`. The independent count/order
comparison is in `07-stage3-bijection.txt`.

## Recorded hashes and producer provenance

```bash
PYTHONPATH=/reference python3 /audit-output/evidence/check_recorded_hashes.py
```

Result: `12-recorded-hash-checks.json`.

```bash
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
```

The hashes are also recorded and compared in
`12-recorded-hash-checks.json`.

## Trusted deterministic-generation preflight

Initial command:

```bash
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r,indent=2,sort_keys=True))'
```

Result: `13-preflight-initial-environment-failure.txt`.

The sandbox's PID namespace made Lean's `/proc/<pid>/exe` lookup fail. The
auditor-authored compatibility source is `lean-app-path-shim.c`. It only
interposes that readlink and returns the kernel `AT_EXECFN` value.

Corrected command:

```bash
LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so PYTHONPATH=/reference \
python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r,indent=2,sort_keys=True))'
```

Result: `14-preflight-rerun-with-pid-shim.json`.

## Fresh Stage 5 project and build

```bash
AUDIT_LEAN_ROOT=$(mktemp -d /tmp/audit-work/lean-proof.XXXXXX)
mkdir "$AUDIT_LEAN_ROOT/project"
cp -a /candidate/. "$AUDIT_LEAN_ROOT/project/"
cp -a /reference/klean-generation/generated/. "$AUDIT_LEAN_ROOT/project/Base/"
```

The selected path is in `18-fresh-lean-project-path.txt`.

From that fresh project:

```bash
LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so lake clean
LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so lake build
```

Complete results: `20-lake-clean.log` and `21-lake-build.log`.

## Axioms, identity, and the trusted final gate

```bash
LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so \
lake env lean AxiomAudit.lean
```

Result: `22-print-axioms-Proof-final.txt`.

```bash
LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so PYTHONPATH=/reference \
python3 -c 'import json; from pathlib import Path; from tools.klean_final_gate import check_proof_candidate; r=check_proof_candidate(Path("/reference/klean-generation"),Path("/candidate")); print(json.dumps(r,indent=2,sort_keys=True))'
```

Result: `26-final-mechanical-gate.json`.

## Operational and adversarial checks

```bash
LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so \
lake env lean OperationalAudit.lean
```

The checked source and result are
`25-operational-adversarial-tests.lean` and
`25-operational-adversarial-tests.log`.

```bash
krun /reference/k-proof/concrete_tests.mpy \
  --definition /reference/k-proof/runtime-kompiled
```

Result: `32-frozen-k-concrete-run.log`.
