# Reviewer command and status ledger

Unless an absolute path is shown, commands ran with working directory
`/tmp/audit-work/review-43` and the system K 7.1.293 tools in `/usr/bin`.
Bounded stdout/stderr is in the named evidence log.

| Purpose | Exact command | Tool status | Evidence |
|---|---|---:|---|
| Mounted-input integrity | `python3 /audit-output/evidence/01_integrity_check.py` | 0 | `01_integrity_check.log` |
| Structured-trace parsing | `python3 /audit-output/evidence/01_trace_summary.py` | 0 | `01_trace_summary.log` |
| Trusted regeneration | `python3 py2mpy.py solution.py > regenerated-solution.mpy` | 0 | `02_translation_identity.log` |
| Submitted/regenerated identity | `cmp solution.mpy regenerated-solution.mpy` | 0 | `02_translation_identity.log` |
| Independent Python differential | `python3 /audit-output/evidence/02_differential.py` | 0 | `02_differential.log` |
| Fresh concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition review-runtime-kompiled` | 0 | `03_kompile_llvm.log` |
| Translate concrete assertions | `python3 py2mpy.py /audit-output/evidence/03_concrete_tests.py > review-concrete-tests.mpy` | 0 | source and subsequent run preserved |
| Concrete K execution | `krun review-concrete-tests.mpy --definition review-runtime-kompiled` | 0 | `03_krun_concrete.log` |
| Fresh bridge-free definition | `kompile --backend haskell connection-definition.k --main-module CONNECTION-DEFINITION --syntax-module MPY-SYNTAX --output-definition review-connection-kompiled` | 0 | `03_kompile_connection.log` |
| Equality connection claim | `kprove connection-spec.k --definition review-connection-kompiled --spec-module CONNECTION-SPEC --claims CONNECTION-SPEC.int-equality` | 0, `#Top` | `03_kprove_connection_int_equality.log` |
| Unary-minus connection claim | `kprove connection-spec.k --definition review-connection-kompiled --spec-module CONNECTION-SPEC --claims CONNECTION-SPEC.int-unary-minus` | 0, `#Top` | `03_kprove_connection_int_unary_minus.log` |
| Fresh target definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition review-verification-kompiled` | 0 | `03_kompile_verification.log` |
| Auxiliary loop claim | `kprove spec.k --definition review-verification-kompiled --spec-module SPEC --claims SPEC.loop-invariant` | 0, `#Top` | `03_kprove_loop_invariant.log` |
| Entire submitted target spec | `kprove spec.k --definition review-verification-kompiled --spec-module SPEC` | 0, `#Top` | `03_kprove_all_target_claims.log` |
| Constructor-level body pinning | `bash /audit-output/evidence/04_constructor_pinning.sh` | 0; KORE `cmp` 0 | `04_constructor_pinning.log` |
| Concrete property substitutions | `kprove ground-substitution.k --definition review-verification-kompiled --spec-module GROUND-SUBSTITUTION` | 0, `#Top` | `04_ground_substitution.log` |
| Rule inventory generation | `python3 /audit-output/evidence/05_rule_inventory.py` | 0; 945 entries | `05_rule_inventory.log`, `05_rule_inventory.md` |
| False equality bridge interpretation | `kprove bridge-negative.k --definition review-connection-kompiled --spec-module BRIDGE-NEGATIVE --claims BRIDGE-NEGATIVE.wrong-int-equality` | 1, expected stuck value | `05_bridge_wrong_equality.log` |
| False unary-minus bridge interpretation | `kprove bridge-negative.k --definition review-connection-kompiled --spec-module BRIDGE-NEGATIVE --claims BRIDGE-NEGATIVE.wrong-int-unary-minus` | 1, expected stuck value | `05_bridge_wrong_unary_minus.log` |
| False-result mutation build | `kprove audit-false-result.k --definition review-verification-kompiled --spec-module AUDIT-FALSE-RESULT --dry-run` | 0 | `06_false_result_dry_run.log` |
| False-result mutation proof | `kprove audit-false-result.k --definition review-verification-kompiled --spec-module AUDIT-FALSE-RESULT` | 1, expected unmet implication | `06_false_result_proof.log` |

For the three expected-failure commands, a reviewer shell wrapper captured the
raw `kprove` status as `KPROVE_EXIT=1` and itself exited 0 only after checking
that the status was exactly 1. The logs preserve both the residual K
configuration and the captured raw status.
