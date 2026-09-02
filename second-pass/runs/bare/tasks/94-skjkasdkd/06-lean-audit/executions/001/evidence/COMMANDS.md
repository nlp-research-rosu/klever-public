# Audit command index

All commands were run from `/audit-output`. Files numbered `01` through `16`
are raw `script(1)` transcripts; each ends with its actual command exit code.

## Producer provenance

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /audit-input.json
```

Result: `01-producer-sha256.txt`.

```sh
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.klean_export import tree_digest; print("generation_tools_tree_sha256=" + tree_digest(Path("/reference/generation-tools")))'
```

Result: `02-producer-tree-sha256.txt`. This is the Klean export tree algorithm,
included for contrast; the launcher records the pipeline artifact-tree digest.

```sh
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print("generation_producer_sources_sha256=" + sha256_tree(Path("/reference/generation-tools")))'
```

Result: `03-producer-pipeline-tree-sha256.txt`.

## Canonical inventory and frozen sources

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Result: `04-reconstructed-inventory.txt`.

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/semantic.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/prompt.py
nl -ba /reference/k-proof/prove.sh
```

Results: `05-verification-k.txt` through `08-source-and-prove.txt`.

The Stage 4 sidecars, root module, metadata, and generated file list are in
`09-stage4-manifests-and-root.txt` and `10-generated-file-list.txt`.

## Required preflight rerun

The first unmodified-environment invocation was:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Result: `11-rerun-check-generation.txt`. It failed at `lake clean` because the
audit sandbox's PID namespace is inconsistent with its `/proc` mount.
`12-rerun-check-generation-with-toolchain.txt` records the unsuccessful
`ELAN_HOME=/opt/elan` diagnostic rerun.

The narrowly scoped workaround source is `proc-self-readlink.c`. It was built
and the pinned toolchain was checked with:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc-self-readlink.so \
  /audit-output/evidence/proc-self-readlink.c
sha256sum \
  /audit-output/evidence/proc-self-readlink.c \
  /tmp/audit-work/proc-self-readlink.so
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake --version
```

Result: `16-proc-shim-build-and-toolchain.txt`.

The successful required rerun was:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/opt/runtimeverification-k/pyk/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
PYTHONPATH=/reference \
python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Result: `13-rerun-check-generation-success.txt`.

## Independent hash, inventory, bijection, and target check

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/verify_hashes_and_bijections.py
```

The final complete result is `15-complete-hashes-and-bijections.txt`; it ends
with `OVERALL: PASS`. `14-hashes-and-bijections.txt` is the earlier, narrower
version retained as raw audit history.
