# Substantive audit commands

All mounted candidate and provenance content was treated as read-only evidence.
The only created files were audit evidence and fresh work below
`/tmp/audit-work`.

## Producer and mounted-tree provenance

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json

PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.pipeline_contract import sha256_tree
from tools.klean_export import tree_digest
# Compute launcher-contract and Klean-contract tree hashes for mounted inputs.
PY
```

## Trusted inventory reconstruction

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
inventory = inventory_verification(Path('/reference/k-proof'))
PY
```

The reconstruction was additionally checked by directly recomputing every
`sha256(" ".join(rule_text.split()))`, every `rule-<hash>` identity, and the
canonical JSON inventory hash.

## Required Stage 4 preflight

The first invocation exposed the audit container's broken numeric
`/proc/<getpid()>/exe` mapping:

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.klean_preflight import check_generation
check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
PY
```

After installing the narrow `/proc/self/exe` readlink shim documented in
`01-producer-and-environment.log`, the same checker was rerun unchanged:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc_self_readlink.so \
PYTHONPATH=/reference \
python3 - <<'PY'
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

## Fresh proof build

```sh
audit_lean_dir=$(mktemp -d /tmp/audit-work/lean-audit.XXXXXX)
cp -a /candidate/. "$audit_lean_dir/"
cp -a /reference/klean-generation/generated/. "$audit_lean_dir/Base/"

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc_self_readlink.so \
lake clean

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc_self_readlink.so \
lake build
```

The retained fresh workspace is
`/tmp/audit-work/lean-audit.wOaxmy`.

## Axiom, identity, and operational-bridge checks

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc_self_readlink.so \
lake env lean Axioms.lean

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc_self_readlink.so \
lake env lean Identity.lean

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc_self_readlink.so \
lake env lean BridgeAudit.lean

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc_self_readlink.so \
lake env lean BridgeMutationAudit.lean
```
