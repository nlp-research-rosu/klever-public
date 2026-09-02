# Reviewer command ledger

All build/proof commands ran from `/tmp/audit-work/reconstruction`; diagnostic
and audit scripts are preserved in `/audit-output/evidence`. Candidate-provided
compiled directories were never copied or referenced.

| Stage | Exact command | Exit | Relevant result/log |
|---|---|---:|---|
| 1 | `python3 /audit-output/evidence/provenance_check.py` | 0 | `OVERALL=PASS`; `stage1-provenance.log` |
| 1 | `python3 /audit-output/evidence/generation_trace_audit.py` | 0 | all 408 JSONL records parsed; all required text records scanned; `stage1-generation-trace-audit.log` |
| 1 | `find /candidate -type f -print0 \| sort -z \| xargs -0 sha256sum > /audit-output/evidence/candidate-files.sha256` | 0 | all 779 candidate files independently hashed; `stage1-candidate-full-hash.log` |
| 2 | `python3 py2mpy.py solution.py > solution.mpy` | 0 | trusted translator; `stage2-translation-identity.log` |
| 2 | `cmp -s solution.mpy submitted-solution.mpy` | 0 | byte identity; both SHA-256 `583efb...1262d`; same log |
| 2 | `python3 /audit-output/evidence/differential_test.py` | 0 | 438 inputs, zero numeric/list mismatches; `stage2-differential.log` |
| 3 | `python3 py2mpy.py /audit-output/evidence/k_smoke.py > audit-smoke.mpy` | 0 | reviewer smoke translation; `stage3-concrete-build.log` |
| 3 | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition fresh-runtime-kompiled` | 0 | fresh LLVM build; same log |
| 3 | `krun audit-smoke.mpy --definition fresh-runtime-kompiled` | 0 | final `.K`, `NoExc`, exit-code 0; `stage3-concrete-run.log` |
| 3 | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX --output-definition fresh-verification-kompiled` | 0 | fresh Haskell build; `stage3-proof-build.log` |
| 3 | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.tri-loop` | 0 | `#Top`; `stage3-proof-tri-loop.log` |
| 3 | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.tri-at-zero` | 0 | `#Top`; `stage3-proof-tri-at-zero.log` |
| 3 | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.tri-at-one` | 0 | `#Top`; `stage3-proof-tri-at-one.log` |
| 3 | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.tri-at-even` | 0 | `#Top`; `stage3-proof-tri-at-even.log` |
| 3 | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.tri-at-odd-recurrence` | 0 | `#Top`; `stage3-proof-tri-at-odd-recurrence.log` |
| 3 | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC --claims SPEC.tri-loop,SPEC.tri-entry` | 0 | dependency-closed entry proof `#Top`; `stage3-proof-entry-with-loop.log` |
| 3 | `kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC` | 0 | all six claims, `#Top`; `stage3-proof-all.log` |
| 4 | `kast solution.mpy --definition fresh-verification-kompiled --module VERIFICATION-SYNTAX --sort Module --expand-macros --output json --output-file /audit-output/evidence/pinning-solution.ast.json` | 0 | parsed regenerated program; `stage4-constructor-pinning.log` |
| 4 | `kast --expression "Module(triDefinition)" --definition fresh-verification-kompiled --module VERIFICATION-SYNTAX --sort Module --expand-macros --output json --output-file /audit-output/evidence/pinning-claim.ast.json` | 0 | parsed claim program; same log |
| 4 | `cmp -s /audit-output/evidence/pinning-solution.ast.json /audit-output/evidence/pinning-claim.ast.json` | 0 | constructor identity; same SHA-256 `5f37fe...654e`; same log |
| 4 | `kprove ground-witness.k --definition fresh-verification-kompiled --spec-module AUDIT-GROUND-WITNESS` | 0 | four ground results, `#Top`; `stage4-ground-witness-k.log` |
| 4 | `python3 /audit-output/evidence/witness_compare.py` | 0 | K/Python equality at N=0,3,4,10; `stage4-witness-compare.log` |
| 5 | `python3 /audit-output/evidence/k_rule_inventory.py > /audit-output/evidence/K-INVENTORY.md` | 0 | 705/705 rules and 233/233 syntax blocks covered; `stage5-inventory-final.log` |
| 5 | `kprove body-sensitivity.k --definition fresh-verification-kompiled --spec-module AUDIT-BODY-SENSITIVITY` | 1 expected | stuck on executed mutated heap `[99]`; `stage5-body-sensitivity.log` |
| 6 | `kprove fresh-false-result.k --definition fresh-verification-kompiled --spec-module AUDIT-FRESH-FALSE-RESULT` | 1 expected | `WarnStuckClaimState`, actual last value 15 versus false 16; `stage6-fresh-false-result.log` |

Diagnostic only: selecting `SPEC.tri-entry` without `SPEC.tri-loop` removes the
loop circularity and unrolls indefinitely. The reviewer interrupted
`kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC
--claims SPEC.tri-entry` with Ctrl-C (exit 130). This does not test the
dependency-closed proof; the subsequent two-claim and full-spec commands above
are the valid positive entry reconstructions.
