# Material audit commands

All paths are the mounted audit paths. Full results are in the named evidence
files.

## Producer and input hashes

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
```

Result: `01_producer_hashes_and_manifests.txt`.

Tree and source hashes were recomputed with the same trusted digest functions
used by the immutable contracts:

```sh
PYTHONPATH=/reference python3
```

The script invoked `tools.pipeline_contract.sha256_tree`,
`tools.klean_export.tree_digest`, and direct SHA-256 for regular files, then
compared their results with `/audit-input.json`. Result:
`05_independent_recorded_hash_checks.txt`.

## Canonical Stage 1 inventory

```sh
PYTHONPATH=/reference python3
```

The script called:

```python
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
inventory_verification(Path("/reference/k-proof"))
```

Result: `06_reconstructed_inventory.json`; command log:
`06_reconstructed_inventory_command.txt`. The independent ordered bijection
and contract validation are in `08_discovery_bijection_pass.txt`.

## Required Stage 4 preflight

The first literal invocation exposed the audit sandbox's blocked numeric
`/proc/<pid>/exe` lookup:

```sh
PYTHONPATH=/reference python3
```

```python
from pathlib import Path
from tools.klean_preflight import check_generation
check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

Result: `12_check_generation_command.txt` (environmental Lake failure).

The minimal `/proc/self/exe` compatibility shim is recorded in
`35_lean_sandbox_shim_build_and_test.txt`. With that shim:

```sh
LD_PRELOAD=/tmp/audit-work/libprocself_readlink.so \
PYTHONPATH=/reference \
python3
```

The same `check_generation(...)` call returned `PASS`. Returned evidence:
`36_check_generation_returned.json`; command log:
`36_check_generation_command.txt`.

Independent obligation and target comparisons are in
`42_independent_stage4_bijection_and_target.txt` and
`43_corrected_stage4_source_record_comparison.txt`.

## Fresh Stage 5 build

```sh
cp -a /candidate/. /tmp/audit-work/stage5-project/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/stage5-project/Base/
```

Copy record: `44_fresh_stage5_copy.txt`.

Working directory: `/tmp/audit-work/stage5-project`.

```sh
LD_PRELOAD=/tmp/audit-work/libprocself_readlink.so lake clean
LD_PRELOAD=/tmp/audit-work/libprocself_readlink.so lake build
```

Complete outputs: `45_stage5_lake_clean.txt` and
`46_stage5_lake_build.txt`.

## Proof and bridge checks

```sh
LD_PRELOAD=/tmp/audit-work/libprocself_readlink.so \
  lake env lean AuditAxioms.lean
```

Exact output: `58_print_axioms_exact_output.txt`; command/exit record:
`58_print_axioms_command.txt`.

```sh
LD_PRELOAD=/tmp/audit-work/libprocself_readlink.so \
  lake env lean AuditIdentity.lean
LD_PRELOAD=/tmp/audit-work/libprocself_readlink.so \
  lake env lean AuditBridge.lean
LD_PRELOAD=/tmp/audit-work/libprocself_readlink.so \
  lake env lean Counterfactual.lean
```

Results: `51_proof_identity_and_adversarial_values.txt`,
`56_universal_operational_bridge_checks.txt`, and
`55_counterfactual_convenient_bridge_pass.txt`.

The exact theorem-header comparison and complete axiom reconciliation are in
`57_proof_statement_and_axiom_reconciliation.txt`.
