# Reviewer evidence index

Every command log records the working directory, exact argv, exit status,
output byte count, truncation status, and combined output.

| Evidence | Purpose | Result |
|---|---|---|
| `01-provenance-check.log` | Hash/type/symlink checks, campaign-lock comparison, supplied-semantics recursive comparison | Exit 0; all applicable file and pipeline-tree hashes match; no semantics differences or symlinks |
| `02-generation-records.log` | Full parse/inspection of every required pipeline-v3 record and all 447 trace events | Exit 0 |
| `03`–`05` logs | Create isolated scratch and copy only candidate source plus trusted inputs | Exit 0 |
| `06-program-fidelity.log` | Trusted translator regeneration | Exit 0; byte identity |
| `07-differential-test.log` | Trusted canonical versus generated Python over examples, branches, boundary, deterministic random sample | Exit 0; 597 positive inputs, 0 mismatches, 0 contract failures |
| `08-tool-versions.log` | Live toolchain | K 7.1.293 |
| `09-kompile-llvm.log` | Fresh concrete definition | Exit 0 |
| `10`–`12` logs | Fresh probe translation, CPython execution, and `krun` | All exit 0; K ends at `.K`, `NoExc`, exit code 0 |
| `13-kompile-haskell.log` | Fresh proof definition | Exit 0 |
| `14-kprove-all-positive.log` | Both submitted positive claims | Exit 0, `#Top` |
| `15-kprove-factor-loop.log` | Helper loop claim selected by fully qualified label | Exit 0, `#Top` |
| `16-kprove-factorize-with-helper.log` | Entry claim with required helper circularity | Exit 0, `#Top` |
| `16-kprove-factorize.log` | Early diagnostic using an unqualified filter label | Exit 113 before proof; superseded by the fully qualified commands above |
| `17-program-pinning.log` | Constructor-level regenerated-body/claim comparison | Exit 0; both closure bodies match |
| `18-claim-witnesses.log` | Ground postcondition substitutions | Exit 0; all compared results equal |
| `19-rule-inventory.log` | Exhaustive K inventory | Exit 0; 26 files, 934 declarations, 698 rules |
| `used-semantics-map.md` | Per-rule-family disposition and active execution slice | All 698 rules accounted for |
| `21-false-mutation-dry-run.log` | Fresh false claim parse/build | Exit 0 |
| `22-false-mutation-kprove.log` | Fresh result mutation | Exit 1 with expected `WarnStuckClaimState`; actual empty list shown |
| `23-body-sensitivity-kprove.log` | Fresh mutation of the closure body actually executed | Exit 1 with expected `WarnStuckClaimState`; mutated `[4]` result shown |

Reviewer-authored executable/source artifacts are preserved in this directory:
`run_logged.py`, `provenance_check.py`, `generation_records_inspect.py`,
`program_fidelity.py`, `differential_test.py`, `concrete-probe.py`,
`generate_mpy.py`, `program_pinning.py`, `claim_witnesses.py`,
`k_rule_inventory.py`, `spec-audit-false.k`, and
`spec-body-sensitivity-audit.k`.
