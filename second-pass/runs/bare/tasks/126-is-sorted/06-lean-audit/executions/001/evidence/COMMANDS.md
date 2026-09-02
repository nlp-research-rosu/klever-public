# Audit command index

All commands were run from `/audit-output`. Full results are in the numbered
transcripts beside this file. Mounted files under `/reference` and `/candidate`
were never modified.

## Audit context

```bash
pwd
env | LC_ALL=C sort | rg '^(AUDIT_MODE|PYTHONPATH|PATH)='
sha256sum /audit-input.json
python -m json.tool /audit-input.json
```

Result: `evidence/00-audit-context.txt`.

## Producer provenance gate

```bash
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json
python -m json.tool /reference/klean-generation/generator-manifest.json
python -m json.tool /reference/generation-tools/source-manifest.json
```

The comparison also used the trusted
`tools.pipeline_contract.sha256_tree` with `PYTHONPATH=/reference` to recompute
the complete producer-bundle digest and compared the generator image ID with
the image-key component of the launcher-recorded bundle path.

Results: `evidence/01-producer-provenance.txt` and
`evidence/02-producer-provenance-comparison.txt`.

## Frozen Stage 1 inputs and inventory

```bash
PYTHONPATH=/reference python - <<'PY'
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(inventory_verification(Path("/reference/k-proof")))
PY
```

The actual recorded command additionally:

- recomputed both Stage 1 tree-digest formats;
- recursively recomputed every Stage 1 file hash;
- recomputed every normalized rule hash and `source_rule_id`;
- recomputed the canonical inventory hash;
- compared ordered IDs, uniqueness, counts, and sets with Stage 3; and
- ran `tools.lemma_discovery_contract.validate_trust_boundary`.

Results: `evidence/03-stage1-frozen-source.txt`,
`evidence/04-rule-inventory-and-bijection.txt`, and
`evidence/05-classification-trace.txt`.

## Required preflight

The required function invocation was:

```bash
PYTHONPATH=/reference python - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation

result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

The sandbox's PID namespace is not represented in its `/proc` mount. Lean
4.22 calls `readlink("/proc/<getpid>/exe", ...)`, so the first two runs failed
before inspecting the project. Those failures are preserved in
`evidence/06-preflight-check-generation.txt` and
`evidence/07-preflight-check-generation-pinned-path.txt`.

The narrowly scoped compatibility shim is
`evidence/proc-self-readlink-shim.c`. It maps only
`/proc/<digits>/exe` to the equivalent `/proc/self/exe` lookup:

```bash
gcc -shared -fPIC -Wall -Wextra -Werror -O2 \
  -o /tmp/audit-work/proc-self-readlink-shim.so \
  /audit-output/evidence/proc-self-readlink-shim.c -ldl

LD_PRELOAD=/tmp/audit-work/proc-self-readlink-shim.so \
  PYTHONPATH=/reference python - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation

result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Results: `evidence/08-lean-sandbox-shim-diagnostic.txt` and
`evidence/09-preflight-check-generation-success.txt`.

## Independent Stage 4 checks

The checks in `evidence/11-independent-stage4-checks.txt` used only trusted
hashing, inventory, audit-envelope, and target-parsing functions from
`/reference/tools`. They independently recomputed:

- the signed launcher-envelope digest;
- Stage 1, Stage 2, Stage 3, Stage 4, generated-project, producer-bundle,
  obligation-map, and trust-inventory hashes;
- all cross-manifest hash bindings;
- the empty source-rule/obligation/trust-parameter bijection;
- the expected and observed target;
- the toolchain-lock identity;
- absence of links or special files; and
- absence of a Stage 5 candidate and all Stage 5 launcher fields.

Raw generated files and JSON sidecars are in
`evidence/10-stage4-artifacts.txt`.
