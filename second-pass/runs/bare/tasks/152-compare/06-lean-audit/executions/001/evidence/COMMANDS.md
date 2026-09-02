# Audit command record

The mounted candidate and provenance files were treated only as data. The
supplied `prove.sh` and prior audit scripts were not executed.

## Producer provenance

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
python3 -m json.tool /audit-input.json
```

Result: `initial_inputs_and_producer_hashes_complete.log`.

## Canonical inventory and Stage 3 trust boundary

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'

PYTHONPATH=/reference python3 \
  /audit-output/evidence/verify_inventory_bijection.py

PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; x=validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")); print(json.dumps(x, indent=2, sort_keys=True))'
```

Results: `reconstructed_rule_inventory.log`,
`verify_inventory_bijection.log`, and
`stage3_manifest_and_trusted_validation.log`.

## Stage 4 trusted preflight

The direct run was:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

It reached the fresh clean-build step and failed because the sandbox PID
namespace makes Lean's `/proc/<getpid()>/exe` lookup invalid. The raw failure is
in `rerun_klean_preflight.log`; diagnostics are in
`lean_toolchain_diagnostics.log`.

The narrow compatibility shim was built with:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean_proc_self_shim.so \
  /tmp/audit-work/lean_proc_self_shim.c -ldl
```

The exact shim source is `lean_proc_self_shim.c`. It changes only a
`readlink("/proc/<self-pid>/exe", ...)` request into
`readlink("/proc/self/exe", ...)`.

The successful preflight rerun was:

```sh
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Result: `rerun_klean_preflight_with_pid_shim.log`.

## Independent hash, manifest, obligation, and target checks

```sh
PYTHONPATH=/reference python3 \
  /audit-output/evidence/verify_all_recorded_hashes.py

python3 -m json.tool \
  /reference/klean-generation/generated/obligation-map.json

rg -n '^[[:space:]]*def[[:space:]]+targetStatement\b' \
  /reference/klean-generation/generated -g '*.lean'
```

Results: `verify_all_recorded_hashes_complete.log` and
`no_obligations_no_target_no_candidate.log`.

## Independent K execution-sensitivity checks

No mounted script was executed. A fresh directory was populated with only
`semantic.k`, `verification.k`, and `spec.k`, then the commands below were run:

```sh
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled --spec-module SPEC

kprove spec-vacuity-ensures.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-ENSURES

kompile verification-body-mut.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mut-kompiled

kprove spec-body-mut.k \
  --definition verification-body-mut-kompiled \
  --spec-module SPEC-BODY-MUT
```

Results: `independent_kompile_verification.log`,
`independent_kprove_spec.log`,
`independent_kprove_false_postcondition_ensures.log`,
`body_mutation_kompile.log`, and `body_mutation_kprove.log`.
