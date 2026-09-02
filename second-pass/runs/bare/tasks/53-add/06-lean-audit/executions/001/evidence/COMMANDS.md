# Audit command index

All paths below are the immutable mounted inputs or fresh audit copies. The
corresponding `.log` files contain the complete terminal output and the exit
code recorded by `script`.

## Producer and manifest evidence

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
nl -ba /reference/generation-tools/source-manifest.json
nl -ba /reference/klean-generation/generator-manifest.json
nl -ba /reference/klean-generation/generated/obligation-map.json
nl -ba /reference/lemma-discovery.json
```

Results:

- `producer_sha256.log`
- `producer_source_manifest.log`
- `generator_manifest.log`
- `obligation_map.log`
- `lemma_discovery_manifest.log`

## Inventory reconstruction and Stage 3 contract

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'

PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
```

Results:

- `inventory_reconstruction.log`
- `stage3_bijection.log`

The frozen sources were inspected with:

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/semantic.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
```

Results are in the `frozen_*_source.log` files and
`frozen_solution_mpy.log`.

## Hash reconciliation

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/hash_audit.py
```

Result: `hash_audit.log`.

## Stage 4 preflight and independent structural gate

The required first preflight attempt was:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

It reached `lake clean` and failed because this sandbox does not expose child
PIDs through `/proc`; see `preflight_rerun.log`.

The environment-only repair and successful rerun were:

```sh
cc -shared -fPIC -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc_exe_shim.so \
  /audit-output/evidence/proc_exe_shim.c -ldl

LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so \
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'

python3 /audit-output/evidence/stage4_structure_audit.py
```

Results:

- `preflight_rerun_with_proc_shim.log`
- `stage4_structure_audit.log`
- `lean_version_with_proc_shim.log`

The shim only supplies Lean's `/proc/<pid>/exe` query with the executable path
from the already-installed pinned toolchain. Its complete source is
`proc_exe_shim.c`.

## Independent Stage 1 execution and sensitivity

The immutable workspace was copied to
`/tmp/audit-work/stage1-independent`; the mounted `prove.sh` was not executed.

```sh
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
kprove spec.k --definition verification-kompiled --spec-module SPEC

kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
kprove spec-body-mutation-audit.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION-AUDIT

krun solution.mpy --definition verification-kompiled -cARG1=0 -cARG2=0
krun solution.mpy --definition verification-kompiled -cARG1=-8 -cARG2=3
krun solution.mpy --definition verification-kompiled -cARG1=91 -cARG2=-91
krun solution.mpy --definition verification-kompiled \
  -cARG1=123456789012345678901234567890 \
  -cARG2=987654321098765432109876543210
```

Results:

- `stage1_fresh_kompile.log`
- `stage1_fresh_kprove.log`
- `stage1_false_postcondition.log`
- `stage1_body_mutation.log`
- `krun_zero.log`
- `krun_signed.log`
- `krun_cancellation.log`
- `krun_large.log`
- `kompile_version.log`, `kprove_version.log`, and `krun_version.log`
