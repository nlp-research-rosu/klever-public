# Audit command index

All referenced `.log` files are raw `script(1)` transcripts. Logs from
interactive Lake progress retain their original control characters.

## Producer authentication and inventory

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json
```

Results: `01_producer_authentication.log`, `01b_producer_manifests.log`, and
`01c_producer_tree_hash.log`.

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
python3 /audit-output/evidence/compare_inventory.py
```

Results: `reconstructed-rule-inventory.json`,
`02_inventory_and_discovery.log`, and `03_classification_sources.log`.

## Deterministic Stage 4 preflight

The first unmodified attempt is in `05_check_generation.log` and failed only
because this sandbox's PID namespace ID is absent from its mounted `/proc`.
`05g_proc_self_shim.log` records the narrow self-executable lookup workaround
and the pinned Lean version it launches.

```sh
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
PYTHONPATH=/reference \
python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Successful returned evidence: `05i_check_generation_pass.log`.

```sh
python3 /audit-output/evidence/audit_hashes_and_stage4.py
```

Result: `07_stage4_independent_checks.log`.

## Source-only Stage 5 clean build

The exact fresh directory and complete command output are recorded with shell
tracing in `08c_candidate_source_only_clean_build.log`.

```sh
audit_project=$(mktemp -d /tmp/audit-work/proof-audit-source-only.XXXXXX)
cp -a /candidate/Proof.lean /candidate/lake-manifest.json \
  /candidate/lakefile.lean /candidate/lean-toolchain "$audit_project"
mkdir "$audit_project/Base"
cp -a /reference/klean-generation/generated/. "$audit_project/Base"
cd "$audit_project"
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH lake clean
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH lake build
```

## Axiom, static, and operational checks

```sh
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
  lake env lean AxiomAudit.lean
python3 /audit-output/evidence/audit_stage5_static.py
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
  lake env lean OperationalBridgeAudit.lean
```

Results: `09b_source_only_print_axioms.log`,
`11_stage5_static_and_identity.log`, and
`10b_operational_bridge_tests_pass.log`. The Lean audit sources are
`AxiomAudit.lean` and `OperationalBridgeAudit.lean`.

## Trusted Stage 5 mechanical gate

```sh
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
PYTHONPATH=/reference \
python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation --candidate /candidate
```

Result: `13_stage5_mechanical_gate.log`.
