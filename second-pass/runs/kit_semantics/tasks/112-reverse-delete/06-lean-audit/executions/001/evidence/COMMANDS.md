# Audit commands

The successful canonical inventory and hash run was:

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/independent_checks.py
```

Its complete result is in `independent-checks-final.log`.

The requested trusted Stage 4 preflight entry point was invoked by
`run_preflight.py`, whose only substantive call is:

```python
check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

The initial command was:

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py
```

It reached `lake clean` but failed because the command sandbox's PID namespace
was paired with the parent namespace's `/proc`, preventing Lean from locating
its executable. The failure is preserved in `check-generation.log`.

After compiling the narrow `/proc/<pid>/exe` readlink compatibility shim whose
source is preserved as `fix_proc_exe.c` (and was compiled from the identical
working copy `/tmp/audit-work/fix_proc_exe.c`), the successful command was:

```sh
LD_PRELOAD=/tmp/audit-work/libfix_proc_exe.so \
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
PYTHONPATH=/reference \
python3 /audit-output/evidence/run_preflight.py
```

The shim compile/version result is in `lean-proc-shim-pass.log`. The complete
successful preflight result is in `check-generation-pass.log` and its returned
JSON is in `check-generation-return.json`.

The read-only source and manifest inspection was:

```sh
bash /audit-output/evidence/read_only_inspection.sh
```

Its traced commands and complete output are in `read-only-inspection.log`.
