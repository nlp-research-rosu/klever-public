# Audit command index

All commands were run against the read-only mounted inputs. Writable copies and
the `/proc` compatibility shim were confined to `/tmp/audit-work` and
`/audit-output/evidence`.

## Input and producer authentication

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; ...'
```

Results: `01-producer-and-mounted-tree-hashes.log`,
`02-pipeline-and-export-tree-hashes.log`,
`03-producer-authentication.log`, `21-stage1-source-hashes.log`,
`22-mounted-artifact-hash-reconciliation.log`,
`37-audit-input-envelope-verification.log`, and
`38-stage4-recorded-hash-reconciliation.log`.

## Canonical rule inventory

```sh
PYTHONPATH=/reference python3 -c \
  'from tools.k_rule_inventory import inventory_verification; ...'
```

Result: `04-rule-inventory-and-bijection.log`. Relevant frozen semantics and
proof ordering are in `05-relevant-frozen-semantics-excerpts.log`,
`33-stage1-proof-order-and-rule-use.log`, and
`35-domain-lemma-relevance-and-operational-semantics.log`.

## Deterministic Stage 4 preflight

The required call was:

```sh
PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.klean_preflight import check_generation;
   print(check_generation(
     Path("/reference/k-proof"),
     Path("/reference/lemma-discovery.json"),
     Path("/reference/klean-generation"),
     toolchain_lock=Path("/reference/klean-toolchain.lock.json")))'
```

The sandbox has a nested PID namespace but a host `/proc`, so Lean 4.22.0 could
not resolve its executable through `/proc/<pid>/exe`. The compatibility source
`proc-exe-shim.c` intercepts only that read-only lookup and supplies the pinned
toolchain executable path. Its compilation and toolchain-commit check are
recorded in `13-proc-shim-toolchain-validation.log`. The successful preflight,
with `LD_PRELOAD=/tmp/audit-work/proc-exe-shim.so`, is
`14-rerun-check-generation-with-proc-shim.log`; the preceding failed
environment-only attempts remain in `06-rerun-check-generation.log`,
`08-rerun-check-generation-pinned-toolchain.log`, and
`12-rerun-check-generation-success.log`.

## Fresh Stage 5 proof build

```sh
cp -a /candidate/. /tmp/audit-work/lean-audit.zDcMtK/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/lean-audit.zDcMtK/Base/
lake clean
lake build
```

The copied hashes and file set are in `18-fresh-proof-copy-corrected.log`.
Complete clean/build outputs are `19-proof-lake-clean.log` and
`20-proof-lake-build.log`.

## Target, axioms, and operational bridge

```sh
lake env lean /audit-output/evidence/PrintAxioms.lean
lake env lean /audit-output/evidence/PrintProofIdentity.lean
lake env lean /audit-output/evidence/OperationalBridgeTests.lean
lake env lean /audit-output/evidence/CounterfactualIdentityFailure.lean
```

Results are `27-print-axioms-Proof-final.log`,
`29-print-proof-identity.log`, `30-operational-bridge-tests.log`, and
`31-counterfactual-identity-failure.log`. The trusted mechanical Stage 5 gate
was also rerun; its returned evidence is
`34-trusted-stage5-mechanical-gate.log`.
