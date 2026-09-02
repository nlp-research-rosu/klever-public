# Audit command index

The `.log` files are raw `script(1)` transcripts. Each transcript records its
command, timestamps, combined output, and exit code.

## Producer provenance and all launcher-recorded hashes

```sh
env PYTHONPATH=/reference AUDIT_MODE="$AUDIT_MODE" \
  python3 /audit-output/evidence/00_provenance_check.py
```

Raw result: `00_provenance_check.log` (exit 0).

## Canonical inventory reconstruction and exact manifest comparison

```sh
env PYTHONPATH=/reference \
  python3 /audit-output/evidence/01_inventory_check.py
```

Raw result: `01_inventory_check.log` (exit 0).

## Required trusted Stage 4 preflight

```sh
env PYTHONPATH=/reference \
  python3 /audit-output/evidence/02_preflight_rerun.py
```

The first raw result, `02_preflight_rerun.log`, exits 1 because the audit
image's Elan proxy cannot detect its Lake installation. A temporary launcher
was compiled from `02_lean_environment_wrapper.c` against the pinned
`/opt/elan/toolchains/leanprover--lean4---v4.22.0/lib/lean/libleanshared.so`.
No mounted input was changed. The temporary sysroot was populated with the
launcher and links to that pinned toolchain, then the same command was rerun
with:

```sh
cc -O2 \
  -I/opt/elan/toolchains/leanprover--lean4---v4.22.0/include \
  /tmp/audit-work/lean_wrapper.c \
  -L/opt/elan/toolchains/leanprover--lean4---v4.22.0/lib/lean \
  -Wl,-rpath,/opt/elan/toolchains/leanprover--lean4---v4.22.0/lib/lean \
  -lleanshared -o /tmp/audit-work/lean-fixed
export LEAN_SYSROOT=/tmp/audit-work/lean-sysroot.<mktemp>
export LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
env PYTHONPATH=/reference \
  python3 /audit-output/evidence/02_preflight_rerun.py
```

`02_preflight_rerun_success.log` preserves an intermediate wrapper-parser
failure. The final raw result is `02_preflight_rerun_success_2.log` (exit 0).
The exact returned document is also `02_preflight_return.json`.

## Obligation/source-rule bijection and target identity

```sh
env PYTHONPATH=/reference \
  python3 /audit-output/evidence/03_manifest_bijection_check.py
```

Final raw result: `03_manifest_bijection_check_2.log` (exit 0).

## Frozen source and operational recurrence checks

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/semantic.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
python3 /audit-output/evidence/04_semantic_model_check.py
```

Raw results: `04_frozen_source_listing.log` and
`04_semantic_model_check.log` (both exit 0).

## Published review validation

```sh
python3 /audit-output/evidence/05_review_validation.py
```

Raw result: `05_review_validation.log` (exit 0).
