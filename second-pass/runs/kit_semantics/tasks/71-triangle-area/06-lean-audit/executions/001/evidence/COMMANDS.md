# Audit command ledger

All referenced `.log` files in this directory contain the complete command
output and exit status. The audit used read-only mounted inputs and wrote only
to `/audit-output` and `/tmp/audit-work`.

## Launcher and producer provenance

```sh
env | rg '^AUDIT_MODE='
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
```

Results: `00-launcher-and-input-inventory.log`,
`01-producer-chain.log`, `01b-producer-manifests.log`, and
`01d-producer-canonical-tree-hash.log`.

## Canonical rule inventory and Stage 3 boundary

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
```

Results: `03-inventory-reconstruction-and-tree-hashes.log` and
`21-consolidated-bijection-producer-target-candidate-checks.log`.

## Stage 4 trusted preflight

The first invocation below failed only because the audit sandbox denied Lean's
numeric `/proc/<pid>/exe` lookup. Its complete failure is preserved in
`05-klean-preflight-check-generation.log`.

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

An auditor-authored, narrowly scoped `readlink` compatibility shim was compiled
from `/tmp/audit-work/lean-readlink-shim.c`; its source and binary hashes and
Lean version check are in `05d-auditor-lean-runtime-shim.log`. The same trusted
function was then rerun:

```sh
LD_PRELOAD=/tmp/audit-work/lean-readlink-shim.so \
PYTHONPATH=/reference \
python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Result: `05e-klean-preflight-check-generation-rerun.log`.

## Independent hash, obligation, and target checks

```sh
python3 -m json.tool \
  /reference/klean-generation/generated/obligation-map.json
PYTHONPATH=/reference python3 -c \
  'import hashlib,json; from pathlib import Path; from tools import klean_export; g=Path("/reference/klean-generation/generated"); m=json.loads((g/"obligation-map.json").read_text()); print(hashlib.sha256((g/"obligation-map.json").read_bytes()).hexdigest()); print(repr(klean_export.expected_target_definition(m))); print(json.dumps(klean_export.target_statement(g), indent=2, sort_keys=True)); print(klean_export.tree_digest(g))'
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; [(print(p, sha256_tree(Path(p)))) for p in ["/reference/k-proof", "/reference/k-audit", "/reference/klean-generation", "/reference/generation-tools", "/candidate"]]'
```

Results: `06-obligation-map-target-and-hashes.log`,
`07-all-recorded-input-hashes.log`, and
`21-consolidated-bijection-producer-target-candidate-checks.log`.

## Fresh Stage 5 build

```sh
cp -a /candidate/. /tmp/audit-work/lean-audit-71.8ZE0zZ/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/lean-audit-71.8ZE0zZ/Base/
LD_PRELOAD=/tmp/audit-work/lean-readlink-shim.so lake clean
LD_PRELOAD=/tmp/audit-work/lean-readlink-shim.so lake build
LD_PRELOAD=/tmp/audit-work/lean-readlink-shim.so \
  lake env lean Check.lean
```

The last command executes the candidate's exact
`#print axioms Proof.final`. Results: `09-fresh-proof-copy.log`,
`10-lake-clean.log`, `11-lake-build.log`, and
`12-print-axioms-proof-final.log`.

## Parameter semantics and adversarial checks

```sh
LD_PRELOAD=/tmp/audit-work/lean-readlink-shim.so \
  lake env lean --run AuditParamTests.lean
krun /tmp/audit-work/inttof-adversarial.mpy \
  --definition /reference/k-proof/runtime-kompiled
```

The Lean run records binary64 bit patterns for zero, signed values, the
`2^53` rounding boundary, `2^1023`, and overflow at `2^1024`. A separate Python
binary64 oracle was run for the same values. Results:
`14-lean-parameter-adversarial-values.log`,
`15-k-inttof-adversarial-values.log`, and
`16-python-binary64-oracle.log`.

Counterfactual proof copies were built after changing both definitions to the
constant `0.0`, and after changing only `proofIntToF` to `0.0`:

```sh
LD_PRELOAD=/tmp/audit-work/lean-readlink-shim.so lake build
```

The both-constant mutation built, while the one-sided mutation failed at
`rfl`. Results: `17b-counterfactual-constant-build.log` and
`18-counterfactual-mismatch-build.log`.

## Trusted Stage 5 mechanical gate

```sh
LD_PRELOAD=/tmp/audit-work/lean-readlink-shim.so \
PYTHONPATH=/reference \
python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation \
  --candidate /candidate
```

Result: `20-stage5-mechanical-check.log`.
