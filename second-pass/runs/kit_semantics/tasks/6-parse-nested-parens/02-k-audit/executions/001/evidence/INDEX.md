# Reviewer evidence index

All executable experiments used source copied to
`/tmp/audit-work/6-parse-nested-parens`; no candidate-provided kompiled
definition or cache was used.

| Stage | Artifact | Result |
|---|---|---|
| 1 | `check_integrity.py`, `stage1-integrity.log` | Pipeline-v3 mounts and required records present; every directly recorded hash matched; campaign block/hash matched; supplied-semantics trees recursively identical with no symlinks. |
| 2 | `differential_test.py`, `stage2-differential.log` | 143,039 intended-domain cases; canonical, submitted Python, and independent oracle had zero mismatches. |
| 2 | `stage2-regeneration.log` | Trusted translator regeneration was byte-identical to `solution.mpy`. |
| 3 | `stage3-kompile-runtime.log`, `stage3-krun-runtime.log` | Fresh LLVM definition built; reviewer assertions terminated at `.K`, `NoExc`, exit code 0. |
| 3 | `stage3-kompile-proof.log`, `stage3-kprove-all.log` | Fresh Haskell definition built; both positive claims closed with `#Top`, exit 0. |
| 3 | `stage3-kprove-scan-loop.log` | Loop circularity alone closed with `#Top`, exit 0. |
| 4 | `pinning.k`, `stage4-kprove-pinning-attempt4.log` | Candidate AST shorthand normalized to the full constructor term; `#Top`, exit 0. Earlier `attempt1`–`attempt3` logs preserve reviewer probe syntax iterations. |
| 4 | `pinning-expanded.mpy`, `stage4-kast-constructor-comparison-attempt2.log` | KORE parses of the submitted and explicit module terms were byte-identical. |
| 4 | `ground.k`, `stage4-kprove-ground.log`, `stage4-ground-python.log` | Empty and `"(()) ()"` satisfying substitutions proved; both Python implementations returned `[2, 1]` for the nonempty witness. |
| 4 | `body-sensitivity.patch`, `stage4-kprove-body-mutation.log` | Changing the executed `solutionBody` initial depth from 0 to 1 made the original target fail with the expected summary mismatch. |
| 5 | `inventory_k.py`, `rule-inventory.tsv`, `stage5-inventory-generation.log` | Exhaustive 986-entry inventory: 246 syntax declarations, 732 rules, five contexts, one configuration, two claims. |
| 6 | `false-result.k`, `stage6-false-result-dry-run.log` | Fresh false claim built successfully. |
| 6 | `stage6-false-result-proof.log` | False `[2]` result for `"()"` failed with `WarnStuckClaimState`, actual heap `[1]`, exit 1. |
| 7 | `toolchain.log` | K v7.1.293 and Python 3.10.12. |

`stage3-diagnostic-entry-without-helper.log` is a deliberately bounded
diagnostic: filtering the entry claim alone also filters out its loop
circularity, so that altered proof problem was interrupted after ten seconds
(exit 124). It is not the candidate's required positive command; the proper
whole-spec run is recorded in `stage3-kprove-all.log`.
