# Exact command/status index

Relevant output is in the referenced bounded log.

| Stage | Exact command | Exit | Log |
|---|---|---:|---|
| 1 | `python3 /audit-output/evidence/provenance_check.py` | 0 | `01-provenance.log` |
| 2 | `python3 /tmp/audit-work/reconstruction/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/regenerated-solution.mpy` | 0 | `02-program-fidelity.log` |
| 2 | `cmp /tmp/audit-work/reconstruction/regenerated-solution.mpy /tmp/audit-work/reconstruction/solution.mpy` | 0 | `02-program-fidelity.log` |
| 2 | `python3 /audit-output/evidence/differential.py` | 0 | `02-program-fidelity.log` |
| 3 | `python3 py2mpy.py auditor-concrete-tests.py > auditor-concrete-tests.mpy` | 0 | `03-positive-reconstruction.log` |
| 3 | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | 0 | `03b-kompile-llvm.log` |
| 3 | `krun auditor-concrete-tests.mpy --definition runtime-kompiled` | 0 | `03c-krun-concrete.log` |
| 3 | `kompile verification.k --backend haskell --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-base-kompiled` | 0 | `03d-kompile-base.log` |
| 3 | `kprove spec.k --definition verification-base-kompiled --spec-module AUX-SPEC` | 0, `#Top` | `03e-kprove-aux.log` |
| 3 | `kompile verification.k --backend haskell --main-module MPY-VERIFICATION-LEMMA --syntax-module MPY-SYNTAX --output-definition verification-lemma-kompiled` | 0 | `03f-kompile-lemma.log` |
| 3 | `kprove spec.k --definition verification-lemma-kompiled --spec-module MAIN-SPEC` | 0, `#Top` | `03g-kprove-main.log` |
| 4 | `kast solution.mpy --definition verification-base-kompiled --module BELOW-ZERO-COMMON --sort Module --expand-macros --output kore > parsed-submitted-program.kore` | 0 | `04a-kast-submitted.log` |
| 4 | `kast claimed-program.mpy --definition verification-base-kompiled --module BELOW-ZERO-COMMON --sort Module --expand-macros --output kore > parsed-claimed-program.kore` | 0 | `04b-kast-claimed.log` |
| 4 | `cmp parsed-submitted-program.kore parsed-claimed-program.kore` | 0 | `04c-program-term-cmp.log` |
| 4 | `python3 /audit-output/evidence/claim_witnesses.py` | 0 | `04d-claim-witnesses.log` |
| 5 | `python3 /audit-output/evidence/k_inventory.py` | 0 | `05-inventory-summary.log` |
| 6 | `kprove spec-audit-mutation.k --definition verification-lemma-kompiled --spec-module AUDIT-MUTATION --dry-run` | 0 | `06a-mutation-dry-run.log` |
| 6 | `kprove spec-audit-mutation.k --definition verification-lemma-kompiled --spec-module AUDIT-MUTATION` | 1, expected stuck result | `06b-mutation-proof.log` |
| 4/5 | `kompile verification-body-mutant.k --backend haskell --main-module MPY-BODY-MUTANT-BASE --syntax-module MPY-SYNTAX --output-definition body-mutant-base-kompiled` | 0 | `07a-kompile-body-mutant-base.log` |
| 4/5 | `kprove spec-body-mutant.k --definition body-mutant-base-kompiled --spec-module AUX-BODY-MUTANT` | 1, expected body-sensitive residual | `07b-kprove-body-mutant-aux.log` |
| 4/5 | `kompile verification-body-mutant.k --backend haskell --main-module MPY-BODY-MUTANT-LEMMA --syntax-module MPY-SYNTAX --output-definition body-mutant-lemma-kompiled` | 0 | `07c-kompile-body-mutant-lemma.log` |
| 4/5 | `kprove spec-body-mutant.k --definition body-mutant-lemma-kompiled --spec-module MAIN-BODY-MUTANT` | 0, `#Top` | `07d-kprove-body-mutant-main.log` |
