# Audit commands

The mounted candidate and provenance files were inspected only as data. No
script or instruction from those inputs was executed.

## Inventory and classification

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/inventory_audit.py
```

Complete result: `inventory-audit.log`.

## Signed hashes, manifests, obligation map, and target

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/hash_and_manifest_audit.py
```

Complete result: `hash-and-manifest-audit-v2.log`.

The generated target was also scanned independently of the manifest helpers:

```sh
rg -n --glob '*.lean' \
  '^[[:space:]]*def[[:space:]]+targetStatement\b' \
  /reference/klean-generation/generated
```

`independent-target-scan.log` records `TARGET_DECLARATION_COUNT=0`.
`obligation-map-raw.log` records the complete raw obligation map.

## Required trusted preflight API

The first direct invocation was:

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_preflight.py
```

Complete result: `preflight-rerun.log`. It failed before a project command
could run because this sandbox does not expose `/proc/<current-pid>/exe`,
which Lean 4.22 uses to locate its executable.

The compatibility shim was built from the recorded source:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /audit-output/evidence/proc-exe-readlink-shim.so \
  /audit-output/evidence/proc-exe-readlink-shim.c -ldl
```

The same trusted API was then rerun with only the process-executable lookup
shim enabled:

```sh
PYTHONPATH=/reference \
LD_PRELOAD=/audit-output/evidence/proc-exe-readlink-shim.so \
  python3 /audit-output/evidence/run_preflight.py
```

Complete returned evidence: `preflight-rerun-with-proc-shim.log`. The nested
`lake clean` and `lake build` outputs are complete because the build output is
shorter than the preflight API's 4000-character retained-output limit.

## Final mechanical gate

```sh
PYTHONPATH=/reference \
LD_PRELOAD=/audit-output/evidence/proc-exe-readlink-shim.so \
  python3 /reference/tools/klean_final_gate.py \
    --frozen-k /reference/k-proof \
    --discovery-manifest /reference/lemma-discovery.json \
    --generation /reference/klean-generation \
    --toolchain-lock /reference/klean-toolchain.lock.json \
    --audit-input /audit-input.json
```

Complete result: `final-mechanical-gate.log`.

## Toolchain diagnostic

The shim's narrow effect and the pinned toolchain were checked with:

```sh
LD_PRELOAD=/audit-output/evidence/proc-exe-readlink-shim.so lean --version
```

Observed:

```text
Lean (version 4.22.0, x86_64-unknown-linux-gnu,
commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05, Release)
```
