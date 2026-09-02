# Audit commands

All mounted inputs under `/reference`, `/candidate`, and `/audit-input.json`
were treated as read-only. The writable isolated project was
`/tmp/audit-work/stage5-review`.

The managed PID namespace does not expose `/proc/<getpid()>/exe`, which Lean
4.22 uses for `IO.appPath`. The first two preflight attempts therefore failed
before elaboration; their complete results are in
`03_check_generation.log` and `04_check_generation_pinned_toolchain.log`.
`proc_exe_compat.c` is the narrowly scoped compatibility source used in all
successful Lean commands. It intercepts only the numeric self-executable
`readlink` and answers it from `AT_EXECFN`.

## Producer and input hashes

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/recompute_hashes.py
```

Result: `01_hash_provenance.log`.

Every per-file Stage 1 source hash recorded by the launcher was checked with:

```sh
python3 /audit-output/evidence/verify_stage1_source_hashes.py
```

Result: `17_stage1_source_hashes.log`.

## Canonical rule inventory

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/compare_inventory.py
```

Result: `02_inventory_reconstruction.log`.

## Required Stage 4 preflight

Initial environment-failing attempt:

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py
```

Pinned-path attempt before the PID compatibility fix:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
PYTHONPATH=/reference \
python3 /audit-output/evidence/run_preflight.py
```

Compatibility library build:

```sh
gcc -shared -fPIC -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc_exe_compat.so \
  /audit-output/evidence/proc_exe_compat.c -ldl
```

Successful required call:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
PYTHONPATH=/reference \
python3 /audit-output/evidence/run_preflight.py
```

Result: `05_check_generation_compat.log`.

## Isolated Stage 5 clean build

```sh
test ! -e /tmp/audit-work/stage5-review
mkdir -p /tmp/audit-work/stage5-review
cp -a /candidate/. /tmp/audit-work/stage5-review/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/stage5-review/Base/
```

From `/tmp/audit-work/stage5-review`:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
lake clean

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
lake build
```

Complete results: `06_stage5_lake_clean.log` and
`07_stage5_lake_build.log`.

## Proof and axiom identity

`PrintAxioms.lean` contained:

```lean
import Proof
#print axioms Proof.final
```

It was run with:

```sh
lake env lean PrintAxioms.lean
```

under the same pinned environment. Exact result: `08_print_axioms.log`.

The exact printed bridge definitions, theorem type, and generated target were
obtained with:

```sh
lake env lean PrintProof.lean
```

Result: `12_print_proof_identity.log`.

The trusted mechanical proof gate was run with:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
PYTHONPATH=/reference \
python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation \
  --candidate /candidate
```

Result: `13_stage5_mechanical_gate.log`.

## Independent Stage 4/5 identity and bridge checks

```sh
python3 /audit-output/evidence/verify_stage4_stage5.py
lake env lean BridgeAudit.lean
```

The Lean command used the pinned environment above. Results:
`10_stage4_stage5_identity.log`, `11_bridge_adversarial.log`, and the expanded
mutation run `15_bridge_mutation_checks.log`.

Frozen source/semantics excerpts and compiled KORE bindings are preserved in
`14_frozen_source_semantics.log` and `16_kore_symbol_bindings.log`.
