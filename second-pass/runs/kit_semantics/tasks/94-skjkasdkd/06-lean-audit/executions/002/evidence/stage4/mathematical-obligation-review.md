# Independent mathematical review of the generated obligations

The 13 obligations occur in the same source order as the independently identified 13 `DOMAIN_LEMMA` rules. No obligation is duplicated, omitted, or a stand-alone `True` proposition.

| # | Frozen lines | Generated proposition, independently interpreted | Judgment |
|---:|---:|---|---|
| 1 | 74–76 | Optional `Val → Int` projection is defined iff `definedProjectInt V = true`; the extra `∧ True` is the faithful translation of `#Ceil(@V)` for the already well-sorted `Val` variable. | Faithful and substantive; the iff is not vacuous. |
| 2 | 82–84 | Under `definedProjectInt V`, the K cast/projection equals `projectIntTotal V`. | Exact guarded reverse-projection rule. |
| 3 | 87–89 | Reinjecting `projectIntTotal V` and projecting again is idempotent. | Exact rule. |
| 4 | 93–96 | For an integer-valued `V`, dynamic `applyCmp(">", V, I)` equals integer `projectIntTotal V >Int I`. | Exact guarded dispatch bridge used by the scan. |
| 5 | 98–101 | The analogous `>=` dispatch equality. | Exact guarded dispatch bridge used by candidate initialization. |
| 6 | 103–106 | `applyCmp("<", I, V)` equals `I <Int projectIntTotal V` for integer-valued `V`. | Exact guarded dispatch bridge used by the divisor loop. |
| 7 | 108–111 | `applyBin("%", V, I)` equals the injected `pyMod(projectIntTotal V, I)` for integer-valued `V`. | Exact guarded Python-modulo dispatch used by both loops. |
| 8 | 113–116 | `applyBin("+", V, I)` equals injected integer addition for integer-valued `V`. | Exact guarded addition dispatch used by updates. |
| 9 | 133–137 | A divisor `D` in `[2,N)` with `pyMod N D = 0` makes `primeTail N D = false`. | Exact composite shortcut from the recurrence. |
| 10 | 138–142 | If `D>2`, `D≤N`, and `D-1` does not divide `N`, then `primeTail N D = primeTail N (D-1)`. | Exact backward fold used to summarize the divisor loop. |
| 11 | 174–178 | For positive `N`, one `pyMod` digit plus the recursive decimal quotient equals `digitSum N`. | Exact reverse orientation of the defining recurrence. |
| 12 | 179–184 | The same equation after expanding `pyMod(N,10)` to normalized truncating remainder. | Exact normalized fold; no weakened arithmetic. |
| 13 | 185–191 | The normalized digit fold under an arbitrary accumulator `T`. | Exact accumulator form required by the `total += ...` loop. |

The guards retain the frozen match domains. Variables appearing as unused Lean hypotheses correspond to conditions whose truth is already forced by the candidate's exact constructors/definitions; their presence does not delete a source guard. In particular, adversarial integer/noninteger, boundary, negative-remainder, prime/composite, and accumulator cases were evaluated separately in Stage 5 evidence.
