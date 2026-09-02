# Audit command index

The `script -q -e -c ...` wrapper captured complete stdout/stderr and the exit
code in each named `.log` file. The substantive commands were:

```sh
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
```

Captured with the manifests in `01_producer_and_manifests.log` and cross-checked
in `04_producer_provenance_crosscheck.log`.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
```

Captured in `06_inventory_reconstruction.log`.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/verify_recorded_hashes.py
```

The final complete run is captured in `29_recorded_hashes_complete.log`.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/run_check_generation.py
```

The initial run is captured in `09_check_generation.log`; it failed because
Lean 4.22 used `/proc/<namespace-pid>/exe` in a sandbox whose `/proc` exposes
host PIDs.

The diagnosis and minimal environment repair were:

```sh
gcc -shared -fPIC /tmp/audit-work/hostpid_preload.c -o /tmp/audit-work/libhostpid_preload.so
LD_PRELOAD=/tmp/audit-work/libhostpid_preload.so lean --version
LD_PRELOAD=/tmp/audit-work/libhostpid_preload.so lake --version
```

Captured in `24_pid_exe_test.log` and `25_pid_namespace_workaround.log`.

The unchanged trusted checker was then rerun with the repaired process
environment:

```sh
PYTHONPATH=/reference LD_PRELOAD=/tmp/audit-work/libhostpid_preload.so \
  python3 /audit-output/evidence/run_check_generation.py
```

Captured in `26_check_generation_rerun.log`.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/compare_preflight_evidence.py
PYTHONPATH=/reference python3 /audit-output/evidence/check_bijection_and_target.py
python3 /audit-output/evidence/definition_witnesses.py
```

Captured in `30_preflight_evidence_comparison.log`,
`28_bijection_and_target.log`, and `31_definition_witnesses.log` respectively.

