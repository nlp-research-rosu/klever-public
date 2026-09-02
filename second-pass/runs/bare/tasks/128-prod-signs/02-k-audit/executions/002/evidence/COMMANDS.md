# Exact audit commands and statuses

All build and execution commands ran from `/tmp/audit-work/fresh` unless a
different working directory is stated. `script -q -e -c ... LOG` preserved the
complete bounded output and its command exit code. ANSI reset sequences in K
logs are tool output.

1. `python3 /audit-output/evidence/provenance_check.py`
   - Exit 0. Log: `01-provenance.log`.
2. `python3 /tmp/audit-work/reference/py2mpy.py /tmp/audit-work/fresh/solution.py > /tmp/audit-work/fresh/regenerated-solution.mpy`
   - Exit 0; `cmp -s solution.mpy regenerated-solution.mpy` exit 0. Log:
     `02-translation.log`.
3. `python3 /audit-output/evidence/differential_test.py`
   - Exit 0. Log: `03-differential.log`.
4. `kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --backend llvm --output-definition semantics-kompiled`
   - Exit 0. Log: `04-kompile-semantics.log`.
5. For each of `input()`, `input(-1)`, `input(0)`, `input(1)`,
   `input(1,2,2,-4)`, `input(0,-7)`, `input(-1,-2)`, and
   `input(-1,-2,-3)`:
   `krun solution.mpy --definition semantics-kompiled -cARGS='INPUT' --output pretty`
   - Every invocation exit 0. Log: `05-krun-boundaries.log`.
6. `python3 /audit-output/evidence/k_semantics_diff.py`
   - Internally runs
     `krun solution.mpy --definition semantics-kompiled -cARGS='input(...)' --output json`
     on the 12 printed inputs and compares the decoded `<result>` with an
     independently imported trusted canonical implementation.
   - Exit 0. Log: `06-k-semantics-differential.log`.
7. `kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition verification-kompiled`
   - Exit 0. Log: `07-kompile-verification.log`.
8. `kprove spec.k --definition verification-kompiled --spec-module SPEC`
   - Exit 0, `#Top`. Log: `08-kprove-all.log`.
9. For each label `empty-contract`, `nonempty-initialization`,
   `negative-step`, `positive-step`, `zero-step`, `loop-exit`,
   `example-negative`, `example-zero`, and `example-three-negative`:
   `kprove spec-labeled.k --definition verification-kompiled --spec-module SPEC-LABELED --claims SPEC-LABELED.LABEL`
   - Every invocation exit 0 and printed `#Top`. Log:
     `09-kprove-individual.log`.
10. `python3 /audit-output/evidence/labeled_claim_equivalence.py`
    - Exit 0; after removing comments, labels, whitespace, and the audit module
      suffix, `spec-labeled.k` is identical to submitted `spec.k`. Log:
      `09a-labeled-claim-equivalence.log`.
11. `python3 /audit-output/evidence/program_term_compare.py`
    - Exit 0; parsed constructor ASTs identical. Log:
      `10-program-term-compare.log`.
12. In `/tmp/audit-work/body-mutation`:
    `kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition verification-kompiled`
    followed by
    `kprove spec.k --definition verification-kompiled --spec-module SPEC`
    - Build exit 0; proof exit 1 with `WarnStuckClaimState` in the mutated
      positive branch. Log: `11-body-sensitivity.log`.
13. `kprove spec-intended.k --definition verification-kompiled --spec-module SPEC-INTENDED --dry-run`
    followed by
    `kprove spec-intended.k --definition verification-kompiled --spec-module SPEC-INTENDED`
    - Dry-run exit 0; proof exit 1 with `WarnStuckClaimState`. Log:
      `12-missing-universal-target.log`.
14. `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run`
    followed by
    `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY`
    - Dry-run exit 0; proof exit 1, stuck at actual `result(-9)` versus mutated
      `result(-8)`. Log: `13-false-result-mutation.log`.
