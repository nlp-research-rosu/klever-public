# Stage 5 static soundness review

## Exhaustive inventory scope

`stage5-rule-inventory-v2.tsv` contains one normalized row for every top-level
`syntax`, `configuration`, `context`, `rule`, and `claim` in the 24 byte-checked
supplied-semantics files plus `row-model.k`, `verification.k`,
`shape-connection.k`, and `spec.k`. It contains 956 entries: 712 supplied
and local semantic rules (695 supplied and 17 local), 233 syntax blocks (227
supplied and six local), five contexts, one configuration, and five proof
claims.

For every row whose origin is `SUPPLIED_FIXED`, the inventory decision is
`ACCEPTED_SELECTED_FIXED_SEMANTICS_BOUNDARY`. This is not a claim that the
semantics models all Python: the selected language is explicitly a subset.
Every entry not mapped to `solution.mpy` is inert for this theorem. Every mapped
entry was additionally traced below. No candidate rule was hidden in the
supplied tree: Stage 1 established recursive byte identity.

No declaration in the complete inventory uses `[functional]`. The full lists
of `[total]`, `[priority]`, `[simplification]`, `[concrete]`, `[owise]`,
`symbol(...)`, and `[no-evaluators]` entries are in
`stage5-special-attributes.log`.

## Configuration and used fixed-semantics path

The fixed configuration (`core.k:49`) carries `<k>`, current environment,
scope store and allocator, heap and allocator, call stack, return state,
exception, and exit code. The entry claim fixes every one of these cells.

The submitted constructor path maps as follows.

| Submitted construct / effect | Fixed declaration and rules | Review |
|---|---|---|
| `Call`, left-to-right arguments, keyword tagging | `syntax.k:25,28`; `core.k:94-102,183-191`; `call.k:18-32` | Callee precedes arguments; arguments are accumulated left-to-right; `KwArg` remains tagged. |
| closure call/binding/return | `call.k:69-75`; `functions.k:62-90` | Exact closure body and defining environment are selected; a fresh frame is pushed, parameters bind in order, `Return` sets `retV`, and `#pop` restores the caller continuation/environment. |
| statement sequence, names, literals | `core.k:123-154,193-196` | Statements execute left-to-right; lookup walks the exact scope chain; integer and `None` literals reduce faithfully. |
| assignments and `+=` | `controls.k:8-31`; `int.k:7-17` | Current-frame writes are explicit. Here all augmented assignments are integer `+`, so the exact `+Int` rule applies. |
| list and tuple construction | `list.k:12-20`; `tuple.k:13-18`; `core.k:117-121,183-191` | List literals allocate fresh heap objects; tuple coordinates are values; element evaluation is left-to-right. |
| list iteration and target binding | `controls.k:62-74,104-108`; `list.k:8-10`; `tuple.k:30-46` | The list reference is dereferenced once, `#iterNext` visits each head in order, the name target is rebound, and the body executes before the loop continuation. |
| membership and conditional | `operators.k:14-17`; `tuple.k:18-21`; `list.k:57-67`; `controls.k:50-54` | `(x,)` is evaluated, membership compares the sole element with structural `==K`, and complementary equality guards choose the branch. On the intended integer domain this is exactly `value == x`. |
| `coordinates.append` | `call.k:15-24,52-67`; `list.k:52-55`; `controls.k:46-48` | `Attribute` retains the receiver reference for a mutator, append performs the sole in-place heap update, returns `noneV`, and `Expr` discards it. |
| tuple subscripts and unary minus in keys | `subscript.k:25-41`; `operators.k:10,44-46`; `int.k:7` | The ground two-element tuple indices 0 and 1 reduce in bounds; column negation is `0 -Int CI`. |
| two keyed `sorted` calls and allocation | `core.k:156-181`; `call.k:34-50`; `sort.k:44-66`; `core.k:117-121` | The builtin binding is resolved normally, the input list reference is dereferenced, each call allocates a fresh list, and the symbolic result is the fixed `sortKeyVS` primitive with the evaluated closure as key. |
| concrete keyed sorting | `concrete.k:20-59` (only `MPY-KRUN`) | Each key is obtained by a real call; insertion uses `<` and recurses past equal keys, hence is stable for this program's integer keys. The reviewer LLVM assertions exercised zero, one, repeated, and multi-row matches. |

The fixed `For(T, OBJ, B) => #loop(OBJ,T,B)` rule at `controls.k:69`
already performs the exact transition used by the local bridge. No used fixed
rule fabricates coordinates, bypasses a submitted helper body, or introduces an
unconstrained candidate oracle.

## Opaque and total fixed symbols

The fixed semantics declares opaque float operations, `md5hexCodes`, `sortVS`,
and `sortKeyVS`. Only `sortKeyVS` can influence this theorem. It is declared at
`sort.k:49` as a total, no-evaluator symbol whose documented contract is stable
ascending sort by the supplied callable. The proof does not add equations for
it and therefore cannot prove a false concrete ordering by choosing a
candidate-controlled interpretation. The exact formal result remains
conditional on this fixed primitive's contract. The concrete module implements
the contract for the submitted integer-valued keys, and finite differential
tests support, but do not universally prove, that bridge.

`valSeqAt` is also `[total]` and under-specified out of bounds, but both key
claims index concrete two-element tuples at 0 or 1, so only its ordinary
in-bounds equations apply.

All other opaque symbols and all unused partial/total helper rules are outside
the constructor dependency graph of `solution.mpy`; they cannot affect a
branch, state cell, or postcondition here.

## Local extension inventory and decisions

| Lines | Extension | Class and complete-domain review | Decision |
|---|---|---|---|
| `row-model.k:6,14-15` | `rowContents` | Total definitional projection. The `list(VS)` case returns `VS`; the `[owise]` non-list case returns empty. Cases are disjoint and cover `Val`. It is used only with an explicit list-shape equality guard. | Sound. |
| `row-model.k:7,17-19` | `listRows` | Total structural predicate. Empty is true; the cons case checks the head is exactly a `list` and descends on the tail. | Sound and covers all finite nested lists, without a size bound. |
| `verification.k:21-24` | guarded `For` bridge | Operational bridge. Guard implies `V ==K list(rowContents(V))`; substituting this equality makes its RHS identical to fixed `controls.k:69`. It reads no cell except `<k>`, writes only `<k>`, preserves arbitrary continuation and every omitted cell, and introduces no abrupt control. The bridge-free universal claim has the same guard and arbitrary suffix and closes independently. | Sound; priority only preempts an equivalent fixed step. |
| `verification.k:8,26-28` | `advanceIndex` | Total structural length accumulator. Base returns the accumulator; cons increments once and strictly descends. | Sound; no overlap. |
| `verification.k:6,30-44` | `scanAppend` | Total result summary. Empty returns the accumulator. Cons cases split on `V ==K X` and its Boolean complement; both increment the column and strictly descend. The equal case appends exactly `(RI,CI)`. | Sound; guards are exhaustive/disjoint and RHSs agree with the inner body. |
| `verification.k:7,46-53` | `rowsAppend` | Partial definitional summary. Empty returns the accumulator. A cons whose head is a list invokes `scanAppend`, increments the row, and strictly descends. `listRows` on every use proves coverage; no totality is asserted. | Sound on its complete declared/use domain. |
| `verification.k:55-65` | `INNERBODY` macro | Constructor macro only. `kast` comparison plus the enclosing body comparison shows the exact translated membership, append, and increment sequence. | Sound and semantically inert normalization. |
| `verification.k:66-72` | `OUTERBODY` macro | Constructor macro only; exact translated resets, inner loop, and row increment. | Sound. |
| `verification.k:73-90` | `GETROWBODY` macro | Constructor macro only; its expanded KAST is byte-independent but structurally identical to the trusted-regenerated `get_row` body. | Sound; pins the submitted body. |
| `verification.k:91-96` | `COLUMNCLOSURE` macro | Constructor macro only; parameter list and body exactly match `_column_desc`; defining environment is the module frame 0. | Sound. |
| `verification.k:97-101` | `ROWCLOSURE` macro | Constructor macro only; parameter list and body exactly match `_row_asc`; defining environment is 0. | Sound. |

`scanAppend`, `rowsAppend`, and `advanceIndex` are result-bearing but not
opaque: their equations fix every result on every domain admitted by the proof.
The `inner-loop` and `outer-loop` circularities are bridge-free execution
connections from the exact submitted loop bodies to those summaries.

## Overlaps, priorities, control, and state

- Local guarded equations have disjoint base/cons shapes or complementary
  equality guards. Every recursive call decreases a finite `ValSeq`.
- The only local priority is 40 on the `For` bridge. It competes with the fixed
  `For` rule but has an identical result on its guard.
- Loop claims frame the allocator, stack, return, exception, and exit cells.
  Their bodies invoke no user closure and allocate no object: tuple coordinates
  are values and append mutates only the existing coordinate-list heap entry.
- The entry claim fixes initial heap `.Map` and heap location 0. Exactly three
  allocations occur: the empty coordinate list, first keyed-sort result, and
  second keyed-sort result. It constrains the return to `ref(2)`, fixes all
  three heap contents, advances the allocator to 3, restores the call stack and
  return state, and leaves exception/exit normal.
- Key claims execute the exact helper closures. They are separate supporting
  theorems; because symbolic `sortKeyVS` is opaque, the K backend does not use
  them to unfold sorting. Their connection to the primitive's callable-key
  contract is part of the fixed-semantics trust boundary, not a candidate rule.

## Sensitivity evidence

The bridge-free exact shape claim closes. A one-element mutation that falsely
drops the element fails with a reachable residual
`#bindTgt(T,7) ~> B ~> #loopLbl(...)`, showing the fixed transition does not
admit the wrong loop result. A separate bridge-free context witness executes a
one-element loop, records `"v" |-> 7` in the scope, then preserves and evaluates
an immediate `Int(9)` continuation to `9`; it closes with `#Top`. A material
entry-body mutation removes the append
from the closure term actually bound to `get_row`; execution then returns an
empty list and fails against the nonempty original postcondition.

No local rule is found unsound, so there is no false-conclusion witness to
report against a local extension.
