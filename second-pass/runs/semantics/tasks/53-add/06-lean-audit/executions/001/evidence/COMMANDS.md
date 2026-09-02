# Audit command index

All paths below are immutable inputs except `/audit-output/evidence`.
The corresponding complete outputs are the numbered `.txt` files in this
directory.

## Launcher and input inventory

```sh
pwd
printf "AUDIT_MODE=%s\n" "$AUDIT_MODE"
sha256sum /audit-input.json
sed -n "1,260p" /audit-input.json
find /reference/tools -maxdepth 3 -type f -printf "%p\n" | sort
find /reference/k-proof /reference/k-audit /reference/klean-generation \
  /reference/generation-tools /candidate -maxdepth 3 -type f \
  -printf "%p\n" 2>/dev/null | sort
```

Result: `00_inputs_and_tools.txt`.

## Canonical Stage 1 rule reconstruction

```sh
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
sha256sum /reference/k-proof/verification.k \
  /reference/lemma-discovery.json
sed -n "1,320p" /reference/lemma-discovery.json
```

Result: `02_reconstructed_inventory_and_discovery.txt`.

```sh
PYTHONPATH=/reference \
  python /audit-output/evidence/verify_inventory_bijection.py
```

Script: `verify_inventory_bijection.py`.
Result: `24_inventory_bijection_verification.txt`.

## Frozen program and operational semantics

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/reference-semantics/semantics/core.k
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k
nl -ba /reference/k-proof/reference-semantics/semantics/call.k
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k
nl -ba /reference/k-proof/reference-semantics/semantics/int.k
```

Results: `03_frozen_sources_and_relevant_semantics_index.txt` and
`04_operational_semantics_sources.txt`.

```sh
python -c \
  'import ast,json; from pathlib import Path; src=Path("/reference/k-proof/solution.py").read_text(); mpy=" ".join(Path("/reference/k-proof/solution.mpy").read_text().split()); verification=" ".join(Path("/reference/k-proof/verification.k").read_text().split()); print(ast.dump(ast.parse(src),indent=2)); print(json.dumps({"normalized_solution_mpy":mpy,"solution_mpy_occurs_exactly_once_in_verification":verification.count(mpy)==1,"occurrence_count":verification.count(mpy)},indent=2))'
```

Result: `27_source_to_harness_identity.txt`.

## Producer provenance

The two producer files were hashed before Stage 4 was judged:

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
PYTHONPATH=/reference \
  python /audit-output/evidence/verify_producer_provenance.py
```

Script: `verify_producer_provenance.py`.
Results: `05_producer_provenance.txt`,
`07_producer_provenance_comparison.txt`, and
`26_producer_provenance_recheck.txt`.

## Fresh trusted Stage 4 preflight

The direct attempt was:

```sh
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result,indent=2,sort_keys=True))'
```

It reached `lake clean` and failed because Lean could not resolve
`/proc/<pid>/exe` in the audit sandbox. Result:
`08_fresh_klean_preflight.txt`.

The sandbox diagnosis and narrow compatibility shim are recorded in
`09_toolchain_diagnosis.txt` through
`19_lean_proc_shim_build_and_probe.txt`. The shim source is
`lean_proc_exe_shim.c`; it redirects only numeric `/proc/<pid>/exe`
`readlink` requests to `/proc/self/exe`.

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  /audit-output/evidence/lean_proc_exe_shim.c \
  -o /audit-output/evidence/lean_proc_exe_shim.so -ldl
LD_PRELOAD=/audit-output/evidence/lean_proc_exe_shim.so \
  PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result,indent=2,sort_keys=True))'
```

Complete returned evidence: `20_fresh_klean_preflight_with_pid_shim.txt`.

## Independent launcher hashes, obligation bijection, and fixed target

```sh
PYTHONPATH=/reference \
  python /audit-output/evidence/verify_hashes_and_bijection.py
```

Script: `verify_hashes_and_bijection.py`.
Result: `23_hashes_and_bijection_verification.txt`.

The raw obligation map, manifests, trust inventory, and generated target
module were displayed with:

```sh
sed -n "1,320p" \
  /reference/klean-generation/generated/obligation-map.json
sed -n "1,320p" /reference/klean-generation/export-result.json
sed -n "1,420p" /reference/klean-generation/preflight.json
sed -n "1,520p" /reference/klean-generation/trust-inventory.json
nl -ba /reference/klean-generation/generated/Klean53Add/Lemmas.lean
nl -ba /reference/klean-generation/generated/Klean53Add.lean
rg -n --no-heading "KleanGeneratedTarget|target|theorem|lemma|def" \
  /reference/klean-generation/generated --glob "*.lean"
```

Result: `21_obligation_target_and_trust_artifacts.txt`.
