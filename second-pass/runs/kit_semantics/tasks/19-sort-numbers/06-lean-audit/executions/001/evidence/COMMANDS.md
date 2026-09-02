# Audit commands

All commands were run from `/audit-output` unless a different working
directory is stated. `script -q -e -c ... LOG` preserved terminal output and
the exit code in each named log.

## Producer provenance

```sh
script -q -e -c 'sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py; printf "%s\n" "=== source-manifest ==="; sed -n "1,80p" /reference/generation-tools/source-manifest.json; printf "%s\n" "=== generator source/image fields ==="; rg -n "exporter_sha256|klean_py_sha256|generator_image_id" /reference/klean-generation/generator-manifest.json; printf "%s\n" "=== audit-input producer source path/tree hash ==="; rg -n "generation_producer_sources|generation_producer_sources_sha256" /audit-input.json' /audit-output/evidence/producer-provenance.log
```

Result: `producer-provenance.log`, exit 0.

## Inventory, classifications, and all structural/hash bindings

```sh
script -q -e -c 'PYTHONPATH=/reference python3 /audit-output/evidence/audit_checks.py' /audit-output/evidence/structural-checks.log
```

Result: `structural-checks.log`, exit 0, `all_checks_pass: true`, no failed
checks. The executed source is `audit_checks.py`.

## Frozen source and supplied operational rules used for classification

```sh
script -q -e -c 'printf "%s\n" "=== verification.k ==="; nl -ba /reference/k-proof/verification.k; printf "%s\n" "=== source solution.py ==="; nl -ba /reference/k-proof/solution.py; printf "%s\n" "=== translated solution.mpy ==="; nl -ba /reference/k-proof/solution.mpy; printf "%s\n" "=== main spec claim ==="; nl -ba /reference/k-proof/spec.k | sed -n "1,35p"; printf "%s\n" "=== call semantics ==="; nl -ba /reference/k-proof/reference-semantics/semantics/call.k | sed -n "1,90p"; printf "%s\n" "=== function frame semantics ==="; nl -ba /reference/k-proof/reference-semantics/semantics/functions.k | sed -n "1,100p"; printf "%s\n" "=== split/join semantics ==="; nl -ba /reference/k-proof/reference-semantics/semantics/methods.k | sed -n "1,90p"; printf "%s\n" "=== supplied sorting semantics ==="; nl -ba /reference/k-proof/reference-semantics/semantics/sort.k | sed -n "1,85p"; printf "%s\n" "=== tuple index semantics ==="; nl -ba /reference/k-proof/reference-semantics/semantics/tuple.k | sed -n "1,35p"' /audit-output/evidence/operational-source.log
```

Result: `operational-source.log`, exit 0.

## Trusted fresh Stage 4 preflight

The direct mandated API call was:

```sh
script -q -e -c 'PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py' /audit-output/evidence/fresh-preflight.log
```

The trusted API reached `lake clean`, then failed because Lean's application
path lookup could not see its namespace PID in the sandbox-mounted `/proc`.
Result: `fresh-preflight.log`, exit 1.

The diagnosis was reproduced with:

```sh
cc -shared -fPIC -O2 -o /tmp/audit-work/path_probe.so /audit-output/evidence/path_probe.c -ldl
script -q -e -c 'LD_PRELOAD=/tmp/audit-work/path_probe.so lean --version || true' /audit-output/evidence/lean-path-diagnostic.log
```

Result: `lean-path-diagnostic.log` records
`readlink(/proc/<namespace-pid>/exe) = -1 errno=2`.

A narrow compatibility shim, whose complete source is
`proc_exe_compat.c`, redirects only that `/proc/<pid>/exe` read to
`/proc/self/exe`:

```sh
cc -shared -fPIC -O2 -o /tmp/audit-work/proc_exe_compat.so /audit-output/evidence/proc_exe_compat.c -ldl
```

The pinned toolchain was validated from
`/reference/klean-generation/generated`:

```sh
script -q -e -c 'LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lean --version && LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake env lean --version' /audit-output/evidence/lean-path-compat-validation.log
```

Result: both commands identify Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The exact trusted preflight API was then rerun:

```sh
script -q -e -c 'LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py' /audit-output/evidence/fresh-preflight-compat.log
```

Result: `fresh-preflight-compat.log`, exit 0,
`status: KLEAN_NO_OBLIGATIONS`; both `lake clean` and `lake build` exited 0.
