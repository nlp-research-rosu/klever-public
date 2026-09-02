# Construct-to-semantics map for `solution.mpy`

All cited fixed-semantics items are in `stage5-rule-inventory.md` and are
byte-identical to the trusted supplied semantics.

| Submitted construct | Declaration/evaluation path | State/control conclusion |
|---|---|---|
| `Module`, statement list | `syntax.k:56,61`; K-0324 through K-0326 (`#loadAll`, head sequencing, empty sequence) | Loads the submitted statement sequence without substitution. |
| `FuncDef`, `Params` | `syntax.k:53,57`; K-0565 | Installs `closureVal` containing the literal submitted body in module scope 0. |
| `Name` | `syntax.k:12`; K-0328/K-0329 plus parent lookup | Resolves locals first, then the module and fixed builtins scope. Thus `is_sorted`, `lst`, `result`, `current`, and `sorted` use their pinned bindings. |
| `Call` | `syntax.k:28`; K-0195 and the left-to-right argument loop K-0336 through K-0338 | Evaluates callee before arguments and dispatches on the resolved value. |
| User-function call | K-0212 plus K-0580/K-0582 | Allocates the exact local scope, binds `lst`, pushes the exact continuation, executes the body, sets the return cell, pops the frame, removes the local scope, and restores the caller. |
| `Assign` | `syntax.k:41 [strict(2)]`; K-0248 | Evaluates the right side first and updates only the named local binding. |
| Integer/Boolean literals | `syntax.k:9,11`; K-0339/K-0340 | Produce mathematical K `Int` and K `Bool`; no bounded-machine overflow exists. |
| `Compare`, `CmpOp` | `syntax.k:30,32`; evaluation contexts plus K-0739 | Evaluate left then wrapped right operand and dispatch by operator string. |
| List equality in `result = lst == sorted(lst)` | right-ref dereference K-0745, then K-0610 | The unboxed input `list(INPUT)` is compared structurally with the heap value returned by `sorted`, yielding `INPUT ==K sortVS(INPUT)`. |
| Builtin `sorted(lst)` | builtin binding in `core.k:157-181`; first-argument dereference K-0205 when needed; K-0785; allocation K-0322 | Calls the selected external builtin and allocates exactly one fresh `list(sortVS(INPUT))` at heap slot 0. Symbolic `sortVS` is intentionally opaque in the Haskell proof (K-0773); K-0775 onward supplies insertion sort only for concrete execution. |
| `For(current, lst, body)` | `syntax.k:45 [strict(2)]`; K-0266 through K-0269; list iterator K-0601/K-0602; target binding K-0918; initial ref dereference K-0284 if needed | Evaluates the iterable once, visits every element in order, binds `current`, executes the literal body, and resumes with the tail. |
| `Attribute(lst, "count")` | `syntax.k:29 [strict(1)]`; K-0193 | Produces a bound method only after evaluating `lst`. |
| `lst.count(current)` | method dispatch K-0197; non-mutating receiver/argument dereference K-0210 and adjacent call rules; K-0666 through K-0670 | Counts occurrences by exact K equality over the full input sequence. On the formal entry domain `current` is an `Int`, so no heap-reference ambiguity is reachable. |
| Integer `> 2` | K-0596 | Uses mathematical integer greater-than. |
| `If` | `syntax.k:49 [strict(1)]`; K-0259 through K-0262 | Evaluates the condition, executes only the selected branch, and assigns `false` exactly when count exceeds 2. |
| `Return(result)` | `syntax.k:50 [strict]`; K-0580 then K-0582 | Evaluates the real local result, performs the actual return/pop control effect, and restores every caller cell fixed in the claims. |

## Reachable priority and opaque boundaries

- Reachable priority rules only select faithful heap dereference before generic
  dispatch: list comparison, non-mutating call arguments/receivers, loop-start
  dereference, and cell-aware alternatives. No candidate added or changed any
  priority rule.
- Of the supplied semantics’ 22 `no-evaluators` declarations, only `sortVS` is
  reachable. All float, keyed-sort, and MD5 opaque symbols are off path.
- The compiler’s non-exhaustive-total warnings (`mapStrVS`, `floorFI`, `toF`,
  `ceilF`, `joinCodes`, and `valSeqAt`) are all off path for this submitted AST
  and formal integer-list domain.
- There are no exceptions, output, I/O, mutation of the input list, or
  additional allocations along the claimed path. The claims nevertheless pin
  all ten configuration cells.
