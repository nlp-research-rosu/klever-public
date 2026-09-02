# Reviewer command ledger

All paths below are container paths. `script -q -e -c ... LOG` records bounded
stdout/stderr and embeds `COMMAND_EXIT_CODE` in each listed log.

| Purpose | Working directory | Exact command | Exit | Evidence |
|---|---|---|---:|---|
| Integrity/provenance | `/audit-output` | `python3 /audit-output/evidence/integrity_check.py` | 0 | `integrity.log` |
| Structured generation record | `/audit-output` | `python3 /audit-output/evidence/generation_record_summary.py` | 0 | `generation-record-summary.log` |
| Trusted translation | `/tmp/audit-work/33-sort-third` | `python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy` | 0 | `translator.log` |
| Translation byte identity | `/tmp/audit-work/33-sort-third` | `cmp --verbose regenerated-solution.mpy solution.mpy` | 0 | `translation-compare.log` |
| Translation hashes | `/tmp/audit-work/33-sort-third` | `sha256sum regenerated-solution.mpy solution.mpy solution.py` | 0 | `translation-hashes.log` |
| Python differential | `/audit-output` | `python3 /audit-output/evidence/differential_test.py` | 0 | `differential.log`, `differential_inputs.jsonl` |
| K versions | `/tmp/audit-work/33-sort-third` | `kompile --version` | 0 | `kompile-version.log` |
| K prover version | `/tmp/audit-work/33-sort-third` | `kprove --version` | 0 | `kprove-version.log` |
| Reviewer concrete translation | `/tmp/audit-work/33-sort-third` | `python3 /reference/py2mpy.py audit_concrete_tests.py > audit-concrete-tests.mpy` | 0 | `concrete-translation.log` |
| Fresh concrete definition | `/tmp/audit-work/33-sort-third` | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | 0 | `kompile-concrete.log` |
| Concrete K execution | `/tmp/audit-work/33-sort-third` | `krun audit-concrete-tests.mpy --definition audit-runtime-kompiled` | 0 | `krun-concrete.log` |
| Fresh proof definition | `/tmp/audit-work/33-sort-third` | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | 0 | `kompile-proof.log` |
| Loop claim alone | `/tmp/audit-work/33-sort-third` | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.sort-third-loop` | 0 (`#Top`) | `kprove-loop.log` |
| End claim with helper filtered out (diagnostic) | `/tmp/audit-work/33-sort-third` | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.sort-third-correct` | 1 (expected loop-head residual) | `kprove-correct.log` |
| Submitted positive proof command | `/tmp/audit-work/33-sort-third` | `kprove spec.k --definition audit-verification-kompiled --spec-module SPEC` | 0 (`#Top`) | `kprove-all.log` |
| Constructor pinning | `/tmp/audit-work/33-sort-third` | `kprove pinning-spec.k --definition audit-verification-kompiled --spec-module PINNING-SPEC` | 0 (`#Top`) | `kprove-pinning.log`, `pinning-spec.k` |
| Ground summary substitution | `/tmp/audit-work/33-sort-third` | `kprove ground-summary-spec.k --definition audit-verification-kompiled --spec-module GROUND-SUMMARY-SPEC` | 0 (`#Top`) | `kprove-ground-summary.log` |
| Body-mutation definition | `/tmp/audit-work/33-sort-third/body-mutation` | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled` | 0 | `kompile-body-mutation.log`, `verification-body-mutated.k` |
| Body-sensitivity proof | `/tmp/audit-work/33-sort-third/body-mutation` | `kprove spec.k --definition body-mutated-kompiled --spec-module SPEC` | 1 (expected result mismatch) | `kprove-body-mutation.log` |
| Fresh false-postcondition proof | `/tmp/audit-work/33-sort-third` | `kprove spec-vacuity.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY` | 1 (expected unmet obligation) | `kprove-vacuity.log`, `spec-vacuity.k` |
| False-mutation witness | `/audit-output` | `python3 /audit-output/evidence/vacuity_witness.py` | 0 | `vacuity-witness.log` |
| Complete lexical inventory | `/audit-output` | `python3 /audit-output/evidence/k_source_inventory.py` | 0 | `k-source-inventory.json`, `k-source-inventory.log` |
| Every-sentence disposition | `/audit-output` | `python3 /audit-output/evidence/classify_k_inventory.py` | 0 | `k-source-dispositions.csv`, `k-source-dispositions.log` |

The first translation-log attempt mistakenly redirected the terminal recorder,
not just the translator, into `regenerated-solution.mpy`; its comparison exited
1 on recorder bytes. The corrected translator redirection shown above
immediately overwrote that scratch file and produced byte identity. This was a
reviewer logging error, not candidate evidence.
