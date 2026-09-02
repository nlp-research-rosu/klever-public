# Used-construct and used-rule map

This map is the focused static review of every syntax construct exercised by
the submitted `solution.mpy`, including the direct-entry proof, the loading
claim, and the separate key-closure claims. The exhaustive declaration-level
inventory is `k-inventory.tsv`; `k-rule-assessments.tsv` gives every inventoried
semantic declaration an explicit disposition.

## Syntax-to-semantics map

| Submitted construct | Declaration | Rules used | Audit finding |
|---|---|---|---|
| `Module`, `FuncDef`, `Params`, `Stmts` | `syntax.k:53-61` | `core.k:125-127`; `functions.k:14-16` | Module loading sequences the actual translated body and installs the exact closure at module scope 0. |
| `Return` | `syntax.k:50` (`strict`) | `functions.k:78-90` | The expression is evaluated before `Return(V)` sets `retV(V)`; `#pop` restores the caller environment/stack and preserves heap allocations. |
| `Call` and argument lists | `syntax.k:28,37` | `call.k:20-21`; `core.k:185-191` | Callee evaluates before arguments; arguments evaluate left-to-right; dispatch is on the resolved callable value. |
| `Name("arr")`, `Name("sorted")`, `Name("bin")`, `Name("value")` | `syntax.k:12` | `core.k:131-181` | Lexical lookup walks the active scope then builtins. The initial states pin builtins at scope -1, so `sorted` and `bin` resolve to their supplied builtin values; the function parameters bind in their call frames. |
| `KwArg("key", Lambda(...))` | `syntax.k:25` | `core.k:95-102` | Key expression evaluates to a value before being tagged as `kwV("key", KV)`; the non-keyword guard prevents retagging. |
| Annotated `Lambda(..., CellVars(), FreeVars(), ...)` | `syntax.k:26` | `functions.k:50-60` | Empty free-variable/cell-variable lists deterministically produce the exact `closureValC` named by `popcountKeyClosure`. |
| `IfExp` | `syntax.k:23` (`strict(1)`) | `controls.k:57-60`; `core.k:199-205` | Condition evaluates first and exactly one branch is selected. The `< 0` condition is Boolean, so `truthy` preserves its value. |
| `Compare(..., CmpOp("<", ...))` | `syntax.k:30,32` | `operators.k:15-17`; `int.k:22` | Left then right evaluation is enforced by contexts; integer `<` is ordinary K integer comparison. |
| `Int(0)` | `syntax.k:9` | `core.k:194` | Literal becomes the mathematical K integer 0. |
| `Str("1")` | `syntax.k:13` | `str.k:13-17` | ASCII conversion produces `iCons(49,.IntSeq)`. |
| `Attribute(bin(value), "count")` | `syntax.k:29` (`strict(1)`) | `call.k:16,20-24`; `methods.k:34-44` | Receiver evaluates before method binding; `count` dispatches to the defined non-overlapping substring count recursion. |
| Inner `sorted(arr)` | call syntax above | `call.k:38-46`; `sort.k:18-37`; `core.k:117-121` | The input list is read, summarized by fixed opaque `sortVS(VS)` in the proof backend, allocated at heap location 0, and returned as `ref(0)`. |
| Outer `sorted(ref(0), key=lambda...)` | call/keyword/lambda syntax above | `call.k:38-46`; `sort.k:49,61-62`; `core.k:117-121` | The first argument reference is dereferenced, the exact key closure is evaluated/tagged, fixed opaque `sortKeyVS` is allocated at location 1, and `ref(1)` is returned. |
| Concrete keyed sort | same submitted syntax, LLVM-only main module | `concrete.k:25-59` at priority 40 plus the ordinary closure-call rules | The concrete leg calls the real key closure for each element and performs stable insertion. Reviewer assertions exercise both branches and result ordering. This module is not imported into the Haskell proof. |
| Binary conversion | builtin call syntax | `builtins.k:108-121`; `int.k:19-20` | Non-negative `bin` builds `"0b"` followed by a terminating base-2 recursion; the separate key claim executes this path universally for `N >= 0`. |

## Configuration, order, control, and state

- The initial configuration and every claim pin all cells from
  `core.k:49-60`: `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`,
  `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`.
- Plain and annotated calls use `call.k:69-94`: a fresh scope is allocated,
  arguments are bound, a continuation frame is pushed, and normal return pops
  exactly that frame. The candidate adds no call/return bridge and no abrupt
  control rule.
- Heap allocation is monotone (`core.k:117-121`). The inner sort consumes
  location 0, the outer sort consumes location 1, and function-frame teardown
  does not rewind heap locations. This exactly explains the entry postcondition.
- The generic call rule and builtin fallback are `[owise]`; exact `sorted`
  dispatch rules therefore preempt them. Heap-reference dereference rules have
  priority 40 and preserve every other cell. In the LLVM-only module, the
  concrete keyed-sort rule has priority 40 over the opaque proof summary.
- No candidate-local rule has `priority`, `simplification`, `anywhere`,
  `concrete`, `functional`, `symbol`, or `no-evaluators`. There are no
  candidate-local operational shortcuts, loop claims, or helper claims.

## Candidate-local rule decisions

The nine candidate rules in `verification.k` are all definitional:

1. `sortArrayLambda`, `sortArrayBody`, `sortArrayClosure`, and
   `sortArrayModule` expand to the exact translated program terms.
2. `popcountKeyClosure` is the exact value produced by evaluating that lambda
   with empty free/cell-variable sets.
3. `sortArraySpec` only names the fixed-semantics result term; it does not
   replace execution.
4. `allNonNegativeInts` is structurally recursive. Its empty, integer-cons, and
   `[owise]` non-integer cases are complete and pairwise disjoint.

All seven `[function,total]` declarations therefore have exhaustive equations
over their declared domains. No overlap produces conflicting right-hand sides,
and all recursive calls descend on a sequence tail.

## Opaque boundary

`sortVS` and `sortKeyVS` are the only opaque supplied symbols reached by this
theorem. They are not candidate additions and the result is not a fresh
variable: the postcondition is the fixed term
`sortKeyVS(sortVS(VS), popcountKeyClosure)`. Nevertheless, K does not prove that
these symbols mean stable Python sorting. The intended meaning comes from the
supplied-semantics contract, with finite support from the concrete LLVM leg and
the independent CPython differential test. This is an evidence/intent bridge,
not an operational unsoundness in `verification.k`.

No candidate-local false rule was found. Consequently there is no sound basis
for an unsoundness label or false-conclusion witness; the narrower limitation is
the unproved intended interpretation of the supplied opaque sort primitives.
