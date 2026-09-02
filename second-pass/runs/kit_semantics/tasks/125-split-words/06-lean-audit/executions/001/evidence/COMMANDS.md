# Audit command record

All mounted candidate and provenance artifacts were read as data only. The
trusted Python modules were loaded from `/reference` by setting
`PYTHONPATH=/reference`.

## Hash and producer checks

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/check_hashes.py
```

The first preserved attempt, `01_hash_recomputation.log`, mistakenly used the
newer audit-contract framing for four pipeline-v3 artifact tree hashes. Its
expected mismatches are algorithm mismatches, not content mismatches. The
script was corrected to call `tools.pipeline_contract.sha256_tree`, the same
trusted function that created those launcher fields, and rerun as
`01b_hash_recomputation_corrected.log`; it exited 0 with `OVERALL=PASS`.

## Canonical inventory reconstruction

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/check_inventory.py
```

Result: exit 0 and `OVERALL=PASS` in
`02_inventory_reconstruction.log`.

## Trusted Stage 4 preflight

The exact function invocation is in `run_preflight.py`:

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py
```

The first preserved run, `03_preflight_rerun.log`, reached the clean-copy Lake
step and exposed a container PID/procfs mismatch: Lean attempted to read
`/proc/<namespace-pid>/exe`, which was absent even though `/proc/self/exe` was
available. `proc_exe_shim.c` is a narrow interposition that changes only a
numeric `/proc/<pid>/exe` `readlink` path to `/proc/self/exe`. After compiling
it, the trusted preflight was rerun without changing its inputs or callback:

```sh
gcc -shared -fPIC /audit-output/evidence/proc_exe_shim.c \
  -o /tmp/audit-work/proc_exe_shim.so -ldl
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so \
  PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_preflight.py
```

Result: exit 0 and `KLEAN_NO_OBLIGATIONS` in
`03b_preflight_rerun_corrected.log`, including successful `lake clean` and
`lake build` diagnostics.

## Independent classification and Stage 4 bijection

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/check_stage4.py
```

Result: exit 0 and `OVERALL=PASS` in `05_stage4_integrity.log`.

The inspected source and operational-semantic slice is preserved in
`04_stage3_semantic_slice.log`. The written independent semantic judgment is
`04_independent_classification.md`.

## Independent model-boundary witness

```sh
python3 -c 's = "\v"; print(repr(s.split())); print(s.isspace())'
sed -n '70,88p' \
  /reference/k-proof/reference-semantics/semantics/methods.k
```

Result is in `06_model_boundary.log`. It is not a Stage 3 domain lemma and not
a Stage 4 obligation; it is a supplied-operational-model adequacy boundary.
