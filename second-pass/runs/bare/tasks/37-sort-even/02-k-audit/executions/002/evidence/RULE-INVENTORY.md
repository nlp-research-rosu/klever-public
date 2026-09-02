# Exhaustive local rule inventory

Line references are to the clean scratch sources copied from `/candidate`.
Imported K domains are recorded as a trust boundary, not expanded as local
rules.

## Syntax, configuration, and declarations

- `semantic.k:9-35` declares `Module`, statement lists, `FuncDef`, `Return`,
  `If`, parameters, expression lists, `Int`, `Name`, `ListExpr`, `BinOp`,
  `Compare`, `Subscript`, `Slice`, `Call`, comparison lists/operators, bounds,
  and runtime `pyInt`, `pyBool`, and `pyList`.  Every constructor in
  `solution.mpy` is in this list; `pyBool` is declared but no final boolean
  value is used by this program.
- `semantic.k:48-52` has exactly two state cells: `<k>` and immutable
  `<program>`.  The submitted program is pure, so no heap, output, or mutable
  state cell is required.
- `semantic.k:54-70` declares the continuation/control constructors used by
  the evaluator: `run`, function application/lookup, `exec`, `eval`,
  conditional continuation, list concatenation continuations, comparison
  continuations, index/slice continuations, call-argument continuations, and
  list-literal continuations.  `comparison` is an intermediate `PyVal`.
- `semantic.k:71-75` declares four local functions. `findFunction` and `bind`
  are ordinary partial K functions. `dropList` is `[function,total]`.
  `headInt` is `[function,total,smtlib(headInt)]`.  The latter has only a
  nonempty integer-headed equation, and clean LLVM compilation warns that it
  is non-exhaustive.
- `verification.k:7` declares the nullary function `solutionProgram`.
  `verification.k:68-73` declares the six ordinary proof-side functions
  `evenPositions`, `oddPositions`, `insertReference`, `sortReference`,
  `rebuildReference`, and `sortEvenReference`.
- There are no local `[functional]`, `[simplification]`, `[concrete]`,
  priority, `owise`, or simplifier rules in any candidate K file.  There are
  no local opaque result symbols other than the uncovered applications of
  `headInt`.

## `semantic.k`: all 39 rules

| Line | Rule | Classification and decision |
|---:|---|---|
| 77 | `dropList(L,0) => L` | Trusted-helper wrapper; true for the used zero start. |
| 78 | positive `dropList` via `range/minInt/size` | Trusted-helper wrapper; correctly drops a clamped positive prefix. Used only at 1 and 2. It has no negative case despite `[total]`; that is an unused coverage gap. |
| 80 | integer-headed `headInt` | Trusted primitive over K lists; correct on nonempty raw-integer lists. The missing empty/non-integer cases conflict with `[total]` and are material outside the integer fragment. |
| 82 | `run` calls `"sort_even"` | Operational semantics; selects the submitted entry name. |
| 84 | `applyFunction` finds a definition in `<program>` | Operational semantics; preserves the continuation and reads, but does not change, the program cell. |
| 86 | `applyFound` executes the body under `bind` | Operational semantics; correct for the exact arities in the submitted module. |
| 88 | matching `findFunction` | Definitional lookup; correct for the unique submitted names. |
| 90 | nonmatching `findFunction` recursion | Definitional lookup; guard is disjoint from line 88 and descent is structural. |
| 94 | empty parameter/value binding | Definitional binding; correct. |
| 95 | recursive parameter/value binding | Definitional binding; correct for unique parameters and exact arities. |
| 98 | `Return` evaluates its expression and discards following statements | Operational control rule; correct Python return behavior. |
| 99 | `If` evaluates its guard before selecting a branch | Operational control rule. It discards the statement suffix, which is safe for this submitted program because every `If` is the complete function body and every branch returns. It is not a reusable full-Python rule. |
| 101 | integer equality true branch | Operational branch; guard is sound. |
| 103 | integer equality false branch | Operational branch; disjoint and exhaustive with line 101 for integers. |
| 105 | integer `<=` true branch | Operational branch; guard is sound. |
| 107 | integer `<=` false branch | Operational branch; `>` is disjoint and exhaustive with line 105 for integers. |
| 110 | integer literal evaluation | Operational expression rule; exact. |
| 111 | name lookup | Operational expression rule; exact for the uniquely bound submitted variables. |
| 112 | list-literal evaluation start | Operational expression rule; delegates left-to-right evaluation. |
| 113 | list `+` evaluation start | Operational expression rule; evaluates left before right. |
| 115 | list `+` right-operand continuation | Operational evaluation-order rule; preserves the left value. |
| 117 | list concatenation | Operational value rule; correct for two `pyList` values. |
| 119 | equality comparison start | Operational expression rule; covers the only equality form used. |
| 121 | `<=` comparison start | Operational expression rule; covers the only ordering form used. |
| 123 | comparison right-operand continuation | Operational evaluation-order rule; preserves the left value and operator. |
| 125 | comparison with the evaluated empty-list literal | Operational value rule; correctly tests whether the original list has size zero for the submitted `X == []` forms. |
| 127 | integer equality result | Operational value rule; preserves operand order, which is immaterial for equality. |
| 128 | integer `<=` result | Operational value rule; reconstructs original left/right order correctly. |
| 130 | integer index evaluation start | Operational expression rule. |
| 132 | positive start-only slice evaluation start | Operational expression rule; exactly covers `[1:]` and `[2:]`. |
| 135 | index result via `pyInt(headInt(dropList(...)))` | Operational value rule. Correct only for a valid index into a raw-integer list. Its unguarded match fabricates an integer-typed result for non-integer elements and does not model `IndexError`; see the witness below. |
| 137 | start-only slice result | Operational value rule; correct for nonnegative starts used by the program. |
| 139 | named function-call evaluation | Operational expression rule; exact for every submitted call target. |
| 142 | completed argument list applies function | Operational control rule; exact. |
| 143 | next call argument | Operational evaluation-order rule; left-to-right. |
| 145 | completed argument continuation | Operational evaluation-order rule; appends in source order. |
| 148 | completed list literal | Operational value rule; exact. |
| 149 | next list item | Operational evaluation-order rule; left-to-right. |
| 151 | completed integer list item | Operational value rule; exact for the integer fragment, but deliberately cannot preserve a non-integer item. |

The integer-fragment rules have no overlap contradiction. Recursive functions
descend by one or two list elements. Function lookup descends through module
definitions. Control and argument/list evaluation are left-to-right, and there
is no state or exception cell to preserve.

## `verification.k`: all 13 rules

| Line | Rule | Classification and decision |
|---:|---|---|
| 8 | `solutionProgram()` equation | Definitional source embedding, not an execution shortcut. Independent parsing/evaluation comparison shows it is the submitted constructor term. |
| 75 | empty `evenPositions` | Definitional summary; true. |
| 77 | nonempty `evenPositions` | Definitional summary; true on raw-integer lists and descends by two. |
| 81 | `oddPositions` | Unused definitional summary; correctly drops one then selects every second position. |
| 83 | empty `insertReference` | Definitional insertion; true. |
| 85 | front-insertion branch | Definitional insertion; true when `X <= head`. |
| 88 | recursive-insertion branch | Definitional insertion; complementary integer guard and structural descent. |
| 94 | empty `sortReference` | Definitional insertion sort; true. |
| 96 | recursive `sortReference` | Definitional insertion sort; structural descent. |
| 100 | empty-source `rebuildReference` | Definitional rebuild; true for the top-level reachable relation. |
| 102 | singleton-source `rebuildReference` | Definitional rebuild; true when an even value exists. An empty `EVENS` argument exposes opaque `headInt(.List)` rather than Python `IndexError`; helper claim scope is overbroad. |
| 105 | multi-element `rebuildReference` | Definitional rebuild; copies the odd-position source value and descends by two/one. It likewise assumes enough `EVENS`. |
| 111 | `sortEvenReference` | Definitional composition: extract even positions, insertion-sort them, and rebuild around original odd positions. It does not replace operational execution. |

There are no proof-local ordinary operational rules, lemmas, priorities, or
simplification equations.  The ten `spec.k` declarations are reachability
claims/circularities, not semantic equations.  `sort-correct` depends on
`insert-correct`; `top-correct` depends on `even-correct`, `sort-correct`
(therefore `insert-correct`), and `rebuild-correct`.  Each dependency was
reproved with the necessary closure.

## Construct mapping

| Submitted constructor | Declaration/rules |
|---|---|
| `Module`, `FuncDef` | `semantic.k:9,12`; function lookup at 84, 88, 90 |
| `Params`, `Name` | declarations at 16, 21; binding/lookup at 94-96, 111 |
| `If`, `Return` | declarations at 13-14; control at 98-108 |
| `Int`, `ListExpr` | declarations at 20, 22; evaluation at 110, 112, 148-152 |
| `BinOp("+",...)` | declaration at 23; left-to-right evaluation/concat at 113-117 |
| `Compare`, `CmpOp("=="/"<=")` | declarations at 24, 28-29; evaluation/branching at 101-108, 119-128 |
| `Subscript(...,Int(0/1))` | declaration at 25; evaluation at 130-135 |
| `Subscript(...,Slice(Int(1/2),NoBound,NoBound))` | declarations at 25-26,30; evaluation at 132,137 |
| `Call(Name(...),...)` | declaration at 27; argument evaluation/call at 139-146 |

## Concrete false-behavior witness and narrower gaps

`["b", "odd", "a"]` satisfies the prompt's written `list` contract and both
Python implementations terminate with `["a", "odd", "b"]`.  In the generated
semantics, line 135 always wraps an indexed element as `pyInt` and obtains it
through `headInt`; line 151 likewise accepts only `pyInt` list-literal items.
Fresh LLVM execution exits 113 at:

```text
headInt ( ListItem ( "b" ) ListItem ( "odd" ) ListItem ( "a" ) )
```

Thus the model neither preserves the string element nor reaches the Python
result.  This is a concrete source-domain witness for the integer-only semantic
restriction.  It is not evidence that the integer-fragment equations are
inconsistent.

Other gaps are narrower and off the submitted entry's integer paths:
negative `dropList` starts have no equation; out-of-range indexing and too-short
`EVENS` do not raise Python exceptions; missing function names and arity
mismatches get stuck; and an `If` with a fall-through suffix would be modeled
incorrectly.  None occurs while `sort_even` executes on a raw-integer list.
