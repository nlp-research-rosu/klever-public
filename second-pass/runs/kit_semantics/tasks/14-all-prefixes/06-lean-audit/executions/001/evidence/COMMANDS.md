# Audit command record

All provenance and candidate mounts were read-only. The only created files
were audit evidence under `/audit-output` and a Lean executable-path workaround
under `/tmp/audit-work`.

## Mode and mounted inputs

```bash
env | rg '^AUDIT_MODE='
find /reference/tools -maxdepth 3 -type f -printf '%p\n' | sort
find /reference -maxdepth 2 -mindepth 1 -printf '%y %p\n' | sort
find /candidate -maxdepth 3 -printf '%y %p\n'
```

Results: `00-audit-mode.txt` through `03-candidate-layout.txt`.

## Producer provenance

```bash
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py

rg -n \
  'generator_image|generation_producer|exporter_sha256|klean_py_sha256|klean_export|f884238|bbd11c|42a38e' \
  /audit-input.json \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json

PYTHONPATH=/reference python -c '
from pathlib import Path
from tools.pipeline_contract import sha256_tree
paths = [
    Path("/reference/generation-tools"),
    Path("/reference/k-proof"),
    Path("/reference/k-audit"),
    Path("/reference/klean-generation"),
    Path("/reference/klean-generation/generated"),
]
[print(f"{sha256_tree(path)}  {path}") for path in paths]
'
```

Results: `04-generation-producer-sha256.txt`,
`10-producer-provenance-crossrefs.txt`, and
`23-pipeline-tree-sha256.txt`.

The launcher-recorded mechanical-checker lock and every file named by it were
also hashed:

```bash
sha256sum /opt/humaneval/data/klean-audit-tools.lock.json
python -m json.tool /opt/humaneval/data/klean-audit-tools.lock.json
for file in /reference/tools/*.py; do sha256sum "$file"; done
```

Results: `157-mechanical-lock-sha256.txt`,
`158-mechanical-lock.json`, and `156-trusted-tool-sha256.txt`.

## Canonical K inventory

```bash
PYTHONPATH=/reference python -c '
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(
    inventory_verification(Path("/reference/k-proof")),
    indent=2,
    sort_keys=True,
))
'
```

Result: `18-reconstructed-rule-inventory.json`.

```bash
PYTHONPATH=/reference python -c '
import json
from pathlib import Path
from tools.lemma_discovery_contract import validate_trust_boundary
print(json.dumps(
    validate_trust_boundary(
        Path("/reference/k-proof"),
        Path("/reference/lemma-discovery.json"),
    ),
    indent=2,
    sort_keys=True,
))
'
```

Result: `32-stage3-trust-boundary-validation.json`.

```bash
PYTHONPATH=/reference python -c '
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
inventory = inventory_verification(Path("/reference/k-proof"))
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
canonical = [rule["source_rule_id"] for rule in inventory["rules"]]
observed = [rule["source_rule_id"] for rule in discovery["rules"]]
print("canonical_count", len(canonical))
print("manifest_count", len(observed))
print("order_exact", observed == canonical)
print("unique", len(observed) == len(set(observed)))
print("missing", [item for item in canonical if item not in observed])
print("extra", [item for item in observed if item not in canonical])
print(
    "inventory_hash_exact",
    discovery.get("inventory_sha256") == inventory["inventory_sha256"],
)
print("verification_sha256", inventory["verification_sha256"])
print("inventory_sha256", inventory["inventory_sha256"])
'
```

Result: `33-stage3-bijection-summary.txt`.

The exact frozen source and the fixed operational rules used for the semantic
classification were printed with `nl -ba` and `sed`:

```bash
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/reference-semantics/semantics/str.k | sed -n '1,32p'
nl -ba /reference/k-proof/reference-semantics/semantics/list.k | sed -n '1,70p'
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k | sed -n '1,190p'
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k | sed -n '1,150p'
```

Results: `25-verification-k-numbered.txt`,
`26-spec-k-numbered.txt`, `27-solution-py-numbered.txt`, and
`142-str-operational-rules.txt` through
`147-controls-for-loop-rules.txt`.

## Required Stage 4 preflight

The first invocation used the mounted Elan proxy:

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
print(json.dumps(result, indent=2, sort_keys=True))
'
```

It reached `lake clean` and failed with:

```text
tools.klean_preflight.KleanPreflightError:
lake clean failed (1): error: could not detect the configuration of the Lake installation
```

Read-only diagnostics established that Lean's `IO.appPath` could not resolve
`/proc/<pid>/exe` in the sandbox. The final workaround source is
`118-lean-app-path-shim-source-proc-pid.txt`; it intercepts only that lookup
for the pinned `lean`, `lake`, and `leanc` executables.

```bash
cc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/lean-app-path-shim.so \
  /tmp/audit-work/lean-app-path-shim.c \
  -ldl

LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so \
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/usr/bin:/bin \
lean --version

cd /reference/klean-generation/generated
LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so \
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/usr/bin:/bin \
lake env lean --version
```

Results: `119-compile-lean-app-path-shim-proc-pid.txt`,
`120-proc-pid-shimmed-lean-version.txt`, and
`121-proc-pid-shimmed-lake-env-lean-version.txt`.

The required trusted check was then rerun unchanged:

```bash
LD_PRELOAD=/tmp/audit-work/lean-app-path-shim.so \
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/opt/runtimeverification-k/pyk/.venv/bin:/usr/local/bin:/usr/bin:/bin \
PYTHONPATH=/reference \
python -c '
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
'
```

Result: `122-rerun-check-generation-shimmed.json`.

## Independent hash, bijection, and target audit

The complete independent checker source is
`148-independent-integrity-audit.py`.

```bash
PYTHONPATH=/reference \
python /audit-output/evidence/148-independent-integrity-audit.py
```

Final results: `159-independent-integrity-audit-final.json` and
`160-independent-integrity-audit-final-exit.txt`.

The checker performed 106 passing assertions, including:

- the signed launcher digest and audit mode;
- the mechanical-checker lock hash and every locked checker file;
- every signed mounted-tree and generated-tree digest;
- all 778 Stage 1 per-file hashes and their exact key set;
- the exact producer bundle contents, source hashes, and image ID;
- all six source spans, normalized hashes, and `source_rule_id` values;
- the whole inventory hash and ordered Stage 3 bijection;
- the independent six-`DEFINITION` classification;
- the empty domain/source-rule/obligation/trust-parameter sets;
- all Stage 4 manifest and sidecar hashes;
- absence of any generated target declaration;
- absence of Stage 5 inputs and `/candidate`; and
- exact equality of the fresh preflight result with the signed launcher record.
