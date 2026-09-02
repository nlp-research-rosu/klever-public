# Audit command ledger

These are the material commands whose complete results are saved in the numbered transcript files.

```bash
env | rg '^AUDIT_MODE='
python3 -m json.tool /audit-input.json
rg --files /reference/k-proof /reference/k-audit /reference/klean-generation /reference/generation-tools /reference/tools /candidate 2>&1 | sort
```

```bash
PYTHONPATH=/reference python3 /audit-output/evidence/recompute_integrity.py
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
```

```bash
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /audit-input.json
```

The initially attempted required preflight was:

```bash
PYTHONPATH=/reference python3 /audit-output/evidence/rerun_preflight.py
```

Lean environment diagnosis used:

```bash
command -v lake
command -v lean
lake --version
lean --version
elan show
elan toolchain list
```

The audit-only `/proc/*/exe` compatibility shim was built and checked with:

```bash
cc -shared -fPIC -Wall -Wextra -O2 \
  /audit-output/evidence/lean_proc_exe_shim.c -ldl \
  -o /audit-output/evidence/lean_proc_exe_shim.so
sha256sum \
  /audit-output/evidence/lean_proc_exe_shim.c \
  /audit-output/evidence/lean_proc_exe_shim.so
LD_PRELOAD=/audit-output/evidence/lean_proc_exe_shim.so \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
LD_PRELOAD=/audit-output/evidence/lean_proc_exe_shim.so \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake --version
```

The successful required preflight rerun was:

```bash
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
PYTHONPATH=/reference \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/audit-output/evidence/lean_proc_exe_shim.so \
python3 /audit-output/evidence/rerun_preflight.py
```

The independent non-preflight structural and semantic checks were:

```bash
python3 /audit-output/evidence/independent_stage4_check.py
python3 /audit-output/evidence/semantic_counterexamples.py
```
