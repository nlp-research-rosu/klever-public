# Used construct map

The submitted `solution.mpy` uses the following source constructors. All
declaration/rule locations below are in the byte-identical supplied semantics
tree copied to `/tmp/audit-work/audit-src/reference-semantics`.

| Submitted construct | Syntax declaration | Fixed-semantics execution path | Candidate-proof treatment |
|---|---|---|---|
| `Module` | `semantics/syntax.k:61` | `semantics/core.k:124-127` loads and sequences module statements | Not used by any entry claim; `solution.mpy` is never loaded |
| `FuncDef`, `Params` | `semantics/syntax.k:53-60` | `semantics/functions.k:14-16` installs the closure | Bypassed; `runGrades` directly constructs a `closureVal` around a copied macro body |
| `Assign`, `Name` | `semantics/syntax.k:12,41`; `semantics/controls.k:9-18`; `semantics/core.k:130-154` | Strict RHS evaluation, scope write, and lexical lookup | The duplicated body executes these fixed rules |
| `ListExpr` | `semantics/syntax.k:17`; `semantics/list.k:13-15` | Left-to-right element evaluation and heap allocation | The duplicated body executes these fixed rules |
| `Int`, `Float` | `semantics/syntax.k:9-10`; `semantics/core.k:193-196`; `semantics/float.k:21` | Literal becomes a K numeric value | Fixed rule |
| `For` | `semantics/syntax.k:45`; `semantics/controls.k:65-74` | Iterator protocol followed by target bind, body, and loop label | Real concrete lists use `semantics/list.k:9-10`; the universal claim instead uses proof-local `numericValues` bridges at `verification.k:86-97` |
| `Call` | `semantics/syntax.k:28`; `semantics/call.k:19-32` | Callee then arguments are evaluated; closure call is `semantics/call.k:69-75` | `runGrades` invokes a copied-body closure through this path |
| `float(...)` | builtins binding `semantics/core.k:157-181`; type-call routing `semantics/call.k:32`; conversion `semantics/float.k:185-187` | Int grades convert with `intToF`; Float grades are unchanged | Fixed supplied primitive; universal input datatype restricts values to Int/Float |
| `If` | `semantics/syntax.k:49`; `semantics/controls.k:51-54` | Condition truthiness selects exactly one branch | Fixed branch rules, but the equality condition is preempted by `verification.k:72-75` |
| `Compare`, `CmpOp` | `semantics/syntax.k:30-32`; evaluation contexts and dispatch `semantics/operators.k:14-20` | Float equality is `semantics/float.k:43`; greater-than routes to `gtF` at `semantics/float.k:125-129` | `>` remains conditional on fixed `gtF`; `== 4.0` is replaced by unconstrained `gpaEqFour` |
| `Attribute`, method call | `semantics/syntax.k:29`; `semantics/call.k:16,20-24` | Attribute becomes a bound method, then call dispatches | Fixed |
| `list.append` | `semantics/list.k:53-55` | In-place heap append and returns `noneV` | Fixed |
| `Str` | `semantics/syntax.k:13`; `semantics/str.k:13-16` | Converts the literal to character codes | Fixed; `letter` duplicates the same representation |
| expression statement `Expr` | `semantics/syntax.k:52`; `semantics/controls.k:48` | Discards the method-call result | Fixed |
| `Return` | `semantics/syntax.k:50`; `semantics/functions.k:78-90` | Stores return value, pops frame, restores continuation/state | Fixed |

No candidate-local simplification rules or `[functional]` declarations exist.
All 29 proof-local rules and all 11 proof-local syntax declarations are
individually adjudicated in `rule-inventory.csv`; the JSON form also preserves
each complete declaration block.
