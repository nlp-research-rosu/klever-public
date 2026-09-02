# Command ledger

All paths below are the mounted read-only inputs or audit-owned paths. Complete
outputs are in the named adjacent `.log` files.

## Mode and mounted input

```bash
printf 'AUDIT_MODE=%s\n' "$AUDIT_MODE"
sha256sum /audit-input.json
python3 -m json.tool /audit-input.json
```

Results: `00-audit-mode-and-input.log`, `02-audit-input-full.log`.

## Producer provenance (run before accepting Stage 4)

```bash
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
rg -n 'generator|producer|exporter_sha|klean_py_sha|generation_producer' \
  /audit-input.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/generation-tools/source-manifest.json
```

Result: `06-producer-source-hashes.log`.

## Independent hashes and canonical inventory

```bash
PYTHONPATH=/reference \
  python3 /audit-output/evidence/audit_checks.py
```

The script invokes `tools.k_rule_inventory.inventory_verification`, independently
recomputes each normalized rule hash and ID, checks ordered identity against the
Stage 3 manifest, verifies the Stage 6 binding contract, and recomputes every
recorded tree/file hash plus all 794 Stage 1 per-file hashes.

Result: `07-independent-hash-and-inventory-checks.log`.

## Frozen source and semantics inspection

```bash
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/prove.sh
```

Results: `04-frozen-k-sources.log`, `08-relevant-operational-semantics.log`,
`09-more-operational-semantics.log`, `30-problem-prompt.log`.

## Mandatory preflight

Initial invocation (failed solely because Lean could not resolve
`/proc/<getpid>/exe` in the managed PID namespace):

```bash
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_preflight.py
```

Result: `10-rerun-klean-preflight.log`.

The narrow `/proc/*/exe` compatibility shim was built and tested with:

```bash
gcc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /audit-output/evidence/proc_exe_shim.so \
  /audit-output/evidence/proc_exe_shim.c -ldl
LD_PRELOAD=/audit-output/evidence/proc_exe_shim.so lean --version
LD_PRELOAD=/audit-output/evidence/proc_exe_shim.so lake --version
```

Result: `17-proc-exe-shim-build-and-test.log`.

Successful exact rerun:

```bash
LD_PRELOAD=/audit-output/evidence/proc_exe_shim.so \
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_preflight.py
```

Result: `18-rerun-klean-preflight-with-proc-shim.log`.

## Independent Stage 4 bijection and target checks

```bash
PYTHONPATH=/reference \
  python3 /audit-output/evidence/stage4_checks.py
```

Result: `19-independent-stage4-checks.log`.

## Fresh K build and proof sensitivity

Working directory: `/tmp/audit-work/fresh-k-001`.

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
bash /audit-output/evidence/check_ast_identity.sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.scan-loop
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Results: `21-fresh-k-kompile.log`, `22-fresh-expanded-ast-identity.log`,
`23-fresh-kprove-loop.log`, `24-fresh-kprove-full.log`.

The independently created source-body mutant was compiled and rejected with:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Results: `25-body-mutation-kompile.log`, `26-body-mutation-kprove.log`.

The independently created false postcondition was rejected with:

```bash
kprove spec-false-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-FALSE-AUDIT
```

Result: `27-false-postcondition-kprove.log`.

## Independent executable summary checks

```bash
python3 /audit-output/evidence/summary_oracle_check.py
```

Result: `31-summary-oracle-and-counterfactuals.log`.

## Stage 5 absence and generated target scan

```bash
find /reference/klean-generation/generated -type f -print | sort
find /reference/klean-generation/generated -type f -exec sha256sum {} + | sort -k2
rg -n 'targetStatement|sorry|admit|unsafe|^[[:space:]]*(axiom|opaque)[[:space:]]' \
  /reference/klean-generation/generated
test ! -e /candidate
```

Results: `28-generated-project-inspection.log`, `29-stage5-absence.log`.
