# Audit command transcript

All paths below refer to the immutable mounts described in `/audit-input.json`.
Full stdout/stderr is in the numbered evidence files.

## Inventory and Stage 3

```sh
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2))'
```

Result: [`03_reconstructed_rule_inventory.json`](03_reconstructed_rule_inventory.json).

```sh
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2))'
```

Result: [`06_stage3_trust_boundary_result.json`](06_stage3_trust_boundary_result.json).
The independent span/hash/order/bijection recomputation is in
[`07_stage3_bijection_and_hash_checks.txt`](07_stage3_bijection_and_hash_checks.txt).

## Producer authentication

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
```

Result and all three compared manifests:
[`01_stage4_producer_authentication_raw.txt`](01_stage4_producer_authentication_raw.txt).

## Required Stage 4 preflight

The first two calls reached the build phase but failed because the audit
sandbox's namespace PID is not represented in its `/proc` mount:

```sh
PYTHONPATH=/reference python3 -c '... tools.klean_preflight.check_generation(...) ...'
ELAN_HOME=/opt/elan PYTHONPATH=/reference python3 -c '... tools.klean_preflight.check_generation(...) ...'
```

Results:
[`10_fresh_check_generation_result.json`](10_fresh_check_generation_result.json)
and
[`13_fresh_check_generation_result.json`](13_fresh_check_generation_result.json).

Lean 4.22's `IO.appPath` calls `readlink("/proc/<getpid()>/exe", ...)`.
Evidence that the sandbox exposes a different host PID namespace is in
[`19_lean_runtime_probe.txt`](19_lean_runtime_probe.txt) and the relevant Lean
implementation is in
[`25_lean_io_app_path_disassembly.txt`](25_lean_io_app_path_disassembly.txt).
The narrowly scoped shim in [`lean_proc_exe_shim.c`](lean_proc_exe_shim.c)
redirects only numeric `/proc/<pid>/exe` reads to `/proc/self/exe`.

```sh
gcc -shared -fPIC /tmp/audit-work/lean_proc_exe_shim.c -ldl \
  -o /tmp/audit-work/lean_proc_exe_shim.so

LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
ELAN_HOME=/opt/elan \
PYTHONPATH=/reference \
python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Successful returned evidence:
[`27_fresh_check_generation_result.json`](27_fresh_check_generation_result.json).

## Independent Stage 4 cross-checks

The structured recomputation in
[`33_independent_manifest_and_hash_checks.txt`](33_independent_manifest_and_hash_checks.txt)
uses SHA-256 directly plus the trusted `pipeline_contract.sha256_tree` and
`klean_export.tree_digest` algorithms. It checks:

- the signed audit-input envelope;
- all mounted Stage 1, Stage 2, Stage 4, generated-project, and producer-source
  tree hashes;
- every Stage 1 per-file hash;
- producer source hashes and immutable image ID;
- exact rule/classification propagation;
- the empty source-rule/obligation/trust-parameter bijection;
- obligation-map, trust-inventory, and toolchain hashes;
- null target identity and consistent `KLEAN_NO_OBLIGATIONS` status; and
- the fresh clean/build exit codes.
