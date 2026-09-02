# Audit command index

All paths below are the mounted audit paths. The corresponding raw results are
in the named files in this directory. Commands were run from `/audit-output`
unless a different working directory is noted.

## Input and producer provenance

Result: `00_inputs_and_mode.txt`

```bash
env | rg "^AUDIT_MODE="
sha256sum /audit-input.json
sed -n "1,260p" /audit-input.json
find /reference/tools -maxdepth 3 -type f -printf "%P\n" | sort
find /reference -maxdepth 2 -type f -printf "%p\n" | sort
find /candidate -maxdepth 3 -type f -printf "%p\n" 2>/dev/null | sort
```

Result: `01_generator_provenance.txt`

```bash
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json
sed -n "1,320p" /reference/generation-tools/source-manifest.json
sed -n "1,360p" /reference/klean-generation/generator-manifest.json
sed -n "1,320p" /reference/klean-generation/input-manifest.json
```

Result: `03_launcher_tree_hashes.txt`

```bash
PYTHONPATH=/reference python -c 'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print("producer_bundle_sha256", sha256_tree(Path("/reference/generation-tools"))); print("k_workspace_sha256", sha256_tree(Path("/reference/k-proof"))); print("generation_artifact_sha256", sha256_tree(Path("/reference/klean-generation")))'
```

## Inventory, source, and operational semantics

Result: `04_reconstructed_inventory.txt`

```bash
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Results: `05_frozen_program_spec_verification.txt`,
`07_operational_semantics_snippets.txt`, and `31_type_and_ast_semantics.txt`

```bash
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/prove.sh

nl -ba /reference/k-proof/reference-semantics/semantics.k
nl -ba /reference/k-proof/reference-semantics/semantics/list.k | sed -n "1,75p"
nl -ba /reference/k-proof/reference-semantics/semantics/methods.k | sed -n "1,75p"
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k | sed -n "1,125p"
nl -ba /reference/k-proof/reference-semantics/semantics/call.k | sed -n "1,112p"
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k | sed -n "60,105p"
nl -ba /reference/k-proof/reference-semantics/semantics/core.k | sed -n "120,225p"
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k | sed -n "1,130p"

nl -ba /reference/k-proof/reference-semantics/semantics/builtins.k | sed -n "285,300p"
rg -n "syntax .*::=.*For|syntax .*::=.*If|syntax .*::=.*Return|syntax .*::=.*ListExpr|strict" \
  /reference/k-proof/reference-semantics/semantics/syntax.k
```

Result: `28_independent_structural_hash_checks.txt`

```bash
PYTHONPATH=/reference python /audit-output/evidence/audit_checks.py
```

Result: `30_semantic_recurrence_adversarial_checks.txt`

```bash
python /audit-output/evidence/classification_semantic_check.py
```

## Generated project and deterministic preflight

Result: `08_generation_artifacts.txt`

```bash
sha256sum /reference/tools/klean_export.py \
  /reference/tools/klean.py \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
find /reference/klean-generation/generated -type f -printf "%P\n" | sort
sha256sum /reference/klean-generation/*.json \
  /reference/klean-generation/generated/obligation-map.json
sed -n "1,320p" /reference/klean-generation/export-result.json
sed -n "1,420p" /reference/klean-generation/trust-inventory.json
sed -n "1,360p" /reference/klean-generation/generated/obligation-map.json
find /reference/klean-generation/generated -name "*.lean" -type f \
  -print -exec sed -n "1,260p" {} \;
```

The first required preflight attempt exposed the audit sandbox's missing
`/proc/<pid>/exe` view. Result: `09_preflight_rerun.txt`.

```bash
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

The compatibility source is `proc_exe_compat.c` in `/tmp/audit-work`.
Compilation and a Lean version test are in
`26_proc_exe_compat_build_and_test.txt`.

```bash
gcc -shared -fPIC -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc_exe_compat.so \
  /tmp/audit-work/proc_exe_compat.c
env LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
env LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  /opt/elan/bin/lean --version
```

Successful required preflight result: `27_preflight_rerun_success.txt`.

```bash
env LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  PYTHONPATH=/reference \
  python -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Result of the trusted classification-only final mechanical gate:
`29_final_mechanical_gate.txt`.

```bash
env LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  PYTHONPATH=/reference \
  python -c 'import json; from pathlib import Path; from tools.klean_final_gate import check_final; result=check_final(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), None, toolchain_lock=Path("/reference/klean-toolchain.lock.json"), audit_input=Path("/audit-input.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```
