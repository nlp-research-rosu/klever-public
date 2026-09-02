# Audit commands

The evidence logs were produced with these commands from `/audit-output`.

```bash
PYTHONPATH=/reference python3 evidence/inventory_audit.py
PYTHONPATH=/reference python3 evidence/hash_and_manifest_audit.py
python3 evidence/summary_semantics_check.py
PYTHONPATH=/reference python3 evidence/run_generation_preflight.py
gcc -shared -fPIC -O2 -o /tmp/proc_exe_compat.so evidence/proc_exe_compat.c -ldl
LD_PRELOAD=/tmp/proc_exe_compat.so PYTHONPATH=/reference python3 evidence/run_generation_preflight.py
rg -n 'targetStatement' /reference/klean-generation/generated -g '*.lean'
rg -n '\b(sorry|admit|unsafe)\b' /reference/klean-generation/generated -g '*.lean'
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/prompt.py
nl -ba /reference/k-proof/reference-semantics/semantics/int.k
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k
nl -ba /reference/k-proof/reference-semantics/semantics/list.k
PYTHONPATH=/reference python3 -c 'from tools import klean_export, pipeline_contract; ...'
```
