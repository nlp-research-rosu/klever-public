# Audit commands

Commands below were run in the listed working directories. Their complete
outputs are the numbered evidence files.

## Audit binding and canonical inventory

Working directory: `/audit-output`

```bash
AUDIT_MODE
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Outputs: `00-audit-mode-and-binding.txt`,
`01-reconstructed-inventory.json`, and
`02-inventory-manifest-comparison.json`.

The comparison recomputed the canonical ordered IDs and compared them with
every Stage 3 entry, including counts, duplicates, missing/extra IDs, order,
inventory hash, and manifest file hash.

## Frozen K proof and lemma-relevance mutations

The original and each mutation were copied below
`/tmp/audit-work/k-lemma-relevance` or `/tmp/audit-work/k-original`.
Only the copied `verification.k` files were edited.

```bash
kompile verification.k \
  --backend haskell \
  --main-module PILE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module PILE-PREFIX-SPEC

kprove spec.k \
  --definition verification-kompiled \
  --spec-module PILE-LOOP-SPEC
```

Outputs:

- Original: `31-original-kompile.log`,
  `32-original-prefix-kprove.log`, `33-original-loop-kprove.log`.
- Right-identity rule removed:
  `27-right-identity-removed-kompile.log`,
  `28-right-identity-removed-kprove.log`.
- Associativity rule removed:
  `29-associativity-removed-kompile.log`,
  `30-associativity-removed-kprove.log`.

## Producer-source attestation and recorded hashes

Working directory: `/audit-output`

```bash
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
```

Python checks used:

```python
from tools.pipeline_contract import sha256_tree
from tools.klean_export import tree_digest
```

to apply the launcher's artifact-tree digest to mounted artifacts and the
export-tree digest to frozen/generated projects. Outputs:
`09-generation-producer-raw.txt`,
`12-generation-producer-final-attestation.json`,
`25-recorded-hash-verification.json`, and
`26-obligation-target-bijection.json`.

## Independent deterministic-generation preflight

Working directory: `/audit-output`

```bash
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
PYTHONPATH=/reference \
python - <<'PY'
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

Output: `44-independent-stage4-preflight-success.json`.

The preload library was compiled with:

```bash
cc -shared -fPIC \
  /tmp/audit-work/lean_proc_self_shim.c \
  -ldl \
  -o /tmp/audit-work/lean_proc_self_shim.so
```

Its exact source is `lean_proc_self_shim.c`. It rewrites only Lean's
current-process `/proc/<pid>/exe` lookup to `/proc/self/exe`, which is required
because the audit container's proc mount and process namespace are mismatched.

## Fresh Stage 5 copy, build, theorem, and axioms

Fresh project: `/tmp/audit-work/stage5-fresh-audit-2`

```bash
mkdir -p /tmp/audit-work/stage5-fresh-audit-2
cp -a /candidate/. /tmp/audit-work/stage5-fresh-audit-2/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/stage5-fresh-audit-2/Base/

LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so lake build
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  lake env lean AxiomAudit.lean
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  lake env lean TheoremAudit.lean
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
  lake env lean CounterfactualAudit.lean
```

Outputs: `37-fresh-stage5-final-prebuild-hashes.json`,
`45-stage5-lake-clean-final.log`, `46-stage5-lake-build-final.log`,
`47-stage5-build-final-exit-codes.txt`,
`48-print-axioms-proof-final.log`,
`49-print-proof-final-and-target.log`,
`51-candidate-integrity-scan.json`,
`52-postbuild-target-identity.json`, and
`57-operational-bridge-and-nonvacuity-success.log`.

The three exact Lean audit sources are `AxiomAudit.lean`,
`TheoremAudit.lean`, and `CounterfactualAudit.lean`.

## Trusted final mechanical gate

Working directory: `/audit-output`

```bash
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so \
PYTHONPATH=/reference \
python - <<'PY'
import json
from pathlib import Path
from tools.klean_final_gate import check_final
result = check_final(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    Path('/candidate'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
    audit_input=Path('/audit-input.json'),
)
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
PY
```

Output: `59-trusted-final-mechanical-gate.json`.
