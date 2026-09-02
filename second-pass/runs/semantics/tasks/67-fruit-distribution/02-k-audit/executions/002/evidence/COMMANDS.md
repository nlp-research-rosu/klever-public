# Auditor command index

All commands ran from `/tmp/audit-work/reconstruction` unless another working
directory is stated. The linked logs contain shell tracing, exit statuses, and
bounded relevant output.

## Stage 1

- `python3 /audit-output/evidence/provenance_check.py`
  — working directory `/audit-output`; exit 0; see `provenance_check.log`.
- `python3 /audit-output/evidence/generation_record_summary.py`
  — working directory `/audit-output`; parsed all 157 JSONL events, exit 0; see
  `generation_record_summary.log`.
- The provenance script independently SHA-256-hashed all launcher-recorded
  file inputs, compared the campaign-lock JSON object, checked required mount
  types/symlinks, byte-compared prompt and translator, and recursively compared
  every candidate supplied-semantics entry with the trusted tree.

## Stage 2

- `python3 py2mpy.py solution.py > regenerated.mpy`
- `cmp -l regenerated.mpy solution.mpy`
  — exit 0; see `translator_regeneration.log`.
- `python3 /audit-output/evidence/differential_test.py`
  — exit 0; 462 cases recorded; see `differential_test.log`.

## Stage 3

- `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled`
  — exit 0; see `kompile_llvm.log`.
- `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled`
  — exit 0; see `kompile_haskell.log`.
- `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC`
  — `#Top`, exit 0; see `kprove_positive.log`.
- `diff -u solution.py <(sed -n '1,3p' k_concrete_tests.py)`
- `python3 py2mpy.py k_concrete_tests.py > k_concrete_tests.mpy`
- `krun k_concrete_tests.mpy --definition runtime-audit-kompiled --output pretty`
  — exit 0, `.K`, `NoExc`, exit-code cell 0; see `krun_concrete.log`.

## Stages 4–5

- `python3 /audit-output/evidence/program_pinning_check.py`
  — exact constructor identity modulo only optional `.Exprs` syntax, exit 0;
  see `program_pinning_check.log`.
- `kprove pinning-spec.k --definition verification-audit-kompiled --spec-module PINNING-SPEC`
  — `#Top`, exit 0; see `kprove_pinning.log`. A prior functional-sort form was
  rejected as unsupported by the backend before proof execution; it was
  replaced by an equivalent `<k>`-cell claim, and the diagnostic is preserved
  in `kprove_pinning_functional_failed.log`.
- `python3 /audit-output/evidence/rule_inventory.py`
  — exit 0; inventoried 1,105 source items including all 698 rules, 229 syntax
  declarations, five contexts, one configuration, and five claims; see
  `rule_inventory.md` and `rule_inventory.log`.
- `kompile audit-variants.k --backend haskell --main-module BRIDGE-FREE --syntax-module MPY-SYNTAX --output-definition bridge-free-kompiled`
- `kompile audit-variants.k --backend haskell --main-module OPPOSITE-INT --syntax-module MPY-SYNTAX --output-definition opposite-int-kompiled`
- `kompile audit-variants.k --backend haskell --main-module OPPOSITE-SPLIT --syntax-module MPY-SYNTAX --output-definition opposite-split-kompiled`
  — all exit 0; see `kompile_bridge_variants.log`.
- `kprove bridge-free-spec.k --definition bridge-free-kompiled --spec-module BRIDGE-FREE-SPEC`
  — expected exit 1 with `WarnStuckClaimState` at the unresolved synthetic
  `splitWS`/`applyBuiltin` obligations; see `kprove_bridge_free.log`.
- `kprove opposite-int-spec.k --definition opposite-int-kompiled --spec-module OPPOSITE-INT-SPEC`
- `kprove opposite-split-spec.k --definition opposite-split-kompiled --spec-module OPPOSITE-SPLIT-SPEC`
  — both `#Top`, both exit 0; see `kprove_opposite_interpretations.log`.
- `kompile body-mutated-verification.k --backend haskell --main-module BODY-MUTATED-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled`
  — exit 0.
- `kprove body-mutated-spec.k --definition body-mutated-kompiled --spec-module BODY-MUTATED-SPEC`
  — expected exit 1 at `N -Int A -Int A == N -Int A -Int B`; see
  `body_sensitivity.log`.

## Stage 6

- `kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY --dry-run`
  — exit 0 (successful parse/build).
- `kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY`
  — expected exit 1 with `WarnStuckClaimState` at
  `N-A-B == N-A-B+1`; see `nonvacuity.log`.
