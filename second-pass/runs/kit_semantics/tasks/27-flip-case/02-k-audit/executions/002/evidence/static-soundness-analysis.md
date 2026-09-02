# Static soundness analysis

The machine-readable exhaustive ledger is `rule-inventory.tsv`. It inventories
all 26 K source files in the proof closure/source bundle, including
`verification.k` and `spec.k`: 1,096 declarations total, 695 rules, 227 syntax
declarations, five contexts, one configuration, 107 declarations marked
`total`, 146 marked `function`, 45 priority-bearing entries, 36
`concrete`-bearing entries, 25 `symbol` declarations, 22 `no-evaluators`
declarations, no `functional` declarations, no simplification declarations,
and one claim. Each row has a theorem-slice assessment.

## Exact target transition cone

The claim follows this fixed-semantics path:

1. `core.k:125-127` loads and sequences the exact module.
2. `functions.k:14-16` binds `flip_case` to its exact closure in scope 0.
3. `call.k:20-21`, `core.k:131-134`, and `core.k:189-191` evaluate the
   function binding and the already-valued `str(CS)` argument left to right.
4. `call.k:69-74` creates scope 1, pushes the continuation, and executes
   parameter binding via `functions.k:63-66`.
5. In the body, the same lookup rules resolve parameter `string`;
   `call.k:16` creates the bound method; `call.k:20-24` evaluates and
   dispatches the zero-argument call.
6. `methods.k:21` yields `str(mapSwap(CS))`.
7. `functions.k:78-90` records the return, pops the frame, restores scope 0,
   and emits the result to the original continuation.

The destination constrains the result and every active configuration cell:
environment 0, the exact module closure and builtins scopes, scope counter 1,
empty heap with counter 0, empty stack, `noRet`, `NoExc`, and exit code 0.

## Result functions and overlap/coverage

`mapSwap` has exactly two constructor cases (`.IntSeq` and `iCons`), and the
recursive call descends on the tail. `swapC` has disjoint ASCII-uppercase and
ASCII-lowercase guards plus an `owise` complement. `isUpperC` and `isLowerC`
are total integer range predicates. Thus the used equations are terminating,
guard-complete, and pairwise consistent in the supplied IntSeq model. They do
not introduce a fresh or unconstrained value: `mapSwap(CS)` is defined
structurally by the trusted supplied tree.

The operational call rules do not validate arbitrary Python arity or arbitrary
method existence, but the theorem supplies exactly one argument to one
parameter and selects `swapcase` on a primitive `str`. Their complete matched
states on this path agree with the intended binding, evaluation order,
return-control effect, and state footprint. There is no proof-local bridge,
priority rule, function, lemma, summary, oracle, or opaque symbol.

## Unused supplied declarations

All fixed supplied declarations outside the transition cone are itemized in
`rule-inventory.tsv` as unable to match this program state. This includes every
float/sort/MD5 opaque symbol and every priority rule. None can influence the
target result, control, state, or proof closure. `MPY-CONCRETE` is imported only
by `MPY-KRUN`, not by the proof's imported `MPY` module.

The LLVM build reports non-exhaustive-match warnings for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`; none appears in the
target transition cone. The Haskell proof build reports only four unused
variables in unrelated `strLt` branches.

## Supplied model gap

The used `swapC` equations are ASCII-only. For internal code point 233 they
return 233; CPython `str.swapcase()` returns code point 201. This is a concrete
fixed-model-versus-CPython behavior divergence, not a candidate-added rule.
The candidate explicitly records the boundary in its trust ledger, and its
unconstrained `CS:IntSeq` theorem has no further restriction. The submitted
Python function is the same `string.swapcase()` computation as the canonical
implementation and therefore behaves correctly on the Unicode gap.

No proof-local or used fixed-semantics rule was found that permits a false
conclusion on a model-representable target input. The Unicode witness is
classified as the campaign amendment's documented supplied-model gap, not as
an illicit candidate narrowing.
