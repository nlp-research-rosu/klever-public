# Audit command index

All commands ran from `/tmp/audit-work/reconstruction` unless another working
directory is shown. The `.log` files are bounded `script(1)` transcripts whose
headers record the exact command and whose footers record the wrapper exit
status.

## Stage 1

- From `/audit-output`: `/audit-output/evidence/01_integrity_checks.sh`
  (`01_integrity_checks.log`, exit 0).

## Stage 2

- `python3 py2mpy.py solution.py > solution.regenerated.mpy; cmp -s
  solution.regenerated.mpy solution.mpy; sha256sum
  solution.regenerated.mpy solution.mpy` (`02_translation_identity.log`;
  `cmp` exit 0).
- From `/audit-output`: `python3 /audit-output/evidence/02_differential.py`
  (`02_differential.log`, exit 0, 215 cases, zero mismatches).

## Stage 3

- `kompile --version && kprove --version && krun --version`
  (`03_tool_versions.log`, exit 0; all version 7.1.293).
- `kompile reference-semantics/semantics.k --backend llvm --main-module
  MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled`
  (`03_build_runtime.log`, exit 0).
- `python3 py2mpy.py /audit-output/evidence/03_concrete_tests.py >
  tests/concrete-tests.mpy`
  (translator exit 0; the generated input is retained in scratch).
- `krun tests/concrete-tests.mpy --definition runtime-kompiled --output
  pretty` (`03_krun_concrete.log`, exit 0, final `<k> .K </k>` and
  `<exit-code> 0 </exit-code>`).
- `kompile verification.k --backend haskell --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled`
  (`03_build_verification.log`, exit 0).
- `kprove spec.k --definition verification-kompiled --spec-module SPEC
  --claims loop-correct` (`03_prove_loop_correct.log`, exit 0, `#Top`).
- `kprove spec.k --definition verification-kompiled --spec-module SPEC
  --claims loop-correct,f-symbolic --trusted loop-correct`
  (`03_prove_f_symbolic.log`, exit 0, `#Top`).
- `kprove spec.k --definition verification-kompiled --spec-module SPEC
  --claims f-zero` (`03_prove_f_zero.log`, exit 0, `#Top`).
- `kprove spec.k --definition verification-kompiled --spec-module SPEC
  --claims f-five` (`03_prove_f_five.log`, exit 0, `#Top`).

## Stage 4

- `python3 /audit-output/evidence/04_constructor_compare.py` was used in its
  four emission modes to create the extracted MPY terms; each extracted term
  and `solution.mpy` was parsed with `kast --definition runtime-kompiled
  --sort <Module|Stmt> --output kore`.
- `python3 /audit-output/evidence/04_constructor_compare.py report; cmp -s
  tests/solution.kore tests/spec-closure.kore; sha256sum
  tests/solution.kore tests/spec-closure.kore; cmp -s
  tests/solution-while.kore tests/spec-while.kore; sha256sum
  tests/solution-while.kore tests/spec-while.kore`
  (`04_constructor_compare.log`; both comparisons exit 0).
- `kprove spec-body-mutation.k --definition verification-kompiled
  --spec-module SPEC-BODY-MUTATION --dry-run`
  (`04_body_mutation_dry_run.log`, exit 0).
- `kprove spec-body-mutation.k --definition verification-kompiled
  --spec-module SPEC-BODY-MUTATION --claims body-mutant-one`
  (`04_body_mutation_proof.log`; internal `kprove` exit 1 as expected, with
  final heap `[2]` failing to unify with `[1]`).

## Stage 5

- From `/audit-output`: `python3
  /audit-output/evidence/05_inventory_k.py`
  (`05_rule_inventory.log`, exit 0; 1,107 declarations including 702 rules).
- `kompile verification.k --backend llvm --main-module VERIFICATION
  --syntax-module MPY-SYNTAX --output-definition
  verification-llvm-kompiled`
  (`05_build_verification_llvm_diagnostics.log`, exit 0; the compiler reports
  `outputOK` as non-exhaustive).
- `kprove spec-predicate-probes.k --definition verification-kompiled
  --spec-module SPEC-PREDICATE-PROBES --claims predicate-valid`
  (`05_predicate_valid.log`, exit 0, `#Top`).
- The same command with `--claims predicate-wrong-int` and
  `--claims predicate-wrong-type` is in `05_predicate_wrong_int.log` and
  `05_predicate_wrong_type.log`; both internal `kprove` processes exit 1 with
  the expected failed implication.

## Stage 6

- `kprove spec-vacuity.k --definition verification-kompiled --spec-module
  SPEC-VACUITY --dry-run` (`06_false_mutation_dry_run.log`, exit 0).
- `kprove spec-vacuity.k --definition verification-kompiled --spec-module
  SPEC-VACUITY --claims false-f-five`
  (`06_false_mutation_proof.log`; internal `kprove` exit 1 as expected, with
  the actual `[1,2,6,24,15]` heap failing to unify with the mutated
  `[1,2,6,24,16]` target).
