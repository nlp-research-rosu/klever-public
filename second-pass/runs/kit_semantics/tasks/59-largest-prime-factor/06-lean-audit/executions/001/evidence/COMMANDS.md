# Reproduction commands

Run all Python checks against the trusted `/reference/tools` package:

```bash
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
PYTHONPATH=/reference python3 /audit-output/evidence/verify_hashes.py
PYTHONPATH=/reference python3 /audit-output/evidence/audit_stage4.py
python3 /audit-output/evidence/summary_witnesses.py
```

The audit sandbox needs the narrowly scoped `/proc/self/exe` workaround
recorded in `06-lean-proc-self-shim.c` for Lean 4.22:

```bash
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean_proc_self_shim.so \
  /audit-output/evidence/06-lean-proc-self-shim.c
export PYTHONPATH=/reference
export LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so
export LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LEAN=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean
export LEAN_AR=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/llvm-ar
export LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
python3 /audit-output/evidence/run_preflight.py
```

The direct frozen-source/semantics inspection commands were:

```bash
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
sed -n '1,180p' /reference/k-proof/reference-semantics/semantics/operators.k
sed -n '1,130p' /reference/k-proof/reference-semantics/semantics/int.k
sed -n '1,125p' /reference/k-proof/reference-semantics/semantics/controls.k
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
```
