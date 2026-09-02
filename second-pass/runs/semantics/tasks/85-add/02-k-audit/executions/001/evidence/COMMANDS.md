# Audit command index

All commands ran from `/audit-output` unless the entry says
`cwd=/tmp/audit-work/candidate-src`. Logs contain the bounded relevant output
and an `EXIT_STATUS` field. Expected negative tests are explicitly identified.

## Integrity and fidelity

1. `python3 /audit-output/evidence/01_integrity_check.py`
   — exit 0; `01_integrity.log`.
2. Source-only scratch setup:
   `mkdir -p /tmp/audit-work/candidate-src /tmp/audit-work/trusted`, followed by
   explicit `cp -a` of the candidate source/proof files and candidate
   `reference-semantics`, and explicit `cp -a` of the trusted prompt,
   canonical, translator, and trusted semantics tree
   — exit 0; `00_scratch_setup.log`.
3. `python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/candidate-src/solution.regenerated.mpy`
   — exit 0; then
   `cmp -s /tmp/audit-work/candidate-src/solution.regenerated.mpy /tmp/audit-work/candidate-src/solution.mpy`
   — exit 0; `02_translation_identity.log`.
4. `python3 /audit-output/evidence/02_differential.py --canonical /tmp/audit-work/trusted/canonical.py --candidate /tmp/audit-work/candidate-src/solution.py --inputs /audit-output/evidence/02_differential_inputs.json --preserve-cases /audit-output/evidence/02_all_cases.json`
   — exit 0; `02_differential.log`.
5. `command -v kompile; kompile --version; command -v kprove; kprove --version; command -v krun; python3 --version`
   — exit 0; `03_tool_versions.log`.

## Clean reconstruction

The following commands used `cwd=/tmp/audit-work/candidate-src`.

1. `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled`
   — exit 0; `03_kompile_llvm.log`.
2. `krun concrete-tests.mpy --definition runtime-kompiled --output pretty`
   — exit 0; `03_krun_concrete_tests.log`.
   A second independent route ran
   `python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate-src/concrete_tests.py > /tmp/audit-work/candidate-src/concrete-tests.regenerated.mpy`,
   `cmp -s /tmp/audit-work/candidate-src/concrete-tests.regenerated.mpy /tmp/audit-work/candidate-src/concrete-tests.mpy`,
   and
   `krun concrete-tests.regenerated.mpy --definition runtime-kompiled --output pretty`;
   all three exited 0; `03_krun_regenerated_concrete_tests.log`.
3. `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-kompiled`
   — exit 0; `03_kompile_haskell.log`.
4. `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant-bound --output pretty`
   — exit 0 and `#Top`; `03_kprove_loop.log`.
5. `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.add-correct --output pretty`
   — exit 0 and `#Top`; `03_kprove_entry.log`.

## Adequacy and ground witnesses

The following commands used `cwd=/tmp/audit-work/candidate-src`.

1. `kast solution.mpy --definition verification-kompiled --module VERIFICATION --sort Module --expand-macros --output kast --output-file /tmp/audit-work/candidate-src/solution.parsed.kast`
   — exit 0.
2. `kast --expression solutionModule --definition verification-kompiled --module VERIFICATION --sort Module --expand-macros --output kast --output-file /tmp/audit-work/candidate-src/solution-macro.kast`
   — exit 0.
3. `cmp -s /tmp/audit-work/candidate-src/solution.parsed.kast /tmp/audit-work/candidate-src/solution-macro.kast`
   — exit 0; all three results are in `04_program_pinning.log`.
4. `kprove ground-witness.k --definition verification-kompiled --spec-module GROUND-WITNESS --claims GROUND-WITNESS.entry-documented-example --output pretty`
   — exit 0 and `#Top`; `04_ground_entry.log`.
5. `kprove ground-witness.k --definition verification-kompiled --spec-module GROUND-WITNESS --claims GROUND-WITNESS.loop-satisfying-state --output pretty`
   — exit 0 and `#Top`; `04_ground_loop.log`.

## Static-soundness and sensitivity diagnostics

The following K commands used `cwd=/tmp/audit-work/candidate-src`.

1. `kompile verification-no-bridge.k --backend haskell --main-module VERIFICATION-NO-BRIDGE --syntax-module VERIFICATION-NO-BRIDGE --output-definition no-bridge-kompiled`
   — exit 0; `05_kompile_no_bridge.log`.
2. `kprove loop-only-no-bridge.k --definition no-bridge-kompiled --spec-module LOOP-ONLY-NO-BRIDGE --claims LOOP-ONLY-NO-BRIDGE.loop-invariant-without-operational-bridge --output pretty`
   — exit 0 and `#Top`; `05_kprove_loop_no_bridge.log`.
3. Three stronger diagnostic bridge claims were attempted and correctly
   remained unestablished:
   `kprove bridge-connection.k --definition no-bridge-kompiled --spec-module BRIDGE-CONNECTION --claims BRIDGE-CONNECTION.exact-loop-summary-with-continuation --output pretty`,
   `... --claims BRIDGE-CONNECTION.observable-call-effect ...`, and
   `... --claims BRIDGE-CONNECTION.loop-summary-preserving-empty-stmts ...`
   — each exit 1; respectively `05_kprove_bridge_connection.log`,
   `05_kprove_bridge_observable.log`, and `05_kprove_bridge_region.log`.
4. `kompile verification-body-mutant.k --backend haskell --main-module VERIFICATION-BODY-MUTANT --syntax-module VERIFICATION-BODY-MUTANT --output-definition body-mutant-kompiled`
   — exit 0; `05_kompile_body_mutant.log`.
5. `kprove body-sensitivity.k --definition body-mutant-kompiled --spec-module BODY-SENSITIVITY --claims BODY-SENSITIVITY.mutated-body-must-not-prove-original-summary --output pretty`
   — expected exit 1 with a result-condition residual;
   `05_kprove_body_mutant.log`.
6. `kprove bridge-domain-witness.k --definition verification-kompiled --spec-module BRIDGE-DOMAIN-WITNESS --claims BRIDGE-DOMAIN-WITNESS.overbroad-empty-stack-transition --output pretty`
   — exit 0 and `#Top`; `05_bridge_domain_extended.log`.
7. `kprove bridge-domain-witness-no-bridge.k --definition no-bridge-kompiled --spec-module BRIDGE-DOMAIN-WITNESS-NO-BRIDGE --claims BRIDGE-DOMAIN-WITNESS-NO-BRIDGE.fixed-semantics-rejects-transition --output pretty`
   — expected exit 1 with fixed execution stuck at `#pop`, changed locals,
   and `retV(2)`; `05_bridge_domain_fixed.log`.
8. `python3 /audit-output/evidence/05_inventory.py --root /tmp/audit-work/candidate-src/reference-semantics --verification /tmp/audit-work/candidate-src/verification.k > /audit-output/evidence/05_rule_inventory.md`
   — exit 0; `05_inventory.log`.

## Fresh non-vacuity mutation

The following commands used `cwd=/tmp/audit-work/candidate-src`.

1. `kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT --claims SPEC-VACUITY-AUDIT.add-false-off-by-one --dry-run --output none`
   — exit 0, establishing a valid build/parse; `06_vacuity_dry_run.log`.
2. `kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT --claims SPEC-VACUITY-AUDIT.add-false-off-by-one --output pretty`
   — expected exit 1 with the unmet equality
   `addAccSpec(INPUT,false,0) +Int 1 == addAccSpec(INPUT,false,0)`;
   `06_vacuity_proof.log`.
