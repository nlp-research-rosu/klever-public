# Audit commands

All paths below are the mounted read-only inputs or audit-owned evidence paths.
The `script` wrapper preserves the raw stdout/stderr and exit status.

## Canonical inventory, classification, and hash checks

```sh
script -q -e \
  -c 'PYTHONPATH=/reference python3 /audit-output/evidence/independent_checks.py' \
  /audit-output/evidence/independent_checks.log
```

Result: exit 0; 101/101 checks passed. The earlier
`independent_checks.initial-failure.log` preserves a discarded comparison that
incorrectly treated historical generator-image source hashes as hashes of the
distinct audit-time tools. The final script records both sets without equating
their provenance scopes.

## Required trusted Stage 4 preflight

Initial invocation:

```sh
script -q -e \
  -c 'PYTHONPATH=/reference python3 /audit-output/evidence/run_check_generation.py' \
  /audit-output/evidence/check_generation.initial-toolchain-failure.log
```

Result: the project-independent `lake clean` launcher failed because Lean 4.22
could not locate its executable through this audit sandbox's PID-namespace
view of `/proc`.

The compatibility shim was compiled and checked:

```sh
script -q -e \
  -c 'gcc -shared -fPIC -O2 -Wall -Wextra -o /tmp/audit-work/proc_exe_compat.so /audit-output/evidence/proc_exe_compat.c -ldl && LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lean --version && LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lean --print-prefix' \
  /audit-output/evidence/lean_runtime_compat.log
```

It rewrites only `/proc/<digits>/exe` readlink requests to
`/proc/self/exe`. It does not alter the generated project, checker, or Lean
source.

Successful required invocation:

```sh
script -q -e \
  -c 'LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so PYTHONPATH=/reference python3 /audit-output/evidence/run_check_generation.py' \
  /audit-output/evidence/check_generation.log
```

`run_check_generation.py` directly calls:

```python
tools.klean_preflight.check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

Result: exit 0, `KLEAN_NO_OBLIGATIONS`, obligation count 0, target `null`;
both internal commands (`lake clean`, `lake build`) exited 0.

The fresh return value was compared to both recorded copies:

```sh
script -q -e \
  -c 'python3 /audit-output/evidence/compare_preflight.py' \
  /audit-output/evidence/compare_preflight.log
```

Result: exit 0; fresh, selected, and signed preflight JSON values are equal.

## Independent operational/fold sensitivity

```sh
script -q -e \
  -c 'python3 /audit-output/evidence/fold_semantics_check.py' \
  /audit-output/evidence/fold_semantics_check.log
```

Result: exit 0; 3,906 bounded sequences agreed with the independently written
operational oracle. Deliberately selecting the wrong negative or positive
extremum caused 1,540 mismatches in each mutation.
