# Audit command index

All commands were run from `/audit-output` unless a different working
directory is stated. The files named after each command contain its captured
stdout/stderr or structured result.

## Mode, producer provenance, and canonical inventory

```sh
printenv AUDIT_MODE
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
```

Results:

- `audit-mode.log`
- `producer-file-hashes.log`
- `producer-pipeline-tree-hash.log`
- `inventory-reconstruction.json`
- `discovery-structural-validation.json`

## Stage 4 preflight and independent manifest checks

The audit sandbox exposes a PID namespace but a host `/proc`, causing the
unmodified Lean runtime to fail `IO.appPath`. The source and compiled shim are
`/tmp/audit-work/lean-proc-self-shim.c` and
`/tmp/audit-work/lean-proc-self-shim.so`. It changes only reads of
`/proc/<pid>/exe` to `/proc/self/exe`.

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean-proc-self-shim.so \
  /tmp/audit-work/lean-proc-self-shim.c -ldl
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
AUDIT_MODE=CLASSIFICATION_AND_PROOF PYTHONPATH=/reference \
  python3 /audit-output/evidence/independent_manifest_check.py
```

Results:

- `preflight-rerun.json`
- `independent-manifest-check.json`
- `fresh-target-identity.json`
- `core-file-hashes.log`

## Fresh proof build

Fresh project preparation:

```sh
mkdir /tmp/audit-work/131-digits-proof-audit
cp -a /candidate/. /tmp/audit-work/131-digits-proof-audit/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/131-digits-proof-audit/Base/
```

From `/tmp/audit-work/131-digits-proof-audit`:

```sh
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so lake clean
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so lake build
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  lake env lean AuditAxioms.lean
```

Results:

- `fresh-project-layout.log`
- `lake-clean-passing.log` (empty stdout/stderr, exit 0)
- `lake-build.log`
- `print-axioms.log`
- `proof-and-target-file-hashes.log`

The trusted independent proof gate was also rerun:

```sh
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_final_gate import check_proof_candidate; result=check_proof_candidate(Path("/reference/klean-generation"), Path("/candidate")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Result: `final-mechanical-gate.json`.

## Candidate trust and operational-bridge checks

```sh
rg -n '\b(sorry|admit|unsafe|axiom|opaque)\b' /candidate \
  --glob '*.lean' --glob 'lakefile.lean'
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_export import lean_trust_declarations; print(json.dumps(lean_trust_declarations(Path("/candidate/Proof.lean")), indent=2, sort_keys=True))'
```

Results:

- `candidate-forbidden-token-scan.log`
- `candidate-trust-declarations.json`

From `/tmp/audit-work/131-digits-proof-audit`:

```sh
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  lake env lean AuditBridge.lean
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  lake env lean AuditDifferential.lean
```

Results:

- `operational-bridge-lean.log`
- `operational-differential-lean.log`

## Direct supplied-K-semantics checks

```sh
kompile /reference/k-proof/reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/runtime-kompiled
krun /tmp/audit-work/k-adversarial.mpy \
  --definition /tmp/audit-work/runtime-kompiled --output none
krun /tmp/audit-work/k-false-assert.mpy \
  --definition /tmp/audit-work/runtime-kompiled --output none
```

Results:

- `k-kompile-llvm.log`
- `k-adversarial-krun.log` (exit 0)
- `k-false-assert-krun.log` (expected exit 1)
