# Static rule assessment

The exhaustive machine inventory is `05_rule_inventory.txt`: 230 syntax
declarations, 701 rules (463 equational and 238 operational), 45 priority
rules, 35 concrete rules, 25 opaque `symbol(...)` declarations, five
evaluation contexts, four reachability claims, zero explicit simplification
rules, and zero `[functional]` declarations. This assessment covers every
record in that inventory. "Inert" means that neither the submitted program,
the proof-local summaries, nor a reachable continuation has the constructor
needed to match the record; no conclusion about the target theorem depends on
it.

## Complete per-file disposition

| File | Disposition for all inventoried records |
|---|---|
| `semantics.k` | Assembly-only `requires`/imports are complete. `MPY` is the proof module; `MPY-CONCRETE` is imported only by `MPY-KRUN`. Accepted. |
| `syntax.k` | All AST declarations are constructor syntax. The submitted term uses `Module`, `ImportFrom`, `FuncDef`, `Params`, `Assign`, `Name`, `ListExpr`, `For`, `If`, `Expr`, `Call`, `Attribute`, and `Return`; their arities and strictness agree with the translated AST. Other declarations are inert. Accepted. |
| `core.k` | The used configuration, allocation, statement sequencing, name lookup, literal/list helpers, truthiness, and `ValSeq` helpers preserve the relevant cells and follow the supplied subset. Priority-40 cell-reference rules cannot match the plain entry frame. Remaining closure-cell, keyword, operator-dispatch, and sequence helpers are inert. Accepted. |
| `iter.k` | Declaration-only iterator protocol. Used through the list cases. Accepted. |
| `list.k` | The two list iterator rules, `ListExpr` allocation, `valSeqConcat`, and `append` are used and implement head/tail iteration, fresh list construction, sequence concatenation, and one in-place append. List comparison supports the concrete assertions. Deep equality and membership rules are inert in the proof. Accepted. |
| `tuple.k` | Only `#bindTgt(Name(...), V)` is used by the loop and it updates the current scope. Cell-target, tuple construction/comparison, membership, indexing, and unpacking are inert. Accepted. |
| `controls.k` | Used rules are plain-name assignment, non-math `ImportFrom` no-op, expression-result discard, `If`/truthiness, `For` to `#loop`, list iteration stepping, loop continuation, and `If`/`For` heap dereference. They preserve evaluation order and the heap update. Augmented assignment, math import binding, `IfExp`, `While`, and break/continue are inert. Accepted. |
| `functions.k` | Used rules bind the exact function body as a closure, bind two parameters, set the return value, pop the callee frame, restore the caller environment, remove the local scope, and preserve the escaping result heap object. Annotated closures/cells and lambdas are inert. Accepted. |
| `call.k` | Used path evaluates the named callee, then arguments left-to-right, dispatches the exact closure binding, creates a frame, cools `Attribute(ref(0),"append")` as a bound method, and keeps the mutating receiver as a reference. Builtin/type/annotated-closure paths are inert. Accepted. |
| `verification.k` | All six equations are accepted. `intersperseAcc` has disjoint, exhaustive cases for empty remainder, empty accumulator/nonempty remainder, and nonempty accumulator/nonempty remainder; every recursive call strictly removes one remainder element. `intersperseVS` is universally covered. `lastNumber` has disjoint empty/nonempty cases and strictly descends. All three `[total]` declarations are truthful. There is no `<k>` rule or operational bridge. |
| `spec.k` | The three helper claims describe empty-loop termination, first-element establishment, and nonempty-accumulator preservation. Their framed maps are guarded for fresh keys, and each is satisfiable. The entry claim executes the exact module and constrains the return reference, output heap contents, allocation counters, scope, stack, return state, exception, and exit code. Accepted after fresh `#Top`, ground instantiation, constructor identity, body sensitivity, and false-postcondition rejection. |
| `assert.k` | Used only by the independent LLVM harness. True assertions disappear; false assertions set `AssertionError` and exit 1. It is not imported as an extra proof principle. Accepted. |
| `concrete.k` | Concrete-only deep equality and keyed-sort machinery is excluded from the Haskell proof module. The test lists contain no referenced elements, so the deep-equality interception is inactive; keyed sort is absent. Inert for the theorem. |
| `bool.k` | Boolean comparison and `BoolOp` rules do not occur in the submitted program. The program's list truth test uses `core.k` plus the priority dereference in `controls.k`. Inert. |
| `int.k` | Only K integer values occur; no arithmetic/comparison AST node occurs in the submitted body. The equations are constructor/operation-disjoint from the target execution. Inert. |
| `operators.k` | Operator dispatch and dereference rules do not occur in the proof path; list equality occurs only in the LLVM assertion harness and follows the list equality equation. Inert for the theorem. |
| `builtins.k` | The builtin scope is constructed in `core.k`, but the submitted body calls no builtin. All builtin applications, folds, arithmetic evaluator, MD5 interception, and its opaque digest are syntactically unreachable. Inert. |
| `float.k` | All 22 float symbols plus float rules and math-call priority rules require float/math constructors absent from the program, summaries, and postcondition. Inert. |
| `str.k` | Runtime string values and string operations are absent; K `String` tokens used as identifiers are a different sort. Inert. |
| `set.k` | Set constructors never occur. Inert. |
| `range.k` | `rangeObj` never occurs. Inert. |
| `dict.k` | Dict constructors never occur. Inert. |
| `subscript.k` | Subscript/slice constructors never occur. Inert. |
| `comprehension.k` | List-comprehension/generator constructors never occur. Inert. |
| `methods.k` | Only the declaration of method application is on the call route; `append` is handled by the list operational rule. All string/list pure-method equations and split priority rules require absent method names or value constructors. Inert. |
| `sort.k` | `sortVS` and `sortKeyVS` plus all sort rules require `sorted`/`sort` calls absent from the program. Inert. |

## Used execution map

1. `#loadAll` and statement sequencing load the no-op typing import and bind the
   exact `intersperse` closure.
2. Name lookup selects that closure; the call layer evaluates the two arguments
   and creates the callee frame.
3. Empty `ListExpr` allocates heap location 0; plain assignment binds
   `result -> ref(0)`.
4. `For` snapshots the read-only bare input `list(NUMBERS)` and enters
   `#loop`. List iteration and name-target binding consume exactly one source
   element per step.
5. `If(ref(0),...)` dereferences heap 0. It is false only before the first
   append and true thereafter.
6. The uniform call path resolves `result.append`; the list rule appends the
   delimiter only on later iterations and appends the current number on every
   iteration.
7. `Return(Name("result"))` returns `ref(0)` and pops the frame. The postcondition
   requires heap 0 to equal the fully defined `intersperseVS(NUMBERS,D)`.

## Priority, overlap, totality, and opacity

- Every priority rule on the used path is a narrowing of a generic rule:
  `If(ref(...))`/`For(...,ref(...))` dereference heap objects, mutating method
  dispatch keeps the receiver reference, and `append` performs the update.
  Their guards/constructors are disjoint from the corresponding plain-value
  path and preserve the relevant heap and continuation.
- The proof-local equations have no overlap with different right-hand sides,
  are exhaustive over their declared algebraic sorts, and terminate by strict
  structural descent.
- No explicit simplification rule and no `[functional]` declaration exists.
- The 25 opaque symbols are the 22 float symbols, `sortVS`, `sortKeyVS`, and
  `md5hexCodes`. None can occur in a reachable target state or influence the
  result, control, heap, or postcondition.
- I found no rule on the used path that encodes the task answer, intercepts the
  function call/body, fabricates a result, drops a relevant continuation, or
  introduces an unconstrained result-bearing oracle. Therefore there is no
  unsoundness finding requiring a false-conclusion witness.
