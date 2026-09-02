# Used-construct map

The locations below refer to the scratch copy at
`/tmp/audit-work/candidate/reference-semantics`.

| Submitted construct | Declaration | Executing rules and audit result |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `semantics/syntax.k:53,57,61` | `semantics/core.k:125-127` loads/sequences the module; `semantics/functions.k:14-16` installs the closure in scope 0. |
| `Call(Name("next_smallest"), ...)` | `semantics/syntax.k:12,28` | `semantics/call.k:20-21` evaluates callee before arguments; `semantics/core.k:189-191` evaluates arguments left-to-right; `semantics/call.k:69-74` allocates the function scope and pushes the exact continuation frame. |
| `Name` | `semantics/syntax.k:12` | `semantics/core.k:131-154` performs lexical lookup through the current scope and parents. The target proof begins with the expected module/builtins scopes. |
| `Assign(Name, expr)` | `semantics/syntax.k:41` (`strict(2)`) | RHS evaluates before `semantics/controls.k:9-11` updates the current scope. Cell-write priority rules are disjoint because this function has no `$cells` marker. |
| `Int`, `NoneVal` | `semantics/syntax.k:9,27` | `semantics/core.k:194,196` produces unbounded K integers and `noneV`. |
| `For` | `semantics/syntax.k:45` (`strict(2)`) | `semantics/controls.k:69-74` evaluates the iterable once, requests the next item, binds the target, executes the body, and loops. The proof-only `intVals` iterator equations in `verification.k:58-62` exactly mirror `semantics/list.k:9-10` for `.ValSeq`/`vCons`. |
| Loop target binding | `semantics/tuple.k:31` | `semantics/tuple.k:32-34` updates `value` in the current function scope before executing the body. |
| `If` | `semantics/syntax.k:49` (`strict(1)`) | `semantics/controls.k:52-54` evaluates only the condition and selects exactly one branch using `truthy`. |
| `Compare` and `CmpOp` | `semantics/syntax.k:30,32` | `semantics/operators.k:15-17` evaluates left then right; `semantics/int.k:22-27` implements the used `==`, `!=`, and `<` comparisons over unbounded integers. |
| `BoolOp("or", ...)` | `semantics/syntax.k:16` | `semantics/bool.k:16-25` evaluates the head first and short-circuits with Python's value-returning semantics. Here the operands are booleans, so it supplies the intended guard. |
| `Return` | `semantics/syntax.k:50` (`strict`) | `semantics/functions.k:78-90` records the value, discards the remaining callee continuation, restores caller control and environment, deletes the callee scope, and resets `scopeLoc`. `#endcall` returns `noneV` only on fallthrough. |

No submitted term uses allocation, mutation, exceptions, I/O, floats, strings,
sorting, dictionaries, comprehensions, slicing, imports, assertions, opaque
digest operations, or any supplied `no-evaluators` symbol. Those declarations
remain in the exhaustive inventory because the fixed semantics imports them,
but their left-hand patterns are disjoint from every reachable term of this
program.
