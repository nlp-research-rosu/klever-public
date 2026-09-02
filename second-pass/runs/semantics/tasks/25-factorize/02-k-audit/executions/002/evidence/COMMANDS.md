# Audit command record

Every command below was run in the stated working directory. The corresponding
`*.log` file is a bounded transcript produced with `script -q -e -c`; its final
footer records `COMMAND_EXIT_CODE`.

## Stage 1: provenance

Working directory: `/audit-output`

```sh
python3 /audit-output/evidence/provenance_check.py
# exit 0; provenance_check.log

python3 /audit-output/evidence/generation_trace_summary.py
# exit 0; generation_trace_summary.log

python3 /audit-output/evidence/generation_output_summary.py
# exit 0; generation_output_summary.log

bash /audit-output/evidence/prepare_scratch.sh
# exit 0; prepare_scratch.log
```

## Stage 2: translation and differential execution

Working directory: `/tmp/audit-work/25-factorize`

```sh
python3 py2mpy.py solution.py > solution.mpy && cmp -s solution.mpy solution.mpy.submitted && sha256sum solution.py solution.mpy solution.mpy.submitted && echo regenerated_solution_mpy_byte_identical=true
# exit 0; translation_identity.log

python3 /audit-output/evidence/differential_factorize.py
# first run exit 1 because the audit harness called canonical.py on a negative
# integer and encountered ValueError; differential_factorize.log

python3 /audit-output/evidence/differential_factorize.py
# corrected run exit 0; differential_factorize_rerun.log
```

The first differential run is retained. The corrected script compares the
intended positive domain and separately reports nonpositive outcomes.

## Stage 3: toolchain and clean reconstruction

Working directory: `/tmp/audit-work/25-factorize`

```sh
command -v kup; command -v kompile; command -v krun; command -v kprove; kompile --version; krun --version; kprove --version
# exit 0; toolchain.log

cp /audit-output/evidence/concrete_audit.py ./concrete_audit.py && diff -u solution.py <(sed -n "1,13p" concrete_audit.py) && python3 py2mpy.py concrete_audit.py > concrete_audit.mpy && sha256sum concrete_audit.py concrete_audit.mpy && echo concrete_harness_prefix_matches_solution=true
# exit 2 under script's /bin/sh because process substitution is a bash feature;
# concrete_harness_prepare.log

cp /audit-output/evidence/concrete_audit.py ./concrete_audit.py && sed -n "1,13p" concrete_audit.py > concrete_audit.prefix.py && cmp -s solution.py concrete_audit.prefix.py && python3 py2mpy.py concrete_audit.py > concrete_audit.mpy && sha256sum concrete_audit.py concrete_audit.mpy && echo concrete_harness_prefix_matches_solution=true
# exit 0; concrete_harness_prepare_rerun.log

kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
# exit 0; kompile_llvm.log

krun solution.mpy --definition audit-runtime-kompiled --output pretty
# exit 0; krun_solution_module.log

krun concrete_audit.mpy --definition audit-runtime-kompiled --output none
# exit 0; krun_concrete_audit.log

kompile verification.k --backend haskell --main-module FACTORIZE-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled
# exit 0; kompile_base_proof.log

kprove spec.k --definition audit-verification-kompiled --spec-module FACTORIZE-LOOP-SPEC --output pretty
# exit 0, output #Top; kprove_loop.log

kompile verification.k --backend haskell --main-module FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA --syntax-module MPY-SYNTAX --output-definition audit-verification-with-lemma-kompiled
# exit 0; kompile_lemma_proof.log

kprove spec.k --definition audit-verification-with-lemma-kompiled --spec-module FACTORIZE-SPEC --output pretty
# exit 0, output #Top; kprove_entry.log
```

## Stages 4 and 5: pinning and extension checks

Working directory: `/tmp/audit-work/25-factorize`

```sh
kast --definition audit-verification-kompiled --module FACTORIZE-VERIFICATION --sort Stmt --expand-macros --output kore --expression factorizeDef --output-file factorize_macro.kore && kast --definition audit-verification-kompiled --module FACTORIZE-VERIFICATION --sort Stmt --expand-macros --output kore /audit-output/evidence/actual_factorize_term.mpy --output-file factorize_actual.kore && cmp -s factorize_macro.kore factorize_actual.kore && sha256sum factorize_macro.kore factorize_actual.kore && echo factorize_macro_equals_translated_constructor=true
# exit 0; program_term_comparison.log

sed -n "9,34p" spec.k > loop_claim_body.txt && sed -n "68,93p" verification.k > loop_rule_body.txt && cmp -s loop_claim_body.txt loop_rule_body.txt && sha256sum loop_claim_body.txt loop_rule_body.txt && echo promoted_rule_body_equals_proved_claim_body=true
# exit 0; loop_claim_rule_identity.log

cp /audit-output/evidence/spec_concrete_substitutions.k ./spec_concrete_substitutions.k && kprove spec_concrete_substitutions.k --definition audit-verification-with-lemma-kompiled --spec-module AUDIT-CONCRETE-SUBSTITUTIONS --output pretty
# exit 0, output #Top; kprove_concrete_substitutions.log

python3 /audit-output/evidence/concrete_substitution_compare.py
# exit 0; concrete_substitution_compare.log

cp /audit-output/evidence/spec_bridge_continuation.k ./spec_bridge_continuation.k
kprove spec_bridge_continuation.k --definition audit-verification-kompiled --spec-module AUDIT-BRIDGE-CONTINUATION --output pretty
# exit 0, output #Top; kprove_bridge_continuation_base.log

kprove spec_bridge_continuation.k --definition audit-verification-with-lemma-kompiled --spec-module AUDIT-BRIDGE-CONTINUATION --output pretty
# exit 0, output #Top; kprove_bridge_continuation_lemma.log

python3 /audit-output/evidence/k_rule_inventory.py
# exit 0; k_rule_inventory.log
```

Body-sensitivity working directory:
`/tmp/audit-work/25-factorize/body-mutation`

```sh
kompile verification.k --backend haskell --main-module FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA --syntax-module MPY-SYNTAX --output-definition body-mutation-kompiled
# exit 0; kompile_body_mutation.log

kprove spec.k --definition body-mutation-kompiled --spec-module FACTORIZE-SPEC --output pretty
# expected exit 1 with WarnStuckClaimState on
# factorLoop(N,2,.ValSeq) = factorLoop(N,3,.ValSeq);
# kprove_body_mutation.log
```

The body mutation itself is preserved as `verification_body_mutation.k`; it
changes the executable `factorizeBody` divisor initialization from 2 to 3.

## Stage 6: fresh result mutation

Working directory: `/tmp/audit-work/25-factorize`

```sh
cp /audit-output/evidence/spec-vacuity.k ./spec-vacuity.k

kprove spec-vacuity.k --definition audit-verification-with-lemma-kompiled --spec-module SPEC-VACUITY --dry-run --output none
# exit 0; spec_vacuity_build.log

kprove spec-vacuity.k --definition audit-verification-with-lemma-kompiled --spec-module SPEC-VACUITY --output pretty
# expected exit 1 with WarnStuckClaimState on
# factorLoop(N+1,2,.ValSeq) = factorLoop(N,2,.ValSeq);
# kprove_vacuity.log
```
