# Audit command record

Each numbered `.typescript` file in this directory is the complete stdout/stderr captured with `script -qefc`. The principal commands were as follows. Read-only inspections (`sed`, `rg`, `find`, `sha256sum`, and JSON pretty-printing) account for the remaining numbered evidence files.

## Mode and hashes

```sh
env | rg '^AUDIT_MODE='
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py /reference/generation-tools/source-manifest.json
PYTHONPATH=/reference python3 /audit-output/evidence/scripts/check_recorded_hashes.py
PYTHONPATH=/reference python3 /audit-output/evidence/scripts/check_stage4_bijection.py
python3 /audit-output/evidence/scripts/candidate_static_audit.py
```

The outputs are in `00_inputs_and_mode.typescript`, `06_producer_authentication.typescript`, `08_producer_pipeline_tree_hash.typescript`, and `30` through `32`.

## Trusted inventory reconstruction

```sh
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

The exact reconstructed rules, source spans, normalized hashes, IDs, and whole inventory hash are in `05_reconstructed_inventory.typescript`. The independent ordered-bijection and classification comparison is in `10_inventory_bijection_and_classification_counts.typescript`.

## Required Stage 4 preflight

The sandbox exposes host PIDs in `/proc` while Lean 4.22 looks up `/proc/<getpid()>/exe`. The narrowly scoped compatibility source is `scripts/proc_pid_compat.c`; it was built and used only to make `getpid()` agree with `/proc/self`:

```sh
gcc -shared -fPIC -O2 -o /tmp/audit-work/proc_pid_compat.so /audit-output/evidence/scripts/proc_pid_compat.c
LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

The first unmodified-environment failure and the successful compatibility rerun are preserved in `11_preflight_rerun.typescript` and `15_preflight_rerun_with_pid_compat.typescript`.

## Fresh Stage 5 build

```sh
AUDIT_WORKSPACE=$(mktemp -d /tmp/audit-work/lean-audit.XXXXXX)
cp -a /candidate/. "$AUDIT_WORKSPACE/"
mkdir -p "$AUDIT_WORKSPACE/Base"
cp -a /reference/klean-generation/generated/. "$AUDIT_WORKSPACE/Base/"
cd "$AUDIT_WORKSPACE"
LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so lake clean
LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so lake build
```

The successful workspace was `/tmp/audit-work/lean-audit.EpMip4`. Complete clean/build output is in `18_fresh_candidate_lake_clean.typescript` and `19_fresh_candidate_lake_build.typescript`. `17_fresh_candidate_lake_clean.typescript` preserves an earlier copy-layout mistake; it was discarded before the correctly constructed fresh workspace above.

The following audit-only files were added to that fresh copy, never to `/candidate` or `/reference`: `AuditAxioms.lean` containing `import Proof` and `#print axioms Proof.final`; `AuditPrint.lean` containing `import Proof`, `#check Proof.final`, and `#print Proof.final`; and `AuditExamples.lean` containing the ground integer/Boolean evaluations and the constructor-free `SortStr` eliminator. They were run with:

```sh
LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so lake env lean AuditAxioms.lean
LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so lake env lean AuditPrint.lean
LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so lake env lean AuditExamples.lean
```

Exact output is in `22_print_axioms_proof_final.typescript`, `23_print_proof_final.typescript`, and `25_original_adversarial_examples.typescript`.

## Counterfactual proof checks

Two copies of the successful fresh workspace were patched only in `Proof.lean` while leaving `Proof.final` unchanged:

1. `operationalOrderGe` was replaced by `| _, _ => false`.
2. `operationalOrderablePair` was replaced by `false`.

For each copy the patch diff and this command were captured:

```sh
LD_PRELOAD=/tmp/audit-work/proc_pid_compat.so lake build
```

Both builds succeeded. See `24_counterfactual_orderge_constant_false.typescript` and `27_counterfactual_orderable_constant_false.typescript`. Ground witnesses are in `26_mutation_ground_witness.typescript` and `29_orderable_mutation_witness_success.typescript`; `28_orderable_mutation_witness.typescript` preserves and supersedes a typo in the first audit-only witness file.
