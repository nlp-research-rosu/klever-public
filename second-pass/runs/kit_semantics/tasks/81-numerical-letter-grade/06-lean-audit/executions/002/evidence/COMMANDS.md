# Audit command index

Each command below was run against the mounted read-only inputs. Complete stdout/stderr is in the named evidence file.

## Environment and producer provenance

```sh
printf 'AUDIT_MODE=%s\n' "$AUDIT_MODE"
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
```

Results: `00-environment-and-files.txt`, `01-producer-provenance.txt`, `01b-producer-manifests.txt`, and `05-recorded-hash-recalculation.txt`.

The producer bundle/tree hashes were recomputed with the launcher algorithms:

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools import pipeline_contract, klean_export
print(pipeline_contract.sha256_tree(Path('/reference/generation-tools')))
print(klean_export.tree_digest(Path('/reference/klean-generation/generated')))
PY
```

## Canonical inventory and bijection

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path('/reference/k-proof')), sort_keys=True, indent=2))
PY
```

Results: `02-reconstructed-rule-inventory.txt`, `06b-inventory-discovery-bijection.txt`, and `07-stage1-proof-order-and-uses.txt`.

## Stage 4 preflight

The sandbox hides `/proc/<current-pid>/exe` while exposing `/proc/self/exe`. Lean 4.22 therefore required a narrowly scoped `LD_PRELOAD` shim that redirects only the former self lookup to the latter. The shim was compiled as follows; its successful version output is in `10-lean-procself-workaround.txt`.

```sh
cc -shared -fPIC -o /tmp/audit-work/lean_procself_shim.so \
  /tmp/audit-work/lean_procself_shim.c -ldl
LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so lake --version
```

The exact preflight call was:

```sh
PYTHONPATH=/reference LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
print(json.dumps(result, sort_keys=True, indent=2))
PY
```

The first unshimmed environment failure is preserved in `08-rerun-klean-preflight.txt`; the successful exact rerun is `11-rerun-klean-preflight-success.txt`. Independent Stage 4 checks are in `12-stage4-obligations-and-target.txt`, `13-independent-obligation-target-bijection.txt`, and `24-all-accessible-recorded-hashes.txt`.

## Fresh Stage 5 rebuild

```sh
mkdir -p /tmp/audit-work/stage5-fresh-001/Base
cp -a /candidate/Proof.lean /candidate/lakefile.lean /candidate/lean-toolchain \
  /tmp/audit-work/stage5-fresh-001/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/stage5-fresh-001/Base/
cd /tmp/audit-work/stage5-fresh-001
LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so lake build
```

Complete output: `15-fresh-stage5-assembly.txt` and `16-fresh-lake-clean-build.txt`. Post-build target and forbidden-token checks are in `18-postbuild-target-and-forbidden-checks.txt`.

## Proof identity and axioms

`PrintAxioms.lean` contained exactly:

```lean
import Proof
#print axioms Proof.final
```

It was run with:

```sh
cd /tmp/audit-work/stage5-fresh-001
LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so lake env lean PrintAxioms.lean
```

Exact Lean output: `17-print-axioms-Proof-final.txt`; reconciliation: `19b-axiom-reconciliation.txt`. The exact `#print Proof.final` output is in `20-print-Proof-final.txt`.

## Operational bridge and adversarial checks

```sh
cd /tmp/audit-work/stage5-fresh-001
LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so lake env lean BridgeChecks.lean
```

The symbolic constructor/hook equations passed; output is `21d-operational-bridge-final-checks.txt`. The audit then built three isolated counterfactual copies:

```sh
# Wrong Int/Float equality dispatch: expected failure.
cd /tmp/audit-work/stage5-mutation-bad-apply
LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so lake build

# Constant-false guard: expected success, demonstrating target vacuity if the bridge is dishonest.
cd /tmp/audit-work/stage5-mutation-vacuous-guard
LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so lake build

# Hard-coded Int promotion: expected success, demonstrating why the operational bridge is audited independently.
cd /tmp/audit-work/stage5-mutation-hardcoded-promotion
LD_PRELOAD=/tmp/audit-work/lean_procself_shim.so lake build
```

Results: `22-counterfactual-bad-apply-mutation.txt`, `23-counterfactual-vacuous-guard-mutation.txt`, and `25-counterfactual-hardcoded-promotion-mutation.txt`.
