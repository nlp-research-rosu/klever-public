# Audit commands

All commands ran from `/audit-output`. Mounted inputs were read only.

## Mode and input inspection

```sh
printf 'AUDIT_MODE_ENV=%s\n' "$AUDIT_MODE"
sed -n '1,260p' /audit-input.json
find /candidate -maxdepth 2 -print
```

## Producer provenance

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json

PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.pipeline_contract import sha256_tree
print(sha256_tree(Path('/reference/generation-tools')))
PY
```

The complete results are in `01-producer-provenance.txt`.

## Canonical rule reconstruction

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(
    inventory_verification(Path('/reference/k-proof')),
    indent=2,
    sort_keys=True,
))
PY

PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.lemma_discovery_contract import validate_trust_boundary
print(json.dumps(validate_trust_boundary(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
), indent=2, sort_keys=True))
PY
```

The canonical output is in `02-rule-inventory.json`; independent span, hash,
order, classification, and source/semantics comparisons are in
`03-inventory-recomputation-and-classification.txt`.

## Stage 4 preflight

The initial exact invocation and failure are in
`04-preflight-initial-environment-failure.txt`. After applying the documented
PID-visibility shim only to the audit process environment, the exact rerun was:

```sh
LD_PRELOAD=/tmp/audit-work/getpid_host.so PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

The exact returned evidence is in `05-preflight-rerun.json`.

## Independent hashes, bijection, and target

The checks in `06-hash-bijection-and-target.json` are reproducible with:

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/hash_bijection_check.py
```

with `tools.pipeline_contract.sha256_tree`,
`tools.klean_export.tree_digest`,
`tools.stage6_resolution_contract.verify_audit_input`,
`tools.k_rule_inventory.inventory_verification`, and direct `hashlib.sha256`
file hashing. Every resolution hash and all 75 recorded Stage 1 per-file hashes
were recomputed. The generation-time `klean_export.py` was loaded directly
after its hash passed and its `_domain_source_rules`, `tree_digest`,
`expected_target_definition`, and `target_statement` functions were rerun.

The direct target/token scan was:

```sh
rg -n '^\s*def\s+targetStatement\b|\bsorry\b|\badmit\b|\bunsafe\b' \
  /reference/klean-generation/generated --glob '*.lean'
test -e /candidate
sha256sum \
  /reference/klean-generation/generated/Klean105ByLength/Lemmas.lean
```

Its exact result is in `07-generated-target-scan.txt`.
