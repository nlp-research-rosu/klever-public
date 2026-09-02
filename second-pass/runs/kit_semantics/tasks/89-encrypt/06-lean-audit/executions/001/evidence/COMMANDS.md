# Audit commands

The numbered transcript files contain the corresponding raw stdout/stderr and
exit status. Exploratory read-only commands are not verdict-bearing; the
verdict-bearing commands are recorded here exactly.

## 01-producer-sha256.txt

```sh
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
```

## 02-producer-tree-sha256.txt

```sh
PYTHONPATH=/reference python -c 'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
```

## 03-reconstructed-rule-inventory.txt

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

## 04-independent-integrity-checks.txt

```sh
PYTHONPATH=/reference python /audit-output/evidence/independent_integrity_checks.py
```

The invoked script is preserved beside the transcript. It recomputes the
signed audit-input digest, producer file/tree hashes, the ordered rule
inventory and source spans, every frozen Stage 1 per-file hash, all selected
tree hashes, manifest bindings, the empty source-rule/obligation bijection,
and target/candidate absence.

## 05-klean-preflight-rerun.txt

This first required preflight attempt was preserved because it exposed the
sandbox `/proc` incompatibility described in `REVIEW.md`.

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

## 08-lean-sandbox-workaround.txt

```sh
gcc -shared -fPIC -O2 -Wall -Wextra -o /tmp/audit-work/libfix_lean_proc_exe.so /tmp/audit-work/fix_lean_proc_exe.c -ldl
sha256sum /tmp/audit-work/fix_lean_proc_exe.c /tmp/audit-work/libfix_lean_proc_exe.so
LD_PRELOAD=/tmp/audit-work/libfix_lean_proc_exe.so lean --version
LD_PRELOAD=/tmp/audit-work/libfix_lean_proc_exe.so lake --version
```

The shim source is `/tmp/audit-work/fix_lean_proc_exe.c`. It only corrects
Lean/Lake self-executable `readlink` calls in the PID-namespace sandbox.

## 06-klean-preflight-rerun-success.txt

```sh
LD_PRELOAD=/tmp/audit-work/libfix_lean_proc_exe.so PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

## 07-operational-semantics-excerpts.txt

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k | sed -n '8,31p;62,75p'
nl -ba /reference/k-proof/reference-semantics/semantics/str.k | sed -n '7,25p'
nl -ba /reference/k-proof/reference-semantics/semantics/int.k | sed -n '7,36p'
nl -ba /reference/k-proof/reference-semantics/semantics/builtins.k | sed -n '183,190p'
nl -ba /reference/k-proof/spec.k | sed -n '1,165p'
```

## 09-classification-boundary-checks.txt

```sh
python /audit-output/evidence/classification_boundary_checks.py
```

The invoked finite-check script is preserved beside the transcript. These
tests are adversarial support only; the universal classification judgment is
based on the frozen equations and operational rules.
