# Reviewer command index

All source/build paths below are reviewer-owned scratch copies under
`/tmp/audit-work/118-get-closest-vowel`. Each linked log contains the exact
command, relevant bounded output, and exit status.

| Purpose | Command | Status | Log |
|---|---|---:|---|
| Provenance/integrity | `bash /audit-output/evidence/provenance/run_provenance_check.sh` | 0 | `provenance/provenance_check.log` |
| Required record inspection | `bash /audit-output/evidence/provenance/inspect_generation_records.sh` | 0 | `provenance/generation_records.log` |
| Trusted translation + differential | `bash /audit-output/evidence/fidelity/run_fidelity_checks.sh` | 1 (three real divergences) | `fidelity/fidelity_checks.log` |
| LLVM build | `kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/118-get-closest-vowel/build/concrete-kompiled --warnings none` | 0 | `build/kompile-llvm.log` |
| Haskell proof build | `kompile semantic.k --backend haskell --main-module MPY --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/118-get-closest-vowel/build/proof-kompiled --warnings none` | 0 | `build/kompile-haskell.log` |
| Generated-semantics comparison | `python3 /audit-output/evidence/build/concrete_compare.py` | 1 (K/real-Python mismatch at length 1000) | `build/concrete-compare.log` |
| All 13 positive claims | `kprove spec.k --definition /tmp/audit-work/118-get-closest-vowel/build/proof-kompiled --spec-module SPEC --warnings none` | 0, `#Top` | `build/kprove-all.log` |
| Individually selected base claims | commands printed per label by `run_individual_claims.sh` and the addendum | 0/`#Top` for C01-C05, C09, C12; C06 diagnostic interrupted after about 120 seconds because selection removed its mutual structural claims | `build/kprove-individual.log`, `build/kprove-individual-addendum.log` |
| Pinning + satisfying witnesses | `bash /audit-output/evidence/static/run_pinning_and_witnesses.sh` | 0 | `static/pinning-and-witnesses.log` |
| Material body sensitivity | `bash /audit-output/evidence/static/run_body_sensitivity.sh` | 0 (the probe successfully exposed insensitivity) | `static/body-sensitivity.log` |
| False mutation parse/build | `kprove spec-vacuity.k --definition /tmp/audit-work/118-get-closest-vowel/build/proof-kompiled --spec-module SPEC-VACUITY --dry-run --warnings none` | 0 | `nonvacuity/dry-run.log` |
| False mutation proof | same command without `--dry-run` | 1, `WarnStuckClaimState` | `nonvacuity/proof.log` |
| Raw K inventory | `rg -n '^[[:space:]]*(configuration|syntax|rule|claim)' semantic.k verification.k program.k spec.k` plus per-kind counts | 0 | `static/raw-rule-inventory.log` |

The original unlabeled `spec.k` is one mutually structural proof module: the
fresh aggregate `kprove` command checks all 13 claims and is the candidate's
positive target command. Selecting an inductive claim alone removes the other
claims that form its constructor-case circularity; the interrupted C06
diagnostic therefore is not treated as a failed candidate proof command.
