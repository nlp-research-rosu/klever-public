# Auditor evidence index

Every `*.log` produced with `script -q -e -c` contains the exact inner command
in its header and `COMMAND_EXIT_CODE` in its footer.

| Evidence | Exit | Meaning |
|---|---:|---|
| `01b-provenance-complete.log` | 0 | Complete mounted-input, hash, record, type, symlink, and supplied-semantics comparison |
| `02-translation-identity.log` | 0 | Trusted regeneration is byte-identical |
| `03b-differential-valid.log` | 1 | Valid differential; expected audit failure due four real canonical mismatches |
| `04-tool-versions.log` | 0 | K tool discovery and v7.1.293 |
| `05-compile-reference-haskell.log` | 0 | Fresh supplied MPY Haskell definition |
| `06-prove-projection.log` | 0 | Bridge-free count connection `#Top` |
| `07-compile-verification.log` | 0 | Fresh candidate verification Haskell definition |
| `08-prove-target-all.log` | 0 | Complete three-claim target `#Top` |
| `08a-prove-outer-claim.log` | 0 | Loop claim `#Top` |
| `08b-prove-empty-claim.log` | 0 | Empty entry claim `#Top` |
| `08c-prove-cons-with-loop.log` | 0 | Nonempty entry plus required loop circularity `#Top` |
| `09-constructor-pinning.log` | 0 | Expanded claim body equals trusted translated body |
| `10b-rule-inventory-valid.log` | 0 | Exhaustive 1,035-declaration inventory |
| `11-fresh-vacuity.log` | 1 | Expected `WarnStuckClaimState` on false empty result |
| `12-body-sensitivity.log` | 1 | Expected stuck claim after changing the executed closure body |
| `13-count-opposite.log` | 1 | Expected stuck claim: fixed count is 2, not 1 |
| `14-compile-concrete.log` | 0 | Trusted translation plus fresh LLVM definition |
| `15-concrete-run.log` | 0 | Reviewer ASCII assertions finish at `.K`, exit code 0 |
| `16-generation-record-summary.log` | 0 | Every trace/log record read; bounded untrusted-claim summary |

`03-differential.log` is the preserved invalid first harness run described in
`REVIEW.md`; it was superseded by `03b`. `10-rule-inventory.log` is the
preserved first inventory whose declaration grouping omitted displayed
`requires` clauses; it was corrected and superseded by `10b`.
