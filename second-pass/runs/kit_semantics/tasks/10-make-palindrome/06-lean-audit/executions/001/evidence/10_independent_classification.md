# Independent Stage 3 classification

The trusted inventory reconstructs 16 local rules in the closure
`VERIFICATION-SYNTAX -> VERIFICATION`. None has a `simplification`
attribute. I classified rules by their behavior in the frozen K source, not by
their names or the protected rationales.

| Span | Rule head | Independent class | Reason |
|---|---|---|---|
| 29–38 | `isPalindromeBody` | `DEFINITION` | Exact macro expansion of the source function's statement AST. |
| 40–43 | `reverseLoopBody` | `DEFINITION` | Exact macro expansion of the first loop's assignment AST. |
| 45–65 | `searchLoopBody` | `DEFINITION` | Exact macro expansion of the second loop's conditional and assignments. |
| 67–84 | `makePalindromeBody` | `DEFINITION` | Exact macro expansion of the source function body AST. |
| 86–90 | `isPalindromeClosure` | `DEFINITION` | Names the closure value built from the exact parameter, body, and defining scope. |
| 92–96 | `makePalindromeClosure` | `DEFINITION` | Names the closure value built from the exact parameter, body, and defining scope. |
| 98–107 | `solutionModule` | `DEFINITION` | Names the module AST containing the two exact `FuncDef` terms. |
| 109 | `reverseAcc(.IntSeq,A)` | `DEFINITION` | Base equation of a reverse-with-accumulator summary. |
| 110–111 | `reverseAcc(iCons(C,R),A)` | `DEFINITION` | Structurally decreasing recurrence; it establishes `reverseAcc(R,A) = reverse(R) ++ A`. |
| 113–114 | `palIS(S)` | `DEFINITION` | Defines a Boolean summary as equality of `S` with `reverseAcc(S,.IntSeq)`; it does not assert a proposition about program output. |
| 116–117 | `seedResult(S)` when `palIS(S)` | `DEFINITION` | Guarded branch of the initial-result summary. |
| 118–120 | `seedResult(S)` when `notBool palIS(S)` | `DEFINITION` | Complementary guarded branch of the initial-result summary. |
| 122–125 | `searchResult(...,true,RESULT)` | `DEFINITION` | Base equation: once `found` is true, later loop iterations cannot change `result`. |
| 126–129 | `searchResult(...,.IntSeq,...,RESULT)` | `DEFINITION` | Base equation: an exhausted iterator returns the accumulated result. Its overlap with the prior base equation has the same RHS. |
| 130–148 | `searchResult(S,iCons(C,R),P,RP,REV,false,RESULT)` | `DEFINITION` | Structurally decreasing recurrence exactly mirroring one unfound loop iteration: update `P` and `RP`, test the source equality, then either select the candidate or recur on `R`. |
| 150–158 | `completePal(S)` | `DEFINITION` | Initializes the search summary with `S`, empty prefixes, `reverseAcc(S,.)`, `palIS(S)`, and `seedResult(S)`. It is a composition/initialization equation, not a claim that its value is shortest or palindromic. |

## Operational-semantic check

The supplied semantics loads `solutionModule` into ordinary `FuncDef`
execution, binds the resulting closures, evaluates the call, executes
assignments, and iterates strings through `#iterNext`/`#loop`. String `+` is
`seqConcat`, string equality is sequence equality, and iteration yields
one-character strings in source order. Consequently:

- the first operational loop computes `reverseAcc(S,.IntSeq)`;
- the initial `found` and `result` assignments compute `palIS(S)` and
  `seedResult(S)`;
- the second operational loop is summarized by the three `searchResult`
  equations; and
- the entry claim's `completePal(S)` is the exact initialized post-state
  summary.

The nine summary equations occur in claim results and symbolic post-state
values; none matches or preempts a source-program `<k>` redex. The seven
macro/named-term rules expand to the exact frozen AST rather than replacing its
execution. Thus there are no local `OPERATIONAL_RULE` entries.

There is no rule first proved against a module omitting it and then imported for
later use, so there is no `PROVED_DERIVED_LEMMA`. The loop reachability claims
in `spec.k` are claims, not rules in this inventory.

There is also no `DOMAIN_LEMMA`. In particular, `palIS` defines a predicate and
`completePal` defines a recursive execution summary; no inventory rule asserts
that `completePal(S)` is a palindrome, begins with `S`, or is shortest. A name
such as `completePal` supplies no theorem. The independently reconstructed true
domain-lemma set is therefore genuinely empty.

The finite test in `09_summary_differential.py` is supporting sensitivity
evidence, not a universal proof: on all 3,280 sequences over `{0,1,2}` of
length at most seven, the recurrences match a direct source implementation and
an independent shortest-palindrome oracle. Identity-reverse and inverted-search
counterfactuals each disagree on 3,120 cases.
