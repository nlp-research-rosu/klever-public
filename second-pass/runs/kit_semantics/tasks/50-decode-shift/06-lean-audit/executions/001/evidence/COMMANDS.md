# Audit commands

The executable audit helpers are included beside their JSON results. They read
only the mounted inputs and import only trusted code from `/reference/tools`.

```text
PYTHONPATH=/reference python3 /audit-output/evidence/01_reconstruct_inventory.py
```

Result: `01_reconstructed_inventory.json`.

```text
python3 /audit-output/evidence/02_classification_analysis.py
```

Result: `02_classification_analysis.json`.

```text
PYTHONPATH=/reference python3 /audit-output/evidence/03_stage4_integrity_preflight.py
```

The first two attempts preserved the ambient Lake failure in
`03a_stage4_integrity_preflight_initial_failure.json` and
`03b_stage4_integrity_preflight_toolchain_path_failure.json`. The successful
rerun used the narrow `/proc/<pid>/exe` compatibility shim documented below.
Its returned evidence is `03_stage4_integrity_preflight.json`; complete nested
command output is in `03c_preflight_command_1.log` and
`03c_preflight_command_2.log`.

```text
gcc -shared -fPIC -O2 -Wall -Wextra -Werror -o /tmp/audit-work/fix_lean_app_path.so /tmp/audit-work/fix_lean_app_path.c -ldl
LD_PRELOAD=/tmp/audit-work/fix_lean_app_path.so lean --version
LD_PRELOAD=/tmp/audit-work/fix_lean_app_path.so lake --version
```

Exact results: `03_lean_app_path_shim.log`. The identical source is preserved
as `03_lean_app_path_shim.c`.

```text
PYTHONPATH=/reference python3 /audit-output/evidence/04_target_absence_audit.py
```

Result: `04_target_absence_audit.json`.

```text
LD_PRELOAD=/tmp/audit-work/fix_lean_app_path.so PYTHONPATH=/reference python3 /reference/tools/klean_final_gate.py --frozen-k /reference/k-proof --discovery-manifest /reference/lemma-discovery.json --generation /reference/klean-generation --toolchain-lock /reference/klean-toolchain.lock.json --audit-input /audit-input.json --output /audit-output/evidence/05_mechanical_gate.json
```

Result: `05_mechanical_gate.json` (`status: PASS`, mode
`CLASSIFICATION_ONLY`, target `null`).
