# Submitted-program construct and rule map

The mechanically regenerated program uses only the following `.mpy`
constructors:

- `Module`, `FuncDef`, `Params`, `Name`, `Assign`, `Int`, `Str`, `For`,
  `If`, `Compare`, `CmpOp`, `AugAssign`, and `Return`, plus the generated
  `Stmts`, `Exprs`, and `ParamNames` list forms.
- At runtime these introduce the internal forms `#loadAll`, `#look`,
  `#callee`, `#evalArgs`, `#applyK(toCall(closureVal(...)))`, `#bindP`,
  `#loop`, `#iterNext`, `#iterYield`, `#loopStep`, `#bindTgt`, `#branch`,
  `applyCmp`, `applyBin`, `#loopLbl`, `#pop`, and `frame`.

The declarations and rules are:

| Program operation | Declaration/evaluation source | Material behavior checked |
|---|---|---|
| AST and statement lists | `semantics/syntax.k:9`, `:32`, `:37`, `:41`, `:56`, `:57`, `:60`, `:61` | `BinOp` is left-to-right `seqstrict`; assignment, augmented assignment, iterable, condition, and return expression carry the needed strictness. |
| Initial state and module loading | `semantics/core.k:49`, `:124-127` | Fresh module/builtin scopes and empty heap/stack/return/exception cells; `#loadAll` executes each exact statement in order. |
| Values and scopes | `semantics/core.k:13-42` | Strings are finite `IntSeq`s, integers/Booleans are values, and the submitted closure is `closureVal(params, body, defining-scope)`. |
| Name lookup | `semantics/core.k:130-154` | Lookup starts at `<env>` and selects the first binding. The submitted plain frames contain no `$cells`, so cell-only priority rules cannot match. |
| Argument order | `semantics/core.k:185-191`, `:213-215` | The callee is evaluated before arguments; the single argument is evaluated and appended left to right before dispatch. |
| Integer literals and truthiness | `semantics/core.k:193-205` | `Int(I)` becomes `I`; comparison returns a Boolean and `truthy(Bool)` is that Boolean. |
| String literal and iteration | `semantics/str.k:8-17` | ASCII literal conversion maps `"["`, `"]"`, and `""` to codes 91, 93, and empty; iteration yields one-character strings left to right and terminates at empty. |
| Comparison dispatch and order | `semantics/operators.k:14-17` | Contexts evaluate comparison left operand, then wrapped right operand, then dispatch. No reference-dereference priority rule can match. |
| Integer operations | `semantics/int.k:9`, `:22`, `:26` | `state += 1`, `state < 2/4`, and `state == 4` use ordinary mathematical integers. |
| String equality | `semantics/str.k:25` | The one-character loop value compares structurally against the literal code sequences. |
| Plain assignment and augmented assignment | `semantics/controls.k:9-31` | The current plain local map is updated; reference/cell alternatives are ruled out by the exact frame and value sorts. |
| Conditional control | `semantics/controls.k:50-60` | The guard is evaluated once; exactly the true or false branch executes. |
| For-loop control | `semantics/controls.k:62-75`, `:84-91` | Iterable is evaluated once, each yield binds the target then executes the body, and `#loopLbl` resumes with the exact remaining iterator. There is no abrupt control in the body. |
| Loop target binding | `semantics/tuple.k:30-41` | `Name("bracket")` updates the current plain local map. The closure-cell rule is inapplicable. |
| Function definition/call/return | `semantics/functions.k:8-20`, `:62-90`; `semantics/call.k:15-32`, `:69-75` | Loading binds the exact body, normal lookup chooses it, the call allocates a plain child frame, the sole parameter is bound, `Return` sets `<ret>`, and `#pop` restores the caller and continuation. |

No list, tuple-value, dict, set, range, subscript, comprehension, method,
builtin, floating-point, sorting, import, assertion, exception, heap,
closure-cell, `break`, `continue`, or `while` rule is reachable from the target
program. `MPY-CONCRETE` is absent from the Haskell proof module; it was used
only for the separate LLVM smoke execution.

## Proof-local declarations and rules

`verification.k` adds exactly four total functions and ten equations:

| Symbol | Equations | Review |
|---|---:|---|
| `nestedStep(Int,Int)` | 5 | The guards partition all integers into `S<2`, `2<=S<4`, and `S>=4`; the first two regions partition on the relevant code equality. The right sides exactly match the two nested Python tests and integer increment. |
| `nestedScan(IntSeq,Int)` | 2 | Empty is the identity; constructor consumes one head and recursively processes the strict tail. Exhaustive, disjoint, terminating. |
| `bracketInput(IntSeq)` | 2 | Empty is accepted and each constructor requires code 91 or 93 plus the recursive tail. Exhaustive, disjoint, terminating. |
| `nestedResult(IntSeq)` | 1 | Exactly `nestedScan(CS,0) ==Int 4`; it does not rewrite any Python term. |

There are no proof-local priority, simplification, `[concrete]`, `[owise]`,
opaque/no-evaluator, macro, or operational-bridge rules.

## Claims

- `SPEC.loop` symbolically executes the fixed `#loop` with the exact target and
  body. It changes only local `state` and `bracket`, preserves `string`, frames
  the continuation and all other cells, and summarizes the state as
  `nestedScan(CS,S)`. Its bounds are inductive because `nestedStep` maps
  `0..4` to `0..4`.
- `SPEC.program` executes `#loadAll` of the mechanically identical submitted
  module, calls the selected binding, and requires all finite codes to be 91
  or 93. Its Boolean destination is constrained by
  `RESULT ==Bool nestedResult(CS)`.

No rule in the supplied or proof-local source bears a `[simplification]` or
`[functional]` attribute. The source inventory records every `[function]`,
`[total]`, `[concrete]`, `[priority]`, `[owise]`, macro, and
`[no-evaluators]` occurrence. All opaque supplied symbols are on constructs
unreachable from this program and cannot influence its branch, value, state,
exception, or postcondition.
