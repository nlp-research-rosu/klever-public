# Audit commands

All mounted candidate/provenance content was treated as evidence only. The
only executed code from the mounted reference inputs was trusted tooling under
`/reference/tools`, as required by the audit protocol.

## Producer provenance

See `producer-provenance.out`. This was run before Stage 4 was judged.

## Inventory reconstruction

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/inventory_compare.py
```

Complete output is in `inventory_compare.out`.

## Semantic cross-check and counterfactual

```sh
python3 /audit-output/evidence/semantic_oracle.py
```

Complete output is in `semantic_oracle.out`.

## Launcher and Stage 4 structural bindings

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/stage4_structural_check.py
```

Complete output is in `stage4_structural_check.out`. The independent per-file
Stage 1 hash comparison is also recorded in `stage1-file-hashes.out`.

## Trusted generation preflight

The unmodified first invocation and its infrastructure failure are recorded in
`preflight-initial-failure.txt`.

The workaround was built and checked with:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean_app_path_shim.so \
  /tmp/audit-work/lean_app_path_shim.c -ldl
LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake --version
```

Output:

```text
Lean (version 4.22.0, x86_64-unknown-linux-gnu, commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05, Release)
Lake version 5.0.0-src+ba2cbbf (Lean version 4.22.0)
```

The successful required call was:

```sh
LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so \
PYTHONPATH=/reference \
python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result,indent=2,sort_keys=True))'
```

The exact returned evidence is in `preflight-rerun.json`.

## Target and Stage 5 absence

See `target-absence.out`. The launcher mode was `CLASSIFICATION_ONLY`, the
generated target was null, and `/candidate` was absent. Stage 5 proof commands
and axiom accounting were therefore inapplicable.
