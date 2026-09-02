# Static rule review record

The machine-generated exhaustive declaration inventory is
`05-rule-inventory.log`. It contains 1,109 declaration records from 26 K source
files: 702 `rule` declarations, 231 `syntax` declarations, 5 contexts, one
configuration, and all imports/modules/claims. It records all attributes,
including 148 `function`, 109 `total`, 45 priority, 36 concrete, 22
`no-evaluators`, 6 macro, and the sole simplification declaration.

Every fixed-semantics record marked
`FIXED_UNUSED_OUTSIDE_DEPENDENCY_SLICE` was inspected as part of its complete
source file and accepted only as an inert part of the supplied definition:
none of its left-hand-side symbols occurs in the submitted program, the three
claims, or a reachable helper term. Function equations in that group cannot
rewrite a term in the proof. `MPY-CONCRETE` is not imported by the Haskell
definition. Records conservatively marked `FIXED_RELEVANT_REVIEWED` were
checked for overlap with the dependency slice; the actual firing slice is
listed below.

## Actual fixed-semantics dependency slice

- `semantics.k`: `MPY` imports the fixed modules; the proof does not import
  `MPY-CONCRETE`.
- `syntax.k`: `Module`, `FuncDef`, `Params`, statement sequencing, `Assign`,
  `For`, `If`, `Expr`, `Return`, `Name`, `Int`, `ListExpr`, `BoolOp`,
  `Compare`/`CmpOp`, `Call`, and `Attribute`. Strictness/context declarations
  evaluate assignment RHS, the iterable once, the condition, return value,
  call callee/arguments, and comparison operands in source order.
- `core.k`: the configuration; `#loadAll` and statement sequencing; scope
  lookup and `builtinsScope`; left-to-right `#evalArgs`; integer literals;
  `#alloc`; and the exhaustive helpers `isRefV`, `appendVal`, and
  `vals2valSeq`.
- `functions.k` and `call.k`: function binding to the exact closure body,
  callee/argument evaluation, parameter binding, frame allocation, return,
  `#endcall`, and frame pop. The builtin-argument dereference priority rules
  expose the result list to `sorted`; mutating-method routing preserves the
  receiver reference for `append`.
- `controls.k`: ordinary local assignment, expression-result discard,
  `If/#branch`, and `For/#loop/#loopStep/#loopLbl`. Their guards and
  priorities are disjoint on the plain non-cell frame used by the claims.
- `tuple.k`: the plain-name `#bindTgt` rule updates `item`. The cell-target
  priority rule is inapplicable because the local scope has no `$cells`
  marker.
- `bool.k`: the head-only context and the true/false `and` rules implement
  left-to-right short circuiting. Here both condition results are Booleans.
- `operators.k` and `list.k`: comparison evaluation; right-reference
  dereference for `item not in result`; list iterator base/step; fresh empty
  list allocation; `valSeqConcat`; in-place `append`; and the
  `#memberAcc/#memberCont/#notB` membership fold. Equal and unequal membership
  guards are complementary. The list-membership rules preempt generic
  comparison dispatch.
- `sort.k`: the unkeyed `sorted` rule allocates a fresh list containing
  `sortVS(VS)`. `sortVS` is the sole reachable opaque fixed-semantics symbol.
  Its concrete integer/string equations are guarded, disjoint, descending
  insertion-sort equations; the symbolic theorem is conditional on the
  supplied primitive's ascending-sort contract.

The other fixed modules (`assert`, general builtins, comprehension, concrete,
dict, float, int arithmetic, range, set, string operations, subscript,
tuple-unpacking, and unused methods) introduce no matching term in the proof.
Generic symbols such as `applyCmp` are also unreachable here because list
membership rewrites directly to `#memberAcc`. All 21 other opaque declarations
are absent from the program and claims.

## Proof-local declaration decisions

- `commonMember` (`verification.k:7-10`) is a definitional summary. Empty and
  cons constructors are disjoint and exhaustive, and recursion is on the
  strict tail. It is connected universally to fixed `#memberAcc` execution by
  the independently closed `member-fold` claim.
- The simplification at `verification.k:14-16` is true on its complete guard:
  `notBool(E ==K V)` makes the left disjunct false, so
  `(E ==K V) orBool B = B`. It has no cells or control effect and no
  conflicting right-hand side.
- `commonAcc` (`verification.k:19-28`) is a definitional summary. Its cases are
  disjoint/exhaustive and recurse on the strict tail of the first sequence.
  Its step exactly mirrors the source branch: append iff the element is in the
  second list and not already in the accumulator.
- `commonLoopBody` and `commonBody` are compile-time macros, not operational
  bridges. Fresh `kast --expand-macros` comparison proves that the complete
  loaded module using `commonBody()` is constructor-identical to the trustedly
  regenerated `solution.mpy`.
- No proof-local priority rule, ordinary operational rule, fresh opaque
  symbol, oracle, or state-abbreviating rewrite exists.

## Claim decisions

- `member-fold` is universal over its value/sequence variables and arbitrary
  continuation/cells. It consumes fixed list iteration and membership control
  and returns exactly `commonMember`.
- `common-loop` pins the unprocessed suffix, second input, accumulator object,
  local bindings, exact return continuation, call frame, allocation counters,
  exception/return state, and exit code. Base reduction is
  `commonAcc(.ValSeq,B,ACC)=ACC`; a cons step executes target binding,
  short-circuited membership, optional append, and recurs on the strict tail.
- `common-program` loads the exact closure body, invokes it through normal
  lookup/call rules, and constrains the returned reference, both heap objects,
  heap counter, scope restoration, empty stack, and normal control state.

No inventoried candidate-local rule admits a false conclusion, so no
unsoundness witness is applicable. The fresh false-result and changed-body
experiments instead confirm discrimination and body sensitivity.
