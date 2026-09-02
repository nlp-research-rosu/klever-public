# Audit commands and result files

All paths below are inside the audit container. Output captured with `tee` is
stored beside this file.

## Inventory reconstruction

```bash
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Full result: `inventory-reconstruction.json`. The independent ordered
bijection comparison is in `inventory-bijection.txt`, and the semantic
classification is in `independent-classification.md`.

## Provenance, tree hashes, obligation map, and target

```bash
PYTHONPATH=/reference python3 /audit-output/evidence/verify_provenance.py
```

Full result: `provenance-verification.json`.

Producer file hashes were also computed directly:

```bash
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
```

The result is included in `provenance-verification.json`.

## Trusted Stage 4 preflight

The first call, without a sandbox workaround, was:

```bash
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

It failed before checking the project because Lean/Lake could not self-locate
in the audit sandbox's PID namespace. Exact output and exit status:
`check-generation-initial-failure.log` and
`check-generation-initial-failure.status`.

The narrow `/proc/<pid>/exe` to `/proc/self/exe` preload workaround was built
with:

```bash
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc-self-exe-shim.so \
  /tmp/audit-work/proc-self-exe-shim.c -ldl
```

Source and hash: `proc-self-exe-shim.c` and `audit-helper-hashes.txt`.

The successful rerun was:

```bash
LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so \
PYTHONPATH=/reference \
python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Full returned evidence: `check-generation-rerun.json`.

## Fresh Stage 5 proof build

The candidate and immutable generated Base were assembled at the path recorded
in `stage5-fresh-path.txt`:

```bash
mkdir -p /tmp/audit-work/stage5-fresh-001
cp -a /candidate/. /tmp/audit-work/stage5-fresh-001/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/stage5-fresh-001/Base/
```

The required commands were then run:

```bash
cd /tmp/audit-work/stage5-fresh-001
LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so lake clean
LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so lake build
```

Complete output and status:

- `stage5-lake-clean.log`, `stage5-lake-clean.status`
- `stage5-lake-build.log`, `stage5-lake-build.status`
- `stage5-fresh-tree.txt`

The trusted mechanical final gate was independently rerun with:

```bash
LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so \
PYTHONPATH=/reference \
python3 -c \
  'import json; from pathlib import Path; from tools.klean_final_gate import evaluate_proof_candidate; print(json.dumps(evaluate_proof_candidate(Path("/reference/klean-generation"), Path("/candidate")), indent=2, sort_keys=True))'
```

Full result: `stage5-mechanical-gate.json`.

## Axiom and adversarial checks

`AuditPrint.lean` contains:

```lean
import Proof
#print axioms Proof.final
```

It was run with:

```bash
cd /tmp/audit-work/stage5-fresh-001
LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so \
  lake env lean AuditPrint.lean
```

Exact output and accounting: `print-axioms.log`, `print-axioms.status`, and
`axiom-accounting.txt`.

`BridgeAudit.lean` proves both that the generated target accepts arbitrary
constant definitions by eliminating the empty `SortScope`, and that the
candidate `_Map_` is not commutative on two disjoint singleton maps. It was run
with:

```bash
cd /tmp/audit-work/stage5-fresh-001
LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so \
  lake env lean BridgeAudit.lean
```

Source, exact output, and status: `BridgeAudit.lean`,
`bridge-adversarial.log`, and `bridge-adversarial.status`.

Candidate/target hashes, forbidden-token results, exact-def counts, and exact
`Proof.final` statement comparison are in `stage5-integrity.txt`.
Relevant frozen, K builtin, generated, and candidate source excerpts are in
`source-excerpts.txt`.
