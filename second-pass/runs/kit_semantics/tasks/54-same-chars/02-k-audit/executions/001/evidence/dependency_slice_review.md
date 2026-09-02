# Static dependency-slice review

This document records the reviewer’s decisions over the broad source inventory
in `rule_inventory.tsv`. The complete inventory has 1,209 declaration records:
695 rules, 227 syntax declarations, one configuration, five contexts, one
claim, and module/import/require boundaries. There are no `[functional]` or
`[simplification]` declarations. The 22 `no-evaluators` declarations are
listed in `opaque_inventory.tsv`; none occurs in the target dependency slice.
All 45 priority-bearing declarations are listed in `priority_inventory.tsv`.

## Proof-local theory

`verification.k` contributes no syntax, function, equation, totality
declaration, simplification, priority, rewrite, opaque symbol, or helper claim.
It requires the trusted `semantics.k` file and imports `MPY`. `spec.k`
contributes only `SPEC.same-chars`. The source inventory’s four
`verification.k` records are therefore module plumbing, not proof extensions.

`MPY-CONCRETE` is not imported by `MPY` or `VERIFICATION`. The fresh Haskell
definition’s `allRules.txt` has zero records from `semantics/concrete.k`, so its
LLVM-only deep-equality and keyed-sort rules cannot affect the proof.

## Used syntax and semantics mapping

| Constructor in the executed term | Declaration | Evaluation |
|---|---|---|
| `Module`, `Stmts` | `syntax.k:56-61` | `core.k:124-127` loads and sequences statements |
| `FuncDef`, `Params` | `syntax.k:53-60` | `functions.k:14-16` binds the exact body as a closure |
| `Assign(Name(...), ...)` | `syntax.k:41` (`strict(2)`) | `controls.k:9-11` evaluates RHS then updates current scope |
| `Return` | `syntax.k:50` (`strict`) | `functions.k:78-90` records the value, pops, restores the caller and allocation counter |
| `Call`, `Name` | `syntax.k:12,28` | `call.k:20-21`, `core.k:130-181`, `core.k:186-191`, and `call.k:69-74` resolve the binding, evaluate arguments left-to-right, and invoke it |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:15-17` evaluates left then right and dispatches equality |
| symbolic `str(IntSeq)` values | `core.k:12` | Already values; the theorem does not rely on ASCII-only `Str` literal parsing |
| `set(str)` | builtin binding at `core.k:157-181` | `call.k:31` and `builtins.k:41` compute `setV(dedupCodes(...))` |
| set equality | `set.k:8` | `set.k:11-39` computes mutual membership |

## Rule-family decisions

1. **Initial state and module flow — sound.** The claim starts from the fixed
   configuration values in `core.k:49-60`. `#loadAll` exposes the module’s
   statement list; the two sequencing rules execute the `FuncDef` before the
   harness assignment. They preserve every non-`k` cell.

2. **Binding and lookup — sound on the complete matched domain used here.**
   `FuncDef` stores `closureVal(params, body, 0)` in module scope. The harness
   looks up that exact name in scope 0. Function-local `s0`/`s1` resolve in
   scope 1; `set` falls through scope 1, then scope 0, to the fixed `-1`
   builtin scope. The priority-40 cell lookup/write variants require a
   `"$cells"` entry, which neither frame contains; their guards are false and
   they do not overlap the selected plain-frame behavior.

3. **Evaluation order and call lifecycle — sound.** `Call` evaluates the
   callee before its argument list. `#evalArgs` consumes the expression list
   left-to-right and `appendVal` preserves order. The closure call allocates
   scope 1, binds both arguments, pushes the exact continuation, and executes
   the body. `Return` discards only the remainder of that function body,
   records the value, and `#pop` restores module environment 0, deletes the
   callee scope, empties the frame stack, resets `scopeLoc` to 1, and resumes
   the assignment. No exception, heap, or output cell is abstracted.

4. **Builtin dispatch — sound and binding-pinned.** The `set` name is obtained
   from `builtinsScope`, not recognized textually by a proof-local shortcut.
   Neither argument is a heap `ref`, so the priority-40 dereference variants
   do not match. The generic builtin dispatch then reaches the exact
   `applyBuiltin("set", str(CS), .Vals)` equation. Special call interceptors
   for math/hash operations have different constructor heads and cannot
   preempt these calls.

5. **Comparison order and dispatch — sound.** The two contexts evaluate the
   left `set` call and then the right call. Both results are bare `setV`
   values, so ref-dereference priority rules do not match. The generic
   comparison route reaches the sort-specific set-equality equation.

6. **Set functions — sound, total on their declared algebraic inputs, and
   terminating.** `codeIn` is ordinary membership. `dedupFrom` consumes one
   input constructor on every recursive call; its `codeIn` and `notBool
   codeIn` guards are disjoint and exhaustive. `snocCode` consumes its list.
   `subsetCodes` consumes its left list. `sameSet` is mutual subset. These
   equations exactly characterize equality of the distinct integers in two
   finite `IntSeq`s, independent of order or multiplicity. They contain no
   opaque value and no oracle.

7. **Result assignment and final cells — sound.** `Assign` writes the computed
   Boolean to `"result"` in restored module scope 0. The cell-write priority
   rule is disabled by the absent `"$cells"` marker. The claim observes `.K`,
   environment, both scopes, both allocation counters, heap, stack, return
   state, exception state, and exit code, so no material active cell is
   omitted.

## Remaining inventory

Every row marked `TRUSTED_SUPPLIED_BASELINE_UNREACHED` has a constructor head,
sort, builtin/method name, operator, or control form absent from every
reachable target state. This includes float, sort, MD5, list/dict/tuple,
subscript, loop, comprehension, method, assert, and concrete-execution
families. No target state contains an unconstrained `Val` that can be narrowed
to those constructors: both inputs are specifically `str(IntSeq)`, both set
calls return specifically `setV(IntSeq)`, and the final comparison returns a
`Bool`.

Those rows are accepted only as the supplied fixed-semantics boundary; this
audit does not claim they form a complete CPython semantics. No concrete or
symbolic witness on the intended two-string input domain makes one of those
rules apply or lets it support a false target conclusion. The exact per-row
disposition and text remain in `rule_inventory.tsv`, while all opaque and
priority subsets are separately preserved.
