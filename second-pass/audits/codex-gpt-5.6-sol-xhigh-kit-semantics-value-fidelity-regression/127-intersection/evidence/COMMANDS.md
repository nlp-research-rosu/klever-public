# Reviewer command ledger

All commands were executed on 2026-07-23. K was v7.1.293 and Python was
3.10.12 (`toolchain.log`). Candidate build directories and caches were never
copied into the scratch tree.

| Stage | Working directory | Exact command | Exit | Output |
|---|---|---|---:|---|
| Provenance | `/audit-output` | `python3 /audit-output/evidence/provenance_check.py` | 0 | `provenance.log` |
| Trusted translation | `/tmp/audit-work/127-intersection` | `python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy; cmp -s regenerated-solution.mpy solution.mpy` | 0, 0 | `translation.log`, `regenerated-solution.mpy` |
| Python differential | `/tmp/audit-work/127-intersection` | `python3 /audit-output/evidence/differential_test.py` | 0 | `differential.log` |
| Concrete harness source | `/tmp/audit-work/127-intersection` | `python3 /audit-output/evidence/make_concrete_harness.py > concrete-harness.py` | 0 | `concrete-harness.py` |
| Concrete harness translation | `/tmp/audit-work/127-intersection` | `python3 trusted/py2mpy.py concrete-harness.py > concrete-harness.mpy` | 0 | `concrete-harness.mpy` |
| Fresh concrete build | `/tmp/audit-work/127-intersection` | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition fresh-runtime-kompiled` | 0 | `kompile-llvm.log` |
| Fresh concrete execution | `/tmp/audit-work/127-intersection` | `krun concrete-harness.mpy --definition fresh-runtime-kompiled` | 0 | `krun-concrete.log` |
| Fresh proof build | `/tmp/audit-work/127-intersection` | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled` | 0 | `kompile-haskell.log` |
| Loop claim | `/tmp/audit-work/127-intersection` | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.factorial-loop` | 0 (`#Top`) | `kprove-factorial-loop.log` |
| Complete target | `/tmp/audit-work/127-intersection` | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC` | 0 (`#Top`) | `kprove-all.log` |
| Body pinning | `/tmp/audit-work/127-intersection` | `python3 /audit-output/evidence/body_pinning.py` | 0 | `body-pinning.log` |
| Ground witnesses | `/tmp/audit-work/127-intersection` | `python3 /audit-output/evidence/adequacy_witness.py` | 0 | `adequacy-witness.log` |
| Rule inventory | `/tmp/audit-work/127-intersection` | `python3 /audit-output/evidence/rule_inventory.py > /audit-output/evidence/rule-inventory.tsv` | 0 | `rule-inventory.tsv` |
| Mutation build | `/tmp/audit-work/127-intersection` | `kprove reviewer-vacuity.k --definition fresh-verification-kompiled --spec-module REVIEWER-VACUITY --dry-run` | 0 | `vacuity-dry-run.log` |
| Mutation proof | `/tmp/audit-work/127-intersection` | `kprove reviewer-vacuity.k --definition fresh-verification-kompiled --spec-module REVIEWER-VACUITY` | 1 (expected stuck claim) | `vacuity-proof.log` |
| Untrusted-record summary | `/audit-output` | `python3 /audit-output/evidence/untrusted_claims_summary.py` | 0 | `untrusted-claims.log` |

The two successful proof commands have `COMMAND_EXIT_CODE="0"` in their raw
logs and print `#Top`. The mutation proof has `COMMAND_EXIT_CODE="1"`,
`WarnStuckClaimState`, and the residual `"YES"` value against the mutated
`"NO"` destination. The dry run establishes that the mutation parsed and
built before the deliberate proof failure.
