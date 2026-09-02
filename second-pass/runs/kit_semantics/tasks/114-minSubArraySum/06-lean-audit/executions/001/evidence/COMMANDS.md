# Audit command index

The adjacent `.log` files contain the complete captured stdout/stderr and exit
status for these commands. `LD_PRELOAD` points only to the audit-owned shim
whose source and build hashes are recorded in `05a_lean_environment_shim.log`;
the untrusted candidate-provided binary was never loaded.

## Producer provenance

```bash
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
```

Result: the producer files, producer tree, source manifest, generator manifest,
immutable image digest, and `/audit-input.json` values all matched. See
`01_producer_provenance.log`.

## Rule inventory and mounted hashes

```bash
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; import json; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2))'
PYTHONPATH=/reference python3 /audit-output/evidence/06_stage4_independent_check.py
```

Results: `02_inventory_reconstruction.log`,
`03_recorded_hashes.log`, and `06_stage4_independent_check.log`.

## Required preflight

Initial ambient-toolchain attempt, retained because it failed before project
evaluation:

```bash
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.klean_preflight import check_generation; print(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")))'
```

Result: `05_preflight_rerun.log` records Lake's `/proc` installation-detection
failure.

Audit-owned environment repair and successful required rerun:

```bash
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/114-minSubArraySum/proc_exe_shim.so \
  /tmp/audit-work/114-minSubArraySum/proc_exe_shim.c -ldl
LD_PRELOAD=/tmp/audit-work/114-minSubArraySum/proc_exe_shim.so \
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; import json; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")), indent=2, sort_keys=True))'
```

Results: `05a_lean_environment_shim.log` and
`05b_preflight_rerun_with_shim.log`.

## Fresh proof copy and clean build

```bash
cp -a /candidate /tmp/audit-work/114-minSubArraySum/proof-audit
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/114-minSubArraySum/proof-audit/Base/
cd /tmp/audit-work/114-minSubArraySum/proof-audit
LD_PRELOAD=/tmp/audit-work/114-minSubArraySum/proc_exe_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/114-minSubArraySum/proc_exe_shim.so lake build
```

Results: `07_fresh_copy.log` and the complete terminal output in
`08_candidate_clean_build.log`.

## Target, axioms, and trusted final gate

`AuditAxioms.lean` contains exactly `import Proof` and
`#print axioms Proof.final`.

```bash
cd /tmp/audit-work/114-minSubArraySum/proof-audit
LD_PRELOAD=/tmp/audit-work/114-minSubArraySum/proc_exe_shim.so \
  lake env lean AuditAxioms.lean
python3 /audit-output/evidence/11_candidate_integrity.py
LD_PRELOAD=/tmp/audit-work/114-minSubArraySum/proc_exe_shim.so \
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; import json; from tools.klean_final_gate import check_final; print(json.dumps(check_final(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), Path("/candidate"), toolchain_lock=Path("/reference/klean-toolchain.lock.json"), audit_input=Path("/audit-input.json")), indent=2, sort_keys=True))'
```

Results: `09_print_axioms.log`, `10_mechanical_final_gate.log`, and
`11_candidate_integrity.log`.

## Operational bridge adversarial checks

```bash
cd /tmp/audit-work/114-minSubArraySum/proof-audit
LD_PRELOAD=/tmp/audit-work/114-minSubArraySum/proc_exe_shim.so \
  lake env lean AuditBridge.lean
```

The final corrected audit harness exits 0 in
`12c_bridge_adversarial_final.log`. The two preceding failed harness
iterations are preserved in `12a_...` and `12b_...`; they were failures in
the audit test proof scripts, not failures of the submitted proof.
