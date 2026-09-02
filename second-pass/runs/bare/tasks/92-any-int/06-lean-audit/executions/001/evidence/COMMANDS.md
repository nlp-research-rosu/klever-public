# Audit command ledger

All paths below were read-only except `/audit-output` and
`/tmp/audit-work`. The `script -q -e -c ... LOG` wrapper captured complete
stdout/stderr and the command exit code in each named log.

## Producer provenance and immutable hashes

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/lemma-discovery.json \
  /audit-input.json
```

Result: exit 0; `01-producer-and-manifest-hashes.log`.

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_producer_provenance.py
```

Result: exit 0, `all_checks_pass: true`;
`02-producer-provenance-contract-hash.log`.

The earlier diagnostic in
`02a-diagnostic-klean-tree-digest-not-contract-hash.log` deliberately records
why the Klean generated-tree algorithm must not be substituted for the
launcher's producer-bundle algorithm. The contract algorithm gives the exact
recorded bundle hash.

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_recorded_hashes.py
```

Result: exit 0, `all_checks_pass: true`; `05-recorded-hashes.log`.

## Canonical inventory and classification evidence

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_inventory.py
```

Result: exit 0; `03-reconstructed-inventory.log`.

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_inventory_bijection.py
```

Result: exit 0, `all_checks_pass: true`; `04-inventory-bijection.log`.

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/semantic.k
```

Results: exit 0; `06-verification-source-numbered.log` and
`07-operational-semantics-numbered.log`.

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_program_definitions.py
```

Result: exit 0, `all_checks_pass: true`;
`14-program-definition-classification.log`.

## Required Stage 4 preflight

The trusted function call is recorded in `run_check_generation.py`:

```python
check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

The audit sandbox denied Lean's internal
`readlink("/proc/<pid>/exe")`. The two unmodified-toolchain failures are
preserved in `08a-check-generation-environment-failure.log` and
`08b-check-generation-lean-proc-failure.log`. A narrow compatibility shim,
whose exact source is `proc_exe_readlink_shim.c`, returns the actual executable
path only for that query and delegates every other `readlink` call.

```sh
cc -shared -fPIC -O2 \
  -o /tmp/audit-work/proc_exe_readlink_shim.so \
  /tmp/audit-work/proc_exe_readlink_shim.c -ldl
```

Source and binary hashes are in `08c-proc-exe-shim-hashes.log`. The pinned
version check is in `08d-lean-version-with-sandbox-shim.log`.

```sh
PATH=/tmp/audit-work/lake-bin:/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/usr/local/bin:/usr/bin:/bin \
LAKE_HOME=/tmp/audit-work/lake-home \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_LIBRARY_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/lib/lean \
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so \
PYTHONPATH=/reference \
python3 /audit-output/evidence/run_check_generation.py
```

Result: exit 0, `KLEAN_NO_OBLIGATIONS`, zero obligations, null target, and
successful `lake clean` plus `lake build`; `08-check-generation.log`.

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_stage4_structure.py
```

Result: exit 0, `all_checks_pass: true`; `09-stage4-structure.log`.

## Fresh K semantic execution

The frozen Stage 1 source was copied to `/tmp/audit-work/k-stage1`. The
untrusted `prove.sh` was not executed.

```sh
kompile verification.k --backend haskell \
  --main-module ANY-INT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Result: exit 0; `11-fresh-k-kompile.log`.

```sh
kprove spec.k --definition verification-kompiled \
  --spec-module ANY-INT-SPEC
```

Result: exit 0 and `#Top`; `12-fresh-k-prove.log`.

```sh
krun --definition verification-kompiled \
  -cPGM='RunAnyInt(intVal(5), intVal(2), intVal(7))'
krun --definition verification-kompiled \
  -cPGM='RunAnyInt(intVal(3), intVal(2), intVal(2))'
krun --definition verification-kompiled \
  -cPGM='RunAnyInt(intVal(3), intVal(-2), intVal(1))'
krun --definition verification-kompiled \
  -cPGM='RunAnyInt(boolVal(true), intVal(1), intVal(1))'
```

Results: all exit 0 and produce, respectively, `true`, `false`, `true`, and
`false`; `13a-krun-5-2-7.log` through `13d-krun-bool-1-1.log`.

## Stage 5

No Stage 5 commands were run. `AUDIT_MODE` and `/audit-input.json` both select
`CLASSIFICATION_ONLY`, Stage 4 has no obligations or target, all Stage 5 paths
are null, and `/candidate` is absent.
