# Audit command manifest

All candidate source execution occurred on copies under
`/tmp/audit-work/candidate-src`. Candidate-built definitions were not used.
The `script -q -e -c ...` wrapper stored the cited terminal output and final
exit status; the exact inner commands are listed below.

| Stage | Working directory | Exact command | Exit | Log |
|---|---|---|---:|---|
| 1 | `/audit-output` | `bash /audit-output/evidence/01_integrity.sh` | 0 | `logs/01-integrity.log` |
| 1 | `/audit-output` | `bash /audit-output/evidence/01_untrusted_claims.sh` | 0 | `logs/01-untrusted-claims.log` |
| 1 | `/audit-output` | `python3 /audit-output/evidence/01_untrusted_trace_summary.py` | 0 | `logs/01-untrusted-trace-summary.log` |
| 2 | `/audit-output` | `bash /audit-output/evidence/02_fidelity.sh` | 0 | `logs/02-fidelity.log` |
| 2 | `/audit-output` | `python3 /audit-output/evidence/02_differential.py --canonical /tmp/audit-work/reference/canonical.py --candidate /tmp/audit-work/candidate-src/solution.py --inputs-out /audit-output/evidence/differential-inputs.jsonl` | 0 | `logs/02-differential.log` |
| 3 | `/tmp/audit-work/regenerate-helper` | `python3 gen_unicode_case.py && cmp -s unicode-case.k /tmp/audit-work/candidate-src/unicode-case.k && sha256sum unicode-case.k /tmp/audit-work/candidate-src/unicode-case.k` | 0 | `logs/03-regenerate-unicode-helper.log` |
| 3 | `/tmp/audit-work/candidate-src` | `kompile --backend llvm semantic.k --main-module MPY --syntax-module MPY-SYNTAX --output-definition concrete-kompiled` | 0 | `logs/03-kompile-llvm.log` |
| 3 | `/tmp/audit-work/candidate-src` | `kompile --backend haskell semantic.k --main-module MPY --syntax-module MPY-SYNTAX --output-definition concrete-haskell-kompiled` | 0 | `logs/03-kompile-concrete-haskell.log` |
| 3 | `/tmp/audit-work/candidate-src` | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-kompiled` | 0 | `logs/03-kompile-haskell.log` |
| 3 | `/tmp/audit-work/candidate-src` | `bash /audit-output/evidence/03_concrete_runs.sh /tmp/audit-work/candidate-src/concrete-haskell-kompiled` | 0 | `logs/03-concrete-runs-haskell-semantic-only.log` |
| 3 | `/tmp/audit-work/candidate-src` | `bash /audit-output/evidence/03_concrete_runs.sh /tmp/audit-work/candidate-src/proof-kompiled` | 0 | `logs/03-concrete-runs-haskell.log` |
| 3 | `/tmp/audit-work/candidate-src` | `bash /audit-output/evidence/03_concrete_runs.sh` | 0 | `logs/03-concrete-runs.log` |
| 3 | `/tmp/audit-work/candidate-src` | `bash /audit-output/evidence/03_backend_unicode.sh` | 0 | `logs/03-backend-unicode.log` |
| 3 | `/tmp/audit-work/candidate-src` | `bash /audit-output/evidence/03_encoding_bridge.sh` | 0 | `logs/03-encoding-bridge.log` |
| 3 | `/tmp/audit-work/candidate-src` | `kprove spec.k --definition proof-kompiled --spec-module SPEC --claims SPEC.symbolic` | 0, `#Top` | `logs/03-kprove-SPEC-symbolic.log` |
| 3 | `/tmp/audit-work/candidate-src` | `kprove spec.k --definition proof-kompiled --spec-module SPEC --claims SPEC.example-hello` | 0, `#Top` | `logs/03-kprove-SPEC-example-hello.log` |
| 3 | `/tmp/audit-work/candidate-src` | `kprove spec.k --definition proof-kompiled --spec-module SPEC --claims SPEC.example-unicode` | 0, `#Top` | `logs/03-kprove-SPEC-example-unicode.log` |
| 4 | `/tmp/audit-work/candidate-src` | `bash /audit-output/evidence/04_pinning.sh` | 0 | `logs/04-pinning-corrected.log` |
| 4 diagnostic | `/tmp/audit-work/candidate-src` | `kast --definition proof-kompiled --module VERIFICATION --input rule /audit-output/evidence/04_claim-term-rule.k --output kast` | 113, parser diagnostic; not evidence | `logs/04-claim-term-rule-diagnostic.log` |
| 5 | `/audit-output` | `python3 /audit-output/evidence/05_rule_inventory.py` | 0 | `logs/05-rule-inventory.log` |
| 5 | `/audit-output` | `python3 /audit-output/evidence/05_unicode_rule_audit.py` | 0 | `logs/05-unicode-rule-audit.log` |
| 5 | `/audit-output` | `bash /audit-output/evidence/05_k_string_docs.sh` | 0 | `logs/05-k-string-docs.log` |
| 6 | `/tmp/audit-work/candidate-src` | `kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY --dry-run` | 0 | `logs/06-vacuity-dry-run.log` |
| 6 | `/tmp/audit-work/candidate-src` | `kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY` | 1, expected stuck obligation | `logs/06-vacuity-proof.log` |
| 6 | `/tmp/audit-work/candidate-src` | `kprove spec-body-mutation.k --definition proof-kompiled --spec-module SPEC-BODY-MUTATION --dry-run` | 0 | `logs/06-body-mutation-dry-run.log` |
| 6 | `/tmp/audit-work/candidate-src` | `kprove spec-body-mutation.k --definition proof-kompiled --spec-module SPEC-BODY-MUTATION` | 1, expected stuck obligation | `logs/06-body-mutation-proof.log` |
| 6 | `/tmp/audit-work/bridge-mutation` | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition mutated-proof-kompiled` | 0 | `logs/06-bridge-mutation-build.log` |
| 6 | `/tmp/audit-work/bridge-mutation` | `diff -u /tmp/audit-work/candidate-src/semantic.k /tmp/audit-work/bridge-mutation/semantic.k` | 1, expected difference | `logs/06-bridge-mutation-diff.log` |
| 6 | `/tmp/audit-work/bridge-mutation` | `kprove spec.k --definition mutated-proof-kompiled --spec-module SPEC --claims SPEC.example-hello --dry-run` | 0 | `logs/06-bridge-mutation-dry-run.log` |
| 6 | `/tmp/audit-work/bridge-mutation` | `kprove spec.k --definition mutated-proof-kompiled --spec-module SPEC --claims SPEC.example-hello` | 1, expected stuck obligation | `logs/06-bridge-mutation-proof.log` |

`04-pinning.log` and `04_claim-term-rule.k` preserve an initial diagnostic
attempt that tried to feed the internal `.Exprs` list-unit notation to the
external program parser. It failed in that parser and was not used as evidence.
The corrected comparison uses the translator's external empty-list spelling;
both terms parse to byte-identical KAST.
