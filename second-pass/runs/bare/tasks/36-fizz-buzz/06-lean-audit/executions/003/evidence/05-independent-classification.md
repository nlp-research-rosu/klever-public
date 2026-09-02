# Independent Stage 3 classification

Frozen sources inspected: `verification.k`, `semantic.k`, `spec.k`,
`solution.py`, `solution.mpy`, and `prove.sh`. The local verification-module
closure reconstructed by the trusted inventory contains only `VERIFICATION`;
the imported fixed operational semantics lives in the required `semantic.k`.

| Source rule ID | Span | Independent class | Semantic judgment |
|---|---:|---|---|
| `rule-e763c3f…` | 13–14 | `DEFINITION` | Negative branch of the named `fizzEnd` summary; for `N < 0`, the program's `i` remains its initialized value `0`. |
| `rule-1904e693…` | 15–16 | `DEFINITION` | Nonnegative branch of `fizzEnd`; the outer loop increments `i` from `0` until `i = N`. |
| `rule-30079623…` | 18–19 | `DEFINITION` | Base equation of the named `digitSevens` summary. The reachable inner-loop boundary is nonnegative, and `X = 0` contributes zero digits; the negative branch totalizes the summary without replacing program execution. |
| `rule-729ad4a6…` | 20–21 | `DEFINITION` | Recursive equation of `digitSevens` for a positive number ending in seven. It adds one and descends through positive integer division by ten, exactly matching the inner-loop body. |
| `rule-5d535d52…` | 22–23 | `DEFINITION` | Complementary positive recursive equation of `digitSevens`; it descends without incrementing when the last digit is not seven. |
| `rule-6f6d25b6…` | 25–26 | `DEFINITION` | First branch of the named `fizzContribution` summary. Divisibility by 11 makes the source conditional execute the digit-counting loop. |
| `rule-e81d3927…` | 27–28 | `DEFINITION` | Second, disjoint eligible branch of `fizzContribution`; divisibility by 13 after excluding divisibility by 11 also executes the digit-counting loop. |
| `rule-ebf29519…` | 29–30 | `DEFINITION` | Complementary branch of `fizzContribution`; divisibility by neither 11 nor 13 leaves `count` unchanged. |
| `rule-dde8b848…` | 32–33 | `DEFINITION` | Base equation of the named interval summary `fizzFrom`; an empty interval contributes zero. |
| `rule-7ba888d5…` | 34–35 | `DEFINITION` | Recursive equation of `fizzFrom`; it adds the current source-loop contribution and advances `I` by one. |
| `rule-115fa5a8…` | 38 | `DOMAIN_LEMMA` | Integer-addition associativity. It is an extra algebraic fact used to normalize the symbolic invariant sum, not a definition or an execution rule. It is relevant to `count + fizzContribution + fizzFrom` versus the right-associated postcondition. |
| `rule-948f699a…` | 43–48 | `DEFINITION` | Macro equation defining the named proof term `INNER-LOOP` as the exact translated inner-loop AST. It does not preempt fixed execution; after macro expansion, the ordinary `While`, `If`, `Assign`, `BinOp`, and lookup rules execute. |
| `rule-55f4df2b…` | 51–59 | `DEFINITION` | Macro equation defining `OUTER-LOOP` as the exact translated outer-loop AST, including the exact inner-loop macro. |

The three `fizzContribution` guards are disjoint and exhaustive. The
`digitSevens` guards are disjoint and exhaustive, with strict descent for
positive inputs. The `fizzFrom` guards are disjoint and exhaustive, with
strict progress toward `N`. The `fizzEnd` guards are disjoint and exhaustive.

There are no `OPERATIONAL_RULE` entries in `verification.k`: no rule matches a
fixed-semantics configuration cell or replaces execution. There are no
`PROVED_DERIVED_LEMMA` entries: `prove.sh` compiles `verification.k` once with
the associativity simplifier already present, and only afterward runs
`kprove spec.k`; no earlier proof of that exact rule against a module omitting
it exists in the frozen workspace.

Independent classification result: 12 `DEFINITION`, 0 `OPERATIONAL_RULE`,
0 `PROVED_DERIVED_LEMMA`, and 1 relevant `DOMAIN_LEMMA`. This exactly agrees
with the protected Stage 3 manifest.
