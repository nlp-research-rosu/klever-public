# Static soundness assessment

This assessment refers to the exhaustive source listing in
`rule_inventory.log` (238 syntax declarations, 715 rules, five contexts, one
configuration, and three claims).  The candidate supplied-semantics tree is not
listed twice because Stage 1 established exact path/type/byte identity with the
trusted tree.  There are no generated helper K files and no candidate
`semantic.k`; the supplied assembly is `reference-semantics/semantics.k`.

## Fixed supplied-semantics modules

Each row classifies every declaration, context, and rule in the named module as
enumerated in `rule_inventory.log`.

| Module | Use in this theorem | Static decision |
|---|---|---|
| `semantics.k` | Imports fixed `MPY`; `MPY-KRUN` additionally imports concrete-only rules | Assembly only; correct dependency split. |
| `syntax.k` | `Module`, `FuncDef`, `Params`, `Expr`, `Str`, `Assign`, `Name`, `Subscript`, `Int`, `For`, `BinOp`, `If`, `Compare`, `CmpOp`, `Return` | Declarations and strictness/context choices give the expected evaluation order. |
| `core.k` | Configuration, module sequencing, literals, name lookup, argument sequencing, values, scopes, `truthy`, list/sequence helpers | Used rules faithfully load and sequence the module, resolve locals before parents, evaluate the integer/string literals, and preserve the configured cells. Cell/keyword/allocation rules are inactive here. |
| `iter.k` | Declares the iterator protocol consumed by `For` | Declaration only; faithful. |
| `range.k` | None | Inactive: no range term is reachable from this program or claim. |
| `operators.k` | `BinOp("+",...)` and `Compare(...,"<",...)` dispatch and operand order | Faithful; left-to-right contexts/strictness precede exact integer operations. Heap-reference cases are inactive because the claim supplies a bare `list(...)` and all elements/locals are integers. |
| `int.k` | Integer addition and less-than | Exact K mathematical-integer operations; other integer operators are inactive. |
| `bool.k` | No `BoolOp`; comparison results pass through core `truthy(Bool)` | All module rules are inactive for the submitted body. |
| `float.k` | None | All 20 opaque/no-evaluator float symbols and every float rule are inactive and cannot influence control or result. |
| `str.k` | Converts the ASCII docstring literal | `strToCodes` structurally converts the literal; the subsequent `Expr` discards it. All string operators/iterators are otherwise inactive. |
| `set.k` | None | Inactive. |
| `list.k` | Fixed list iterator rules underlie the proof-local exact specializations | Empty/cons iterator equations are faithful. Literal allocation, list operations, deep equality, mutation, and membership are inactive. |
| `tuple.k` | `#bindTgt(Name(...),V)` binds the loop variable | The plain-frame binding rule updates only the active local scope. Cell, tuple, unpacking, and tuple-operation rules are inactive. |
| `subscript.k` | Reads `nums[0]` | The proof precondition is non-empty, index is exactly zero, and `valSeqAt` returns the head. The trusted total-but-underspecified out-of-bounds behavior is unreachable. Slice rules are inactive. |
| `comprehension.k` | None | Inactive macros/rules. |
| `methods.k` | None | Inactive. |
| `controls.k` | Assignment, expression discard, `If`, `For/#loop`, and loop continuation | Used rules preserve RHS-first assignment, one-time iterable evaluation, target binding, body execution, and loop continuation. While, imports, cell writes, break/continue, heap dereference, and augmented assignment are inactive. |
| `functions.k` | Exact closure, parameter binding, `Return`, and frame pop | Plain closure path is faithful for this non-escaping top-level function: it allocates a local scope, binds `nums`, evaluates the body, restores the caller, and deletes the local frame. Annotated/nested closure paths are inactive. |
| `builtins.k` | `builtinsScope` is present but no builtin is called | All builtin operations and the opaque `md5hexCodes` symbol are inactive. |
| `call.k` | Direct `#applyK(toCall(closureVal(...)),...)` enters the exact closure | The plain closure rule preserves continuation, caller environment, stack, and fresh scope. Callee-expression, builtin, method, type, annotated-closure, and heap-dereference paths are inactive. |
| `sort.k` | None | Opaque `sortVS`/`sortKeyVS` and all sort rules are inactive. |
| `assert.k` | Concrete reviewer/candidate harness only; absent from the positive claims | Assertion success/failure behaves as the supplied exception subset specifies; it does not help any proof claim. |
| `dict.k` | None | Inactive. |
| `concrete.k` | LLVM harness only; excluded from `MPY` proof definitions | Concrete list-equality/key-sort rules do not enter any Haskell proof. |

No unused fixed-semantics symbol occurs in the submitted constructor term,
entry claims, recursive summaries, or loop bridge.  Thus the fixed opaque
float/sort/digest boundaries cannot constrain a branch, result, state cell, or
postcondition in this theorem.  The compiler's non-exhaustive-totality warnings
also concern unused `mapStrVS`, float, join, and out-of-bounds `valSeqAt` cases.

## Used constructor-to-rule map

| Submitted construct | Declaration and active rule path |
|---|---|
| `Module(FuncDef(...))` | `syntax.k:61`; `core.k` `#loadAll` and statement sequencing; `functions.k` plain `FuncDef` installs the closure. |
| Docstring `Expr(Str(...))` | `syntax.k` `Str`/`Expr`; `str.k` `Str -> str(strToCodes(...))`; `controls.k` discards `Expr(Val)`. |
| `Assign(Name(...), RHS)` | `syntax.k` strict RHS; `controls.k` plain-frame map update. |
| `Name(...)` | `core.k` local-first `#look`; all referenced locals are present, so no parent lookup is needed. |
| `Int(...)` | `core.k` literal rule. |
| `Subscript(Name("nums"),Int(0))` | `subscript.k` contexts, `applyIndex(list(...),0)`, `normIdx`, and head `valSeqAt`; proof-local exact simplification agrees. |
| `For(Name("value"),Name("nums"),body)` | `syntax.k` evaluates the iterable once; `controls.k` creates `#loop`; `list.k` iterator and `tuple.k` name-target binding run each body and continuation. |
| `BinOp("+",...)` | `syntax.k` left-to-right `seqstrict`; `operators.k` dispatch; `int.k` exact `+Int`. |
| `Compare(...,CmpOp("<",...))` | `operators.k` left then right contexts; `int.k` exact `<Int`; core `truthy(Bool)` controls `If`. |
| `If` | `syntax.k` strict condition; `controls.k` `#branch` selects exactly one arm. |
| `Return(Name("smallest"))` | `syntax.k` evaluates the expression; `functions.k` records the value, discards the remaining function body, pops the saved frame, and resumes the exact continuation. |
| Entry `#applyK(toCall(closure),args)` | `call.k` plain-closure rule plus `functions.k` parameter/return rules. |

The body uses a bare immutable `list(intVals(...))`, so no heap allocation,
mutation, output, exception, or external call occurs.  The only changing cells
are the temporary call frame, `env`, `scopeLoc`, `stack`, and its four local
bindings; return restores/deletes all temporary call state.

## Proof-local declarations and rules (`verification.k`)

1. `intVals` empty/cons rules are exact structural embeddings of `IntSeq` in
   `ValSeq`.  Their constructor guards are disjoint and recursion descends.
2. The two priority-30 `#iterNext(list(intVals(...)))` rules are exact
   specializations of the fixed empty/cons list iterator rules after one
   `intVals` unfolding.  Their domains are disjoint and outputs agree with the
   fixed rules on overlaps.
3. The sole simplification,
   `valSeqAt(intVals(iCons(I,R)),0) => I`, is the fixed head-access equation
   after unfolding `intVals`; its non-empty/zero-index guard is syntactic.
4. `chooseSmaller` has disjoint and exhaustive integer guards `A < B` and
   `A >= B`; at equality its second result is equal to the first.  It is exactly
   mathematical minimum.
5. `nextCurrent(I,C)` is definitionally `min(I,C+I)`.
6. The two `kadaneCurrent` equations cover empty/cons sequences, descend on the
   tail, and exactly fold `nextCurrent`.
7. The two `kadaneSmallest` equations cover empty/cons sequences, descend on
   the tail, and update the running best with the new current.
8. `minSubArraySumSpec` intentionally has only the non-empty equation.  Every
   use is syntactically `iCons(H,T)`, so its complete used domain is covered.
9. The two `lastFrom` equations cover empty/cons, descend on the tail, and
   return the last iterated element for every non-empty starting sequence.
10. `kadaneBody`, `minSubArraySumBody`, `minSubArraySumDef`, and
    `minSubArraySumClosure` are syntax macros.  Fresh `kast --expand-macros`
    comparison produced identical KORE for regenerated `solution.mpy` and
    `Module(minSubArraySumDef)` (SHA-256
    `5d2ddbcad87c5128676acf9d66d57b8f73ff6bf0371f2e28edd605abd857ec45`).
11. The sole operational extension is the priority-30 loop summary.  It reads
    `k`, `env`, and the exact plain local frame; consumes only the non-empty
    `#loop`; preserves `nums`, every framed scope entry, every omitted cell, and
    the arbitrary continuation; and updates only `smallest`, `current`, and
    `value`.  `LOOP-SPEC` has the identical full match domain and post-state,
    imports `VERIFICATION-BASE` where the bridge is absent, and freshly closed
    with `#Top`.

The bridge has no fresh or opaque result.  Its three result-bearing summaries
are fixed by terminating equations and by the bridge-free universal
`LOOP-SPEC`; therefore their occurrence in `FUNCTION-SPEC` is not an oracle or
circular value assumption.

## Operational and value sensitivity

- An observable `Assign(Name("after"),Int(99))` placed immediately after the
  loop closed under both the bridge-free base definition and the bridge-enabled
  definition.  Both require final `smallest=-2`, `current=-2`, `value=-2`, and
  `after=99` for input `[1,-2]`.
- A body mutation changed the executed macro from `current + value` to
  `current - value`.  Macro-expanded KORE changed from SHA-256
  `5d2d...ec45` to `6c13...b31b`; the bridge-free universal loop theorem then
  failed with `WarnStuckClaimState`.
- The satisfying ground mutation witness `input=[1]`, `C=0`, `B=1` reached
  `current=-1, smallest=-1`, while the original summary demanded
  `current=1, smallest=1`.  Its proof failed with the exact terminal
  configuration in `stage5_body_mutation_ground_kprove.log`.

No false proof-local rule was found, so there is no candidate-unsoundness
witness to report.  The remaining limitation is adequacy: the formal
postcondition defines the Kadane recurrence but does not itself quantify over
all contiguous index intervals.  The recurrence-to-natural-language bridge is
ordinary mathematics and strongly tested, but remains informal rather than a
second K theorem.
