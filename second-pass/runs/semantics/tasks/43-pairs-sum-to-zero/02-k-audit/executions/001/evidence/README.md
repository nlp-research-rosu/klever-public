# Audit evidence index

All scripts are reviewer-authored. All K builds ran from
`/tmp/audit-work/pairs-audit`; `/candidate` was read-only.

- `toolchain.{sh,log}`: installed K commands and versions.
- `stage1_integrity.{sh,log}`: candidate/reference trees, missing provenance,
  comparisons, file types, and hashes.
- `differential.py`, `stage2_fidelity.{sh,log}`: trusted regeneration and 20,550
  source-level differential cases.
- `stage3_rebuild.sh`, `stage3_*.log`: fresh LLVM/Haskell builds, concrete run,
  and every positive claim.
- `stage4_ground-spec.k`, `stage4_ground_checks.{sh,log}`,
  `stage4_kprove_*.log`: fixed-semantics ground substitutions and Python
  comparisons.
- `rule_inventory.py`, `stage5_inventory.{sh,log}`, `rule_inventory.txt`: full
  declaration/rule inventory.
- `stage5_bridge_context.{py,mpy}`, `stage5_bridge-witness.k`,
  `stage5_bridge_checks.{sh,log}`, `stage5_context_*.log`,
  `stage5_*heap.log`: false-conclusion and continuation-sensitivity witnesses.
- `stage6_false-mutation.k`, `stage6_nonvacuity.{sh,log}`,
  `stage6_mutation_*.log`: fresh negated-result non-vacuity mutation.
