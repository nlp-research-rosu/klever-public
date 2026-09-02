# Principal audit commands

The scripts named below are retained alongside their outputs so that the exact
logic used for each comparison is inspectable.

```bash
PYTHONPATH=/reference \
  python /audit-output/evidence/reconstruct_and_hash.py \
  > /audit-output/evidence/07_reconstructed_inventory_and_hashes.json
```

```bash
python /audit-output/evidence/semantic_recurrence_check.py \
  > /audit-output/evidence/36_semantic_recurrence_and_mutations.json
```

The first two preflight attempts are preserved in
`09_required_check_generation.txt` and
`11_required_check_generation_rerun.txt`. They failed before building because
the container's namespace PID was not mounted as `/proc/<pid>`.

The successful required preflight used the audit-local app-path shim retained
as `lean_app_path_shim.c`:

```bash
cc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/lean_app_path_shim.so \
  /audit-output/evidence/lean_app_path_shim.c -ldl

export PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/opt/elan/bin:$PATH
export LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so
PYTHONPATH=/reference \
  python /audit-output/evidence/run_required_preflight.py
```

Its complete output is `34_required_check_generation_success.txt`.

```bash
PYTHONPATH=/reference \
  python /audit-output/evidence/verify_all_recorded_hashes.py \
  > /audit-output/evidence/39_all_recorded_hashes_bijection_target.json
```

The generated-project target/declaration scan and raw manifest contents are in
`35_obligation_map_target_and_trust.txt`.
