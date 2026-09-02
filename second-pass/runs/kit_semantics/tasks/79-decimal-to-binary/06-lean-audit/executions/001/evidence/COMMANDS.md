# Audit command index

All mounted candidate and provenance inputs were read-only. The commands below
either read those mounts or wrote only beneath `/audit-output` and
`/tmp/audit-work`.

## Producer integrity

Results: `producer-integrity-contract.log` (the earlier
`producer-integrity.log` also records a diagnostic hash made with a different,
non-contract tree framing algorithm).

```bash
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
PYTHONPATH=/reference python -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
```

## Canonical inventory reconstruction

Result: `inventory-reconstruction.log`.

```bash
PYTHONPATH=/reference python -c '
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
i = inventory_verification(Path("/reference/k-proof"))
m = json.loads(Path("/reference/lemma-discovery.json").read_text())
ids = [r["source_rule_id"] for r in i["rules"]]
mids = [r["source_rule_id"] for r in m["rules"]]
print(json.dumps({
  "reconstructed": i,
  "manifest_inventory_sha256": m.get("inventory_sha256"),
  "exact_order_match": mids == ids,
  "inventory_ids_unique": len(ids) == len(set(ids)),
  "manifest_ids_unique": len(mids) == len(set(mids)),
  "missing_from_manifest": [x for x in ids if x not in mids],
  "extra_in_manifest": [x for x in mids if x not in ids],
}, indent=2, sort_keys=True))'
```

The frozen program, claim, verification rules, and load-bearing supplied
semantics excerpts used for reclassification are in `semantic-source.log`.

## Required deterministic-generation check

The first exact call, in `check-generation.log`, failed before project
elaboration because Lean/Lake could not resolve their executable path in this
audit runtime:

```bash
PYTHONPATH=/reference python -c '
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
  Path("/reference/k-proof"),
  Path("/reference/lemma-discovery.json"),
  Path("/reference/klean-generation"),
  toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))'
```

`lean-toolchain-recovery.log` records the failure, the narrow executable-path
shim's hashes, and confirmation of Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. The shim source is
`lean_app_path_shim.c`; it changes only `readlink`/`readlinkat` answers for the
current process's `/proc/.../exe` link. It was compiled with:

```bash
cc -shared -fPIC -O2 \
  -o /tmp/audit-work/lean_app_path_shim.so \
  /audit-output/evidence/lean_app_path_shim.c
```

The successful rerun used the same trusted function and inputs, plus the
pinned direct toolchain path and the runtime shim. Returned evidence is in
`check-generation-rerun.log`.

```bash
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so \
PYTHONPATH=/reference python -c '
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
  Path("/reference/k-proof"),
  Path("/reference/lemma-discovery.json"),
  Path("/reference/klean-generation"),
  toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))'
```

## Independent hash and bijection checks

`hash-reconciliation.log` records validation of the signed audit envelope,
both Stage 1 tree-digest conventions, the Stage 2/3/4 and producer trees, the
generated tree, audit-mode agreement, all 788 Stage 1 file hashes, target
identity, and candidate absence.

`manifest-bijection.log` records every cross-manifest hash comparison, the
independently empty domain set, empty source-rule and obligation lists, unique
obligation IDs, empty trust parameters, target absence, and candidate absence.

`generated-target-inspection.log` contains the raw obligation map, empty
generated Lemmas namespace, generator manifest, input manifest, export result,
and a search for any theorem/lemma/example or generated-target declaration.
