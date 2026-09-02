# Reviewer command index

All commands were run from `/tmp/audit-work/fresh` unless a different working
directory is stated. The cited logs contain bounded output and explicit exit
statuses.

1. `python3 /audit-output/evidence/integrity_check.py`
   - Exit 0; `01b-integrity.log`.
2. `python3 /audit-output/evidence/constructor_compare.py`
   - Exit 0; `02c-constructor-compare.log`.
3. `python3 /audit-output/evidence/differential_test.py`
   - Exit 0; `03b-differential.log`.
4. `kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition semantic-llvm-kompiled -Wno unused-symbol -Wno unused-var`
   - Exit 0; `04-kompile-semantic-llvm.log`.
5. `bash /audit-output/evidence/run_concrete.sh`
   - Exit 0; `05-concrete-runs.log`.
6. `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-haskell-kompiled -Wno unused-symbol -Wno unused-var`
   - Exit 0; `06-kompile-verification.log`.
7. `kompile lemmas.k --backend haskell --main-module VERIFIED-LOOP-LEMMAS --syntax-module MPY-SYNTAX --output-definition lemmas-haskell-kompiled -Wno unused-symbol -Wno unused-var`
   - Exit 0; `07-kompile-lemmas.log`.
8. `bash /audit-output/evidence/run_all_claims.sh`
   - Exit 0; `08-all-claims-summary.log` and one complete log per claim.
   - The script runs each of the 15 claims separately with
     `kprove spec.k --definition <definition> --spec-module <module> --claims <module>.<label> --output pretty -Wno unused-symbol -Wno unused-var`.
9. The two `kprove` commands recorded verbatim in `11-bridge-connection.log`
   against `verification-haskell-kompiled`.
   - Both exit 1 with `WarnStuckClaimState`.
10. From `/tmp/audit-work/body-mutation`, the `kompile` and `kprove` commands
    recorded verbatim in `12-body-sensitivity.log`.
    - Build exit 0; proof exit 1 with the expected equality residual.
11. The `--dry-run` and ordinary `kprove` commands recorded verbatim in
    `13-non-vacuity.log`.
    - Dry run exit 0; deliberately false proof exit 1 with the concrete
      `pyInt(1)` versus `pyInt(2)` residual.
12. The `--dry-run` and ordinary `kprove` commands recorded verbatim in
    `14-main-no-bridge.log`.
    - Dry run exit 0; proof exit 1 at symbolic `execFor`.
13. `bash /audit-output/evidence/bridge_ground_compare.sh`
    - Exit 0; `15-bridge-ground-compare.log`.
14. The Python and `krun` whitespace probe recorded in
    `16-whitespace-model-probe.log`.
    - Exit 0; it exhibits the generated-semantics/Python mismatch outside the
      single-ASCII-space contract grammar.
