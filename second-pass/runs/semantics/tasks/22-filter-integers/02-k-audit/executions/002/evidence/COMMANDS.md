# Reviewer command ledger

All execution/build commands ran against copied source under
`/tmp/audit-work/22-filter-integers`. Candidate-provided compiled definitions
were not present or used.

| Stage | Exact command | Exit | Bounded log/result |
|---|---|---:|---|
| 1 | `python3 /audit-output/evidence/stage1_integrity.py` | 0 | `stage1-integrity.log`: required regular files, 367 valid trace records, all recorded regular-file hashes and manifest-tree hashes matched; recursive semantics comparison identical. |
| 2 | `python3 /tmp/audit-work/22-filter-integers/py2mpy.py /tmp/audit-work/22-filter-integers/solution.py > /tmp/audit-work/22-filter-integers/regenerated-solution.mpy` | 0 | `stage2-fidelity.log` |
| 2 | `cmp /tmp/audit-work/22-filter-integers/regenerated-solution.mpy /tmp/audit-work/22-filter-integers/solution.mpy` | 0 | Both SHA-256 `caa0e9fffddb1e422387467f4480c6bdfb3bb7ce7d5ed0394eb61b8a51a0e0f9`. |
| 2 | `python3 /audit-output/evidence/differential.py` | 0 | `stage2-fidelity.log`: 16,116 cases, 0 mismatches. |
| 3 | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled` | 0 | `stage3-kompile-llvm.log` |
| 3 | `krun concrete_tests.mpy --definition reviewer-runtime-kompiled` | 0 | `stage3-krun-candidate-tests.log`: `.K`, `NoExc`, exit cell 0. |
| 3 | `kompile verification.k --backend haskell --main-module FILTER-VERIFICATION --syntax-module MPY-SYNTAX --output-definition reviewer-verification-kompiled` | 0 | `stage3-kompile-haskell.log` |
| 3 | `/audit-output/evidence/stage3_proofs.sh` | 0 | `stage3-kprove.log`; the script records each exact command below and the combined command. |
| 3 | `kprove spec.k --definition reviewer-verification-kompiled --spec-module FILTER-SPEC --claims FILTER-SPEC.empty` | 0 | `#Top` |
| 3 | `kprove spec.k --definition reviewer-verification-kompiled --spec-module FILTER-SPEC --claims FILTER-SPEC.prompt-example-one` | 0 | `#Top` |
| 3 | `kprove spec.k --definition reviewer-verification-kompiled --spec-module FILTER-SPEC --claims FILTER-SPEC.prompt-example-two` | 0 | `#Top` |
| 3 | `kprove spec.k --definition reviewer-verification-kompiled --spec-module FILTER-SPEC --claims FILTER-SPEC.order-and-scalars` | 0 | `#Top` |
| 3 | `kprove spec.k --definition reviewer-verification-kompiled --spec-module FILTER-SPEC` | 0 | `#Top` |
| 4 | `kast solution.mpy --definition reviewer-verification-kompiled --module FILTER-VERIFICATION --sort Module --expand-macros --output json --output-file solution-expanded.json` | 0 | `stage4-program-pinning.log` |
| 4 | `kast --expression FILTER-PROGRAM --definition reviewer-verification-kompiled --module FILTER-VERIFICATION --sort Module --expand-macros --output json --output-file macro-expanded.json` | 0 | `stage4-program-pinning.log` |
| 4 | `cmp solution-expanded.json macro-expanded.json` | 0 | Both 7,243 bytes and SHA-256 `542fc8227368544d17538fbb13ad417fae99ff10ed73360e3f33eb16a628d211`. |
| 4 | `python3 py2mpy.py /audit-output/evidence/stage4_k_witnesses.py > stage4-k-witnesses.mpy` | 0 | Ground witnesses for all four claim shapes. |
| 4 | `krun stage4-k-witnesses.mpy --definition reviewer-runtime-kompiled` | 0 | `stage4-ground-witnesses.log` |
| 4 | `python3 /audit-output/evidence/stage4_python_witnesses.py` | 0 | Expected one K/Python mismatch: Bool witness. |
| 4 | `kompile verification.k --backend haskell --main-module FILTER-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutant-kompiled` (in `body-mutant/`) | 0 | `stage4-body-mutant-build.log` |
| 4 | `kprove spec.k --definition body-mutant-kompiled --spec-module FILTER-SPEC --claims FILTER-SPEC.prompt-example-one` | 1 (expected) | `stage4-body-mutant-proof.log`: `WarnStuckClaimState`, result heap empty. |
| 5 | `python3 /audit-output/evidence/build_rule_inventory.py > /audit-output/evidence/rule-inventory.tsv` | 0 | 1,107 inventoried K sentences. |
| 5 | `python3 /audit-output/evidence/review_rule_inventory.py > /audit-output/evidence/rule-inventory-reviewed.tsv` | 0 | A target-specific disposition for every sentence. |
| 6 | `kprove spec-vacuity.k --definition reviewer-verification-kompiled --spec-module FILTER-SPEC-VACUITY --dry-run` | 0 | `stage6-vacuity-dry-run.log`: emitted valid `kore-exec` proof command. |
| 6 | `kprove spec-vacuity.k --definition reviewer-verification-kompiled --spec-module FILTER-SPEC-VACUITY` | 1 (expected) | `stage6-vacuity-proof.log`: `WarnStuckClaimState`; actual heap `list(.ValSeq)` did not match false `[0]`. |

Toolchain: `kompile`, `krun`, and `kprove` all reported K v7.1.293
(`toolchain.log`).
