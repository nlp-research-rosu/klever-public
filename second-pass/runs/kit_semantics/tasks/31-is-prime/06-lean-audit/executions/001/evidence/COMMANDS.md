# Audit command record

The helper sources named below are stored in this directory. The corresponding
`.log` files are raw `script(1)` transcripts with exit codes.

## Rule inventory reconstruction

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
```

Result: exit 0; see `01_inventory_reconstruction.log`.

## Producer provenance gate

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/check_producer_provenance.py
```

Result: exit 0; see `02_producer_provenance.log`.

## Required trusted Stage 4 preflight (first attempt)

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/rerun_preflight.py
```

Result: exit 1 before artifact judgment because unmodified Lean could not
resolve `/proc/<pid>/exe`; see `03_preflight_rerun.log`.

## Sandbox `/proc` diagnosis and compatibility shim

```sh
cc -shared -fPIC /audit-output/evidence/trace_readlink.c \
  -o /tmp/audit-work/trace_readlink.so
cc -shared -fPIC /audit-output/evidence/proc_self_exe_shim.c \
  -o /tmp/audit-work/proc_self_exe_shim.so
lean --version
LD_PRELOAD=/tmp/audit-work/trace_readlink.so lean --version
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so lean --version
cd /reference/klean-generation/generated
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so lake --version
```

The trace showed Lean reading a hidden numeric proc path. The narrow shim maps
only `/proc/<digits>/exe` to the equivalent exposed `/proc/self/exe`. See
`07_lean_environment_diagnosis.log`.

## Required trusted Stage 4 preflight (successful rerun)

```sh
env PYTHONPATH=/reference \
  LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
  python3 /audit-output/evidence/rerun_preflight.py
```

Result: exit 0, `KLEAN_NO_OBLIGATIONS`; the trusted checker internally ran
`lake clean` and `lake build`, both exit 0. See
`04_preflight_rerun_with_proc_shim.log`.

## Independent hashes, bijection, and target identity

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/verify_stage4_integrity.py
```

Result: exit 0; see `05_stage4_integrity.log`.

## Operational K witnesses

```sh
krun /audit-output/evidence/classification-witnesses.mpy \
  --definition /reference/k-proof/runtime-kompiled
```

Result: exit 0; see `06_operational_witnesses.log`.
