# Reviewer command record

All commands ran in the audit container on 2026-07-26. Candidate inputs under
`/candidate` and launcher records were read-only. Builds were made only below
`/tmp/audit-work`; logs and reviewer-authored artifacts were written only below
`/audit-output/evidence`.

## Stages 1–2

| Working directory | Exact command | Exit | Relevant output |
|---|---|---:|---|
| `/audit-output` | `python3 /audit-output/evidence/integrity_check.py 2>&1 \| tee /audit-output/evidence/stage1-integrity.log` | 0 | `failure_count=0` |
| `/audit-output` | `python3 /audit-output/evidence/inspect_generation.py 2>&1 \| tee /audit-output/evidence/stage1-generation-inspection.log` | 0 | 739 JSONL records parsed; generation claims treated as untrusted |
| `/audit-output` | `python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/candidate/regenerated.mpy && cmp --silent /tmp/audit-work/candidate/regenerated.mpy /tmp/audit-work/candidate/solution.mpy && sha256sum /tmp/audit-work/candidate/regenerated.mpy /tmp/audit-work/candidate/solution.mpy \| tee /audit-output/evidence/stage2-translation.log` | 0 | Both files `cd9c3c57…a69bbd7` |
| `/audit-output` | `python3 /audit-output/evidence/differential_test.py 2>&1 \| tee /audit-output/evidence/stage2-differential.log` | 0 | 1,000 domain inputs, zero mismatches |

## Stage 3

| Working directory | Exact command | Exit | Relevant output |
|---|---|---:|---|
| `/tmp/audit-work/candidate` | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition fresh-runtime-kompiled` | 0 | Fresh LLVM definition; warnings recorded in `stage3-kompile-runtime.log` |
| `/tmp/audit-work/candidate` | `kompile verification.k --backend haskell --main-module ROMAN-BASE --syntax-module MPY-SYNTAX --output-definition fresh-lemma-kompiled` | 0 | Fresh base Haskell definition |
| `/tmp/audit-work/candidate` | `kompile verification.k --backend haskell --main-module ROMAN-VERIFICATION --syntax-module MPY-SYNTAX --output-definition fresh-verification-kompiled` | 0 | Fresh extended Haskell definition |
| `/tmp/audit-work/candidate` | `python3 /tmp/audit-work/trusted/py2mpy.py /audit-output/evidence/k_semantics_smoke.py > /tmp/audit-work/candidate/k-semantics-smoke.mpy && krun k-semantics-smoke.mpy --definition fresh-runtime-kompiled --output none` | 0 | Eight asserted normal/boundary results; empty log is expected with `--output none` |
| `/tmp/audit-work/candidate` | `kprove spec.k --definition fresh-lemma-kompiled --spec-module ROMAN-LEMMA-SPEC` | 0 | `#Top` |
| `/tmp/audit-work/candidate` | `kprove spec.k --definition fresh-verification-kompiled --spec-module ROMAN-SPEC` | 0 | `#Top` |
| `/tmp/audit-work/candidate` | `bash /audit-output/evidence/run_individual_claims.sh` | 0 | All nine labeled claims independently exited 0 and printed `#Top` |

The individual script records every exact labeled command in
`stage3-individual-claims-summary.log`; the complete per-claim outputs are
`stage3-claim-*.log`.

## Stages 4–5

| Working directory | Exact command | Exit | Relevant output |
|---|---|---:|---|
| `/audit-output` | `python3 /audit-output/evidence/program_term_compare.py 2>&1 \| tee /audit-output/evidence/stage4-program-term-comparison.log` | 0 | Five parameter/body constructor comparisons equal |
| `/audit-output` | `python3 /audit-output/evidence/claim_witnesses.py 2>&1 \| tee /audit-output/evidence/stage4-ground-witnesses.log` | 0 | 1,000 grounded K postconditions agree with both Python functions |
| `/audit-output` | `python3 /audit-output/evidence/build_rule_inventory.py 2>&1 \| tee /audit-output/evidence/stage5-rule-inventory-summary.log` | 0 | 1,003 exhaustive inventory records; four rejected bridges |
| `/tmp/audit-work/candidate` | `kprove /audit-output/evidence/bridge_rule_witnesses.k --definition fresh-verification-kompiled --spec-module BRIDGE-FALSE-WITNESSES` | 0 | `#Top` for all four false numeral results |
| `/tmp/audit-work/candidate` | `kprove /audit-output/evidence/bridge_rule_witnesses.k --definition fresh-lemma-kompiled --spec-module BASE-CORRECT-WITNESSES` | 0 | `#Top` for all four fixed-semantics `"z"` results |
| `/tmp/audit-work/candidate` | `bash /audit-output/evidence/run_bridge_base_false.sh` | 0 | Harness success; each of four inner `kprove` commands exited 1 with `WarnStuckClaimState` |
| `/tmp/audit-work/candidate` | `kprove /audit-output/evidence/entry_body_sensitivity.k --definition fresh-verification-kompiled --spec-module ENTRY-BODY-MUTATION-BRIDGED` | 0 | `#Top` despite actual helper body mutation |
| `/tmp/audit-work/candidate` | `kprove /audit-output/evidence/entry_body_sensitivity.k --definition fresh-lemma-kompiled --spec-module ENTRY-BODY-MUTATION-FIXED` | 1 (expected) | `WarnStuckClaimState`; fixed execution result is `"z"` |

For the four base-false commands, exact commands and inner statuses are in
`stage5-base-false-summary.log`. Each full residual ends in
`str(iCons(122, .IntSeq))`, i.e. `"z"`, rather than the bridge-fabricated
place digit.

## Stage 6

| Working directory | Exact command | Exit | Relevant output |
|---|---|---:|---|
| `/tmp/audit-work/candidate` | `kprove /audit-output/evidence/spec-vacuity.k --definition fresh-verification-kompiled --spec-module AUDIT-SPEC-VACUITY --dry-run` | 0 | Mutation parses and builds to KORE |
| `/tmp/audit-work/candidate` | `kprove /audit-output/evidence/spec-vacuity.k --definition fresh-verification-kompiled --spec-module AUDIT-SPEC-VACUITY` | 1 (expected) | `WarnStuckClaimState`; failed equality between genuine result and result with extra `x` |

## Toolchain

`kompile --version`, `kprove --version`, and `krun --version` each reported K
v7.1.293. Exact output is in `toolchain.log`.
