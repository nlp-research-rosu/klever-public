# Claim-by-claim adequacy and satisfiability

The submitted `spec.k` contains nine unlabeled claims. The audit-only
`spec-labeled.k` adds names without changing any claim body; every labeled claim
closed independently in `09-kprove-individual.log`.

| Claim | Plain-language precondition | Plain-language postcondition | Satisfying ground witness | Relation to requested theorem |
|---|---|---|---|---|
| `empty-contract` (`spec.k:7-12`) | Fresh configuration, empty integer input | Actual submitted program terminates, final argument binding is empty, result is `contract([])=none` | `input()` | Complete and correct for empty input. Both Python functions return `None`. |
| `nonempty-initialization` (`16-29`) | Fresh configuration, symbolic nonempty input `X,IS` | Execution reaches the loop head with tail `X,IS`, `total=0`, `sign=1`, `x=0`; result remains `noResult` | `X=2`, `IS=.Ints` | Executes the real entry prefix but makes no return-value claim. |
| `negative-step` (`32-44`) | A loop head with negative `X`; arbitrary `T,S`, old `x`, tail, framed cells | Exactly one iteration consumes `X`, adds its magnitude and multiplies sign by `-1` | Reachable state for input `[-2]`: `X=-2`, `IS=.Ints`, `T=0`, `S=1`, old `x=0` | Correct one-step lemma, but contains neither original input nor a prefix/suffix invariant. |
| `positive-step` (`47-59`) | Same, with positive `X` | Exactly one iteration adds `X` and multiplies sign by `1` | Reachable state for `[2]`: `X=2`, `T=0`, `S=1`, old `x=0` | Correct one-step lemma only. |
| `zero-step` (`62-74`) | Same, with `X=0` | Exactly one iteration preserves total and sets sign to `0` | Reachable state for `[0]`: `X=0`, `T=0`, `S=1`, old `x=0` | Correct one-step lemma only. |
| `loop-exit` (`77-83`) | Empty loop tail, arbitrary accumulator integers `T,S`, pending actual return | Execution returns exactly `T*S` | State reached after `[2]`: `T=2`, `S=1` | Correctly constrains the return expression but does not relate `T,S` to the input. |
| `example-negative` (`86-96`) | Exact input `[1,2,2,-4]` | Actual submitted program terminates with final state and `contract(...)=-9` | The stated input | Complete but fixed example; both Python functions return `-9`. |
| `example-zero` (`98-108`) | Exact input `[0,1]` | Actual submitted program terminates with final state and result `0` | The stated input | Complete but fixed example; both Python functions return `0`. |
| `example-three-negative` (`110-120`) | Exact input `[-1,-2,-3]` | Actual submitted program terminates with final state and result `-6` | The stated input | Complete but fixed example; both Python functions return `-6`. |

For a nonempty list not among the examples, such as `[2]`, both trusted
canonical Python and candidate Python return `2`, and fresh K execution also
returns `2`. But no submitted entry claim says that: the only symbolic entry
claim stops before the loop with `noResult`.

The missing result-constraining theorem has the shape recorded in
`/tmp/audit-work/fresh/spec-intended.k`: for every `IS:Ints`,
`boot(solutionProgram)` must terminate with `result(contract(IS))`. It parses
successfully but does not close (`12-missing-universal-target.log`). The three
one-step claims can validate any chosen finite unrolling; without a
machine-checked invariant/summary claim linking the arbitrary loop tail and
accumulators to `contract(IS)`, they do not constitute a K proof for
unrestricted finite integer lists.

Mechanical pinning passes: trusted translation is byte-identical
(`02-translation.log`), and expanding V12-V14 yields the identical K
constructor AST (`10-program-term-compare.log`). A body mutation that changes
the positive branch in V12—the term actually executed by all claims—builds but
causes the positive-step claim to get stuck
(`11-body-sensitivity.log`). Therefore the defect is not a substituted program
or body-insensitive proof.
