# Used-construct and control-flow map

The submitted `solution.mpy` uses these AST constructs. This map names the
trusted declaration and the operative fixed-semantics rules in the fresh copy.

| Submitted construct | Declaration | Operative rules and effect |
|---|---|---|
| `Module`, `Stmts` sequencing | `semantics/syntax.k:56,61` | The entry claims start directly at the translated `FuncDef ~> Call`; statement sequencing is `core.k:126-127`. |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16` installs `closureVal(params, exact body, defining env 0)`. |
| `Call(Name("is_sorted"), Name("input"))` | `syntax.k:28` | `call.k:20-21` evaluates callee before arguments; `core.k:131-154` performs scope-chain lookup; `core.k:189-191` evaluates arguments left-to-right; `call.k:69-74` allocates the ordinary call frame. |
| Parameter binding | `functions.k:8-11` | `functions.k:63-66` binds `lst` in the fresh plain frame. The cell-binding priority rule is excluded because the frame has no `"$cells"` marker. |
| `Assign(Name, rhs)` | `syntax.k:41 [strict(2)]` | RHS evaluates first; `controls.k:9-11` writes the current plain scope. Cell-write rule `controls.k:12-18` is guard-inapplicable. |
| `Name` | `syntax.k:12` | `core.k:131-154` walks current frame to its parent; the found binding is returned. Cell lookup priority rule is guard-inapplicable in the plain frame. |
| `Int`, `Bool` | `syntax.k:9,11` | `core.k:194-195` returns the underlying mathematical `Int`/`Bool`. |
| `UnaryOp("-", Int(1))` | `syntax.k:14 [strict(2)]` | `operators.k:10` dispatches after operand evaluation; `int.k:7` yields `0 -Int 1 = -1`. |
| `Compare` and `CmpOp("<"|"=="|">", rhs)` | `syntax.k:30,32` | `operators.k:15-17` evaluates left then right and dispatches; `int.k:22,24,26` implements mathematical integer comparison. Ref-deref priority rules are inapplicable to constrained `Int` operands. |
| `If` | `syntax.k:49 [strict(1)]` | `controls.k:52-54` computes Boolean truth and selects exactly one branch; `core.k:200` makes `truthy(Bool)=Bool`. |
| `AugAssign(Name("repeated"), "+", Int(1))` | `syntax.k:44 [strict(3)]` | `controls.k:20-23` reads and updates the existing integer local after RHS evaluation; `int.k:9` is integer addition. Ref-special rule `controls.k:27-31` is inapplicable. |
| `For(Name("number"), Name("lst"), body)` | `syntax.k:45 [strict(2)]` | `controls.k:69-74` evaluates the iterable once and sequences iteration/binding/body/continuation; `list.k:9-10` yields the head and tail; `tuple.k:31-41` binds the `Name` target in the plain frame. |
| `Return(Bool)` | `syntax.k:50 [strict]` | `functions.k:78-90` discards the active function continuation on early return, records the value, pops/deallocates the frame, restores caller env and location, and resumes with the returned value. |

Evaluation-order and overlap conclusions:

- The strictness declarations give the order needed by this program. Its
  expressions have no side-effecting operands, so the limited Name-target
  `AugAssign` model does not create an order discrepancy on the theorem domain.
- All competing priority rules concern heap `ref` values or annotated closure
  cells. The entry claims provide an unboxed `list(ValSeq)`, the loop elements
  are constrained `Int`, and the call creates a plain frame. Their guards are
  therefore false on the complete target path.
- Integer operator equations are sort-disjoint from Boolean, float, string,
  list, tuple, set, and dictionary cases.
- `Return(V) ~> _ => #pop` correctly implements the program's early returns by
  discarding the remainder of the loop/body while preserving the outer call
  continuation captured in the frame.
- No candidate rule intercepts `Call`, `For`, `Compare`, name lookup, return, or
  frame operations.
