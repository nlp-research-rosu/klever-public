# Static soundness review

This document is reviewer-authored. The exhaustive machine-readable inventory
is `rule-inventory.tsv`; its final generator run records 952 entries from all 24
trusted supplied-semantics K files plus `verification.k` and `spec.k`: 708
rules, 235 syntax declarations, 5 evaluation contexts, 1 configuration, and 3
claims. It records every entry's full normalized source, attributes,
classification, reachability status, and assessment. There are no
`functional` or `simplification` attributes. Twenty-two declarations use
`no-evaluators`; all opaque/symbol declarations are in unused float, sort, or
digest functionality and no target claim depends on them.

## Candidate-local declaration and rule decisions

| Location | Declaration/rule | Class and complete domain | Decision |
|---|---|---|---|
| `verification.k:8` | `.Ints`, `intCons(Int, Ints)` | Free constructors for finite integer sequences | Accept. This has no equations and introduces no equality between distinct terms. |
| `verification.k:10` | `intVals(Ints) : ValSeq` | Proof-local symbolic representation constructor | Accept with a limitation: it is a fresh constructor, not an oracle. Its iterator meaning is completely fixed by the next two rules, but the candidate does not contain a machine-checked universal equivalence theorem connecting it to the fixed `vCons/.ValSeq` representation. |
| `verification.k:15` | empty `intVals` iterator | Matches `<k> #iterNext(list(intVals(.Ints))) => #iterDone ... </k>` for every continuation and every setting of omitted cells; priority 40 | Accept. It changes only the head of `<k>`, preserves the complete continuation and every other cell, performs no abrupt control effect, and is the truthful empty-sequence case. Its pattern is disjoint from fixed `list(.ValSeq)` and `list(vCons(...))` cases, so the priority creates no overlap. |
| `verification.k:17` | nonempty `intVals` iterator | Matches `<k> #iterNext(list(intVals(intCons(X,XS)))) => #iterYield(X,list(intVals(XS))) ... </k>` for every `X`, `XS`, continuation, and omitted-cell setting; priority 40 | Accept with the same representation-connection limitation. The rule yields the actual head, structurally decreases the sequence, preserves suffix/control/cells, and is disjoint from both the empty proof-local case and both fixed list rules. It cannot admit an opposite head interpretation. |
| `verification.k:23-29` | `contribution(I,X)` and three equations | All mathematical integers. Guards partition `(I mod 3 == 0)`, `(I mod 3 != 0 and I mod 4 == 0)`, and `(I mod 3 != 0 and I mod 4 != 0)` | Accept. The guards are exhaustive and pairwise disjoint; divisors are positive constants, and each RHS is exactly the square/cube/identity contract branch. |
| `verification.k:32-35` | total `sumSquares` | Both constructors of `Ints`; arbitrary starting index and accumulator | Accept. Constructor coverage is complete, recursion strictly descends through `XS`, and the equation adds exactly one `contribution` before incrementing the index. |
| `verification.k:38-41` | total `endIndex` | Both constructors of `Ints`; arbitrary start index | Accept. Complete, disjoint, strictly descending structural recursion exactly counts iterations. |
| `verification.k:43-46` | total `endValue` | Both constructors of `Ints`; arbitrary old value | Accept. Empty preserves the old binding; nonempty recurses with the current head and thus returns the last bound value. Complete, disjoint, and descending. |
| `verification.k:48-75` | `sumSquaresLoopBody` macro | No runtime rewrite; macro-expands one loop body | Accept. Expanded KAST is constructor-identical to the translated `For` body (`8cc17e...bd2cb` on both sides). |
| `verification.k:77-83` | `sumSquaresFunctionBody` macro | No runtime rewrite; macro-expands the entire function body | Accept. Expanded KAST is constructor-identical to the translated `FuncDef` body (`75bccb...d0d6a5` on both sides), including binding name and sole parameter. |

No candidate-local rule is a simplification, an opaque result source, an
unconstrained oracle, a call interceptor, a direct result rewrite, or a
task-answer axiom. The only operational additions are the two exhaustive rules
for the proof-local sequence representation.

## Reachable fixed-semantics slice

The inventory marks every record in this slice as
`ACCEPT_FIXED_REACHABLE`; all remaining fixed records are marked
`ACCEPT_FIXED_UNUSED`. The unused records cannot be selected from these claims
because their constructors, callable names, value domains, or control markers
do not occur.

| Phase | Fixed declarations/rules followed | State/control review |
|---|---|---|
| Syntax and evaluation order | `syntax.k:9-61`: `Module`, `FuncDef`, `Call`, `Name`, `Int`, `BinOp [seqstrict(2,3)]`, `Compare` plus its two contexts, `Assign [strict(2)]`, `AugAssign [strict(3)]`, `For [strict(2)]`, `If [strict(1)]`, `Return [strict]`, statement/argument/parameter lists | The target's expressions evaluate left-to-right. Its evaluated subexpressions are pure integer/name reads, so no material order is omitted. |
| Call selection and frame entry | `core.k:130-154,185-194`; `call.k:19-21,69-74`; `functions.k:8-11,63-66` | Lookup starts at exact scope 0 and selects the exact `"sum_squares"` closure. The only argument is evaluated and bound to `"lst"`. Call entry allocates scope 1, saves the empty continuation in the frame, and moves `env/scopeLoc/stack` exactly as the body claim states. No problem-local call interception exists. |
| Statement sequencing and locals | `core.k:124-127`; `controls.k:9-23` | The two assignments create integer locals `total=0`, `index=0`. `AugAssign` reads an existing local and applies the integer operator before updating the same local. The target has no heap, allocation, output, or exception side effect. |
| Loop iteration and target binding | `controls.k:65-74,85`; `tuple.k:31-34`; `iter.k:8`; the two candidate `intVals` rules | `For` evaluates its iterable once, `#loop` requests one iterator step, `#bindTgt` updates `"value"`, the body runs, and `#loopLbl` returns to the structurally smaller rest. Empty iteration terminates. All continuation fragments are preserved. |
| Branching and arithmetic | `operators.k:12,15-17`; `int.k:9,14-15,19-20,26`; `core.k:199-205`; `controls.k:51-54` | `%` uses `pyMod` with divisors 3 and 4, `==` returns Bool, truthiness returns that Bool, and `If` selects exactly one branch. Addition and multiplication are unbounded K integers, matching Python integers on the stated domain. The nested second `If` is reached only when the multiple-of-3 test is false, which gives the required precedence at indices divisible by 12. |
| Return and frame restoration | `functions.k:78-90` | `Return(total)` records the value, discards the callee continuation as a Python return should, and `#pop` restores `env=0`, removes scope 1, restores `scopeLoc=1`, empties the stack, and places the value into the caller continuation. All exact main-claim cells are restored; `ret` is reset and `exc/exit-code/heap` remain unchanged. |

The fixed priorities reachable here are cell/ref specializations. The exact
claim uses plain local integers and an unboxed read-only list, so their guards
are false. The candidate iterator priorities match only `intVals` and are
constructor-disjoint from fixed list iteration. There is no reachable
overlap with inconsistent right-hand sides.

## Claim and invariant decisions

The loop claim is a genuine circularity at `#loop`, not a summary rewrite. Its
base case uses the empty iterator rule. Its step case yields the head, executes
the real loop macro, updates `value/total/index`, and returns to the same claim
with `XS`; this is strict structural progress. The exact map pattern records all
four locals and preserves the original `lst`.

The body claim starts after the two initial assignments, uses the separately
proved loop theorem, then executes the real `Return`/frame-pop rules. The main
claim starts at the exact function call and exact binding, uses the separately
proved body theorem, and constrains the result to `sumSquares(IS,0,0)`. No
right-hand-side result variable is free.

## Sensitivity and boundaries

The body-sensitivity mutation changed the square expression in the macro
actually stored in the claimed closure to `value * value + 1`. It compiled,
but the untrusted-free loop proof failed with the expected residual equality

`sumSquares(XS,I+1,ACC+X*X+1) == sumSquares(XS,I+1,ACC+X*X)`.

Thus closure does depend on the real loop operation; changing only
`solution.py` was not used as a sensitivity test.

No false rule was identified. Accordingly there is no claimed unsound rule for
which a false-conclusion witness is required. The one remaining limitation is
an evidence/connection gap, not a known unsoundness: the proof-local `intVals`
representation is informally but not machine-checkingly related to the fixed
concrete `vCons/.ValSeq` representation. Its defining rules are exhaustive and
truthful, and finite concrete/differential evidence agrees, so they do not
enable a known false result on the intended domain.
