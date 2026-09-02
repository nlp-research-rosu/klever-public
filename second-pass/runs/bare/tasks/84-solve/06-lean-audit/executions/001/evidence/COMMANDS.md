# Audit commands

The paired `.log` files contain complete combined stdout/stderr and the command
exit status. Python drivers are retained beside their logs.

## Producer provenance

Result: `producer-provenance.log`.

```bash
printf "%s\n" "AUDIT_MODE=${AUDIT_MODE-<unset>}"
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /audit-input.json
python -m json.tool /reference/generation-tools/source-manifest.json
python -m json.tool /reference/klean-generation/generator-manifest.json
```

## Tree hashes

Result: `tree-hashes.log`.

```bash
PYTHONPATH=/reference python -c '
from pathlib import Path
from tools import pipeline_contract, klean_export
print("pipeline generation-tools", pipeline_contract.sha256_tree(Path("/reference/generation-tools")))
print("pipeline k-proof", pipeline_contract.sha256_tree(Path("/reference/k-proof")))
print("pipeline k-audit", pipeline_contract.sha256_tree(Path("/reference/k-audit")))
print("pipeline klean-generation", pipeline_contract.sha256_tree(Path("/reference/klean-generation")))
print("klean stage1", klean_export.tree_digest(Path("/reference/k-proof")))
print("klean generated", klean_export.tree_digest(Path("/reference/klean-generation/generated")))
'
```

## Canonical inventory reconstruction

Driver: `reconstruct_inventory.py`. Result: `inventory-reconstruction.log`.

```bash
PYTHONPATH=/reference python /audit-output/evidence/reconstruct_inventory.py
```

## Frozen sources and relevant manifests

Result: `frozen-source-and-manifests.log`.

```bash
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/semantic.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
python -m json.tool /reference/lemma-discovery.json
python -m json.tool /reference/klean-generation/generated/obligation-map.json
```

## Fresh K operational witnesses

Result: `fresh-k-operational-witnesses.log`.

```bash
audit_sem_dir=$(mktemp -d /tmp/audit-work/semantics.XXXXXX)
cp /reference/k-proof/semantic.k \
  /reference/k-proof/verification.k \
  /reference/k-proof/solution.mpy \
  "$audit_sem_dir"
kompile --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  -o "$audit_sem_dir/semantic-kompiled" \
  "$audit_sem_dir/semantic.k"
kast "$audit_sem_dir/solution.mpy" \
  --definition "$audit_sem_dir/semantic-kompiled" \
  --module MPY-SYNTAX \
  --sort Pgm \
  --output json \
  --output-file "$audit_sem_dir/translated.json"
kast --expression solutionProgram \
  --definition "$audit_sem_dir/semantic-kompiled" \
  --module VERIFICATION \
  --sort Pgm \
  --expand-macros \
  --output json \
  --output-file "$audit_sem_dir/embedded.json"
cmp "$audit_sem_dir/translated.json" "$audit_sem_dir/embedded.json"
sha256sum "$audit_sem_dir/translated.json" "$audit_sem_dir/embedded.json"
for audit_n in 0 9 10 36 99 147 9999 10000; do
  krun "$audit_sem_dir/solution.mpy" \
    --definition "$audit_sem_dir/semantic-kompiled" \
    -cN="$audit_n"
done
```

## Stage 4 preflight

The initial exact call is in `stage4-preflight-rerun.log`; it failed at
`lake clean` because this PID namespace lacks `/proc/<getpid()>/exe`.
`lean-pid-namespace-workaround.log` records the condition and the narrow
`readlink` workaround built from `/tmp/audit-work/proc-self-exe-shim.c`.

The successful retry and returned JSON are in
`stage4-preflight-rerun-with-pid-shim.log`.

```bash
LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so \
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

## Independent Stage 4 cross-check

Driver: `independent_stage4_checks.py`. Result:
`independent-stage4-checks.log`.

```bash
PYTHONPATH=/reference \
python /audit-output/evidence/independent_stage4_checks.py
```

## Model-free final mechanical gate

Result: `mechanical-final-gate.log`. Machine-readable result:
`mechanical-final-gate.json`.

```bash
LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so \
PYTHONPATH=/reference \
python -m tools.klean_final_gate \
  --frozen-k /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --generation /reference/klean-generation \
  --toolchain-lock /reference/klean-toolchain.lock.json \
  --audit-input /audit-input.json \
  --output /audit-output/evidence/mechanical-final-gate.json
```
