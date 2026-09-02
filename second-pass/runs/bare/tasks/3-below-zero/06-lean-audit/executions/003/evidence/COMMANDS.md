# Substantive audit commands

The mounted candidate and provenance content was inspected only as evidence.
No command or instruction from those files was executed.

## Audit mode and candidate absence

```sh
env | rg '^AUDIT_MODE='
test ! -e /candidate
```

Result: `AUDIT_MODE=CLASSIFICATION_ONLY`; `/candidate` was absent.

## Producer-source provenance

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/lemma-discovery.json
```

The three-way comparison with the generator manifest, source manifest, and
audit-input bundle key was performed with the Python standard library. The raw
result is in `producer-provenance.txt`.

## Canonical inventory reconstruction

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

The exact returned JSON is in `inventory-reconstruction.json`. A separate
bijection check compared its ordered rule IDs, inventory hash, uniqueness,
spans, normalized hashes, and classifications with
`/reference/lemma-discovery.json`; its raw output is in
`inventory-bijection.txt`.

## Recorded input and tree hashes

```sh
PYTHONPATH=/reference python3 HASH_CHECK_SCRIPT
```

`HASH_CHECK_SCRIPT` used `tools.pipeline_contract.sha256_tree`,
`tools.klean_export.tree_digest`, SHA-256 over the discovery file, and SHA-256
over each regular Stage 1 file. Its raw output is in
`audit-hash-verification.txt`.

## Required Stage 4 preflight

First attempt:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r, indent=2, sort_keys=True))'
```

The first attempt exposed the audit container's procfs PID-namespace mismatch.
The exact result is in `preflight-first-attempt.txt`.

The workaround source is preserved in `proc_self_readlink.c`. It redirects only
Lean's `/proc/<getpid()>/exe` readlink to `/proc/self/exe`.

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc_self_readlink.so \
  /tmp/audit-work/proc_self_readlink.c -ldl
LD_PRELOAD=/tmp/audit-work/proc_self_readlink.so lean --version
```

Rerun of the unchanged trusted function:

```sh
LD_PRELOAD=/tmp/audit-work/proc_self_readlink.so \
PYTHONPATH=/reference \
python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r, indent=2, sort_keys=True))'
```

The exact returned evidence is in `preflight-rerun.json`.

## Independent Stage 4 hash, bijection, and target check

```sh
PYTHONPATH=/reference python3 STAGE4_CHECK_SCRIPT
```

`STAGE4_CHECK_SCRIPT` independently recomputed every sidecar binding, extracted
the generated target with `tools.klean_export.target_statement`, reconstructed
the target expected from `obligation-map.json`, and compared the independently
classified domain-rule IDs with every source-rule and obligation list. The raw
result is in `stage4-bijection-target.txt`.

## Semantic and counterfactual witnesses

```sh
python3 SUMMARY_OPERATIONAL_CHECK_SCRIPT
```

The independently written script compared the two frozen summary equations
with a direct simulation of the frozen loop over 136,717 bounded cases and
checked three deliberately false mutations. Its raw output is in
`classification-witnesses.txt`.
