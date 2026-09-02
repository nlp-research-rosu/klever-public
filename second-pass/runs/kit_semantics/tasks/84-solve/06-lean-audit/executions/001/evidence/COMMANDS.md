# Audit command record

All paths below are the mounted or fresh-copy paths used in this audit.

```bash
PYTHONPATH=/reference python3 /audit-output/evidence/01_inventory_audit.py

LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
PYTHONPATH=/reference \
python3 /audit-output/evidence/02_run_preflight.py

PYTHONPATH=/reference/generation-tools:/reference \
python3 /audit-output/evidence/03_integrity_audit.py

cd /tmp/audit-work/84-solve-proof-audit-2
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake clean
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake build

LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
PYTHONPATH=/reference \
python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation \
  --candidate /candidate

cd /tmp/audit-work/84-solve-proof-audit-2
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  lake env lean AxiomAudit.lean
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  lake env lean PrintFinal.lean

kompile /tmp/audit-work/int-oracle.k \
  --backend llvm \
  --main-module INT-ORACLE \
  --syntax-module INT-ORACLE \
  --output-definition /tmp/audit-work/int-oracle-kompiled
bash /audit-output/evidence/09_operational_bridge_k.sh

cd /tmp/audit-work/84-solve-proof-audit-2
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  lake env lean BridgeChecks.lean
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  lake env lean ObligationChecks.lean
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  lake env lean FalseMutation.lean

LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
PYTHONPATH=/reference \
python3 /reference/tools/klean_final_gate.py \
  --frozen-k /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --generation /reference/klean-generation \
  --candidate /candidate \
  --toolchain-lock /reference/klean-toolchain.lock.json \
  --audit-input /audit-input.json
```

The preload library is built from `proc_exe_compat.c`:

```bash
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc_exe_compat.so \
  /audit-output/evidence/proc_exe_compat.c
```

It redirects only Lean's failing `/proc/<namespace-pid>/exe` lookup to
`/proc/self/exe`. The original invocation and error are preserved in
`02_run_preflight.log`; the successful rerun is in
`02_run_preflight_rerun.log`.
