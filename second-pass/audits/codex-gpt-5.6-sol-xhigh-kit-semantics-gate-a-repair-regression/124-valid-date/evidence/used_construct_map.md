# Submitted-AST construct map

All locations below are in the clean scratch copy of the byte-identical supplied
semantics.

| Submitted construct | Declaration | Execution/equation rules used |
|---|---|---|
| `Module` | `semantics/syntax.k:61` | `semantics/core.k:124-127` sequences `#loadAll` and statements |
| `FuncDef`, `Params`, `ParamNames` | `semantics/syntax.k:53,57,60` | `semantics/functions.k:14-16` binds the closure in module scope |
| `Call` | `semantics/syntax.k:28` | `semantics/call.k:20-21` evaluates callee then arguments; `core.k:185-191` evaluates arguments left-to-right; `call.k:69-74` enters a user-function frame |
| `Name` | `semantics/syntax.k:12` | `semantics/core.k:130-154` performs lexical/builtin lookup; `core.k:157-181` defines the fixed builtin frame |
| `If` | `semantics/syntax.k:49` (`strict(1)`) | `semantics/controls.k:51-54` dispatches on `truthy` |
| `Return` | `semantics/syntax.k:50` (`strict`) | `semantics/functions.k:78-90` records the value, discards the function suffix, restores caller state, and deletes the callee scope |
| `Assign(Name, ...)` | `semantics/syntax.k:41` (`strict(2)`) | `semantics/controls.k:9-11` writes the current callee scope |
| `Int`, `Bool`, `Str` | `semantics/syntax.k:9,11,13` | `semantics/core.k:194-195`; `semantics/str.k:13-17` converts the ASCII `"-"` literal |
| `Compare`, `CmpOp` | `semantics/syntax.k:30,32` | `semantics/operators.k:15-17` evaluates left then right and dispatches; `semantics/int.k:22-27` and `semantics/str.k:25-26` supply the used comparisons |
| `BoolOp("or", ...)` | `semantics/syntax.k:16` | `semantics/bool.k:16-25` evaluates left-to-right and short-circuits with Python value-returning behavior; all submitted operands are Booleans |
| `BinOp` | `semantics/syntax.k:15` (`seqstrict(2,3)`) | `semantics/operators.k:12` dispatches after left-to-right evaluation; `semantics/int.k:9,13-14` supplies `+`, `-`, and `*` |
| `Subscript` | `semantics/syntax.k:22,38` | `semantics/subscript.k:27-41` evaluates object then index, normalizes the nonnegative index, and returns a one-code string |
| builtin `len` | fixed builtin binding in `semantics/core.k:157-181` | generic call routing in `semantics/call.k:31`; `semantics/builtins.k:20-26`; `semantics/core.k:227-229` |
| builtin `ord` | fixed builtin binding in `semantics/core.k:157-181` | generic call routing in `semantics/call.k:31`; exact one-code equation at `semantics/builtins.k:143` |
| `solutionProgram` | `verification.k:10` | sole equation at `verification.k:12-104`; independently pinned to the regenerated program |
| `dateCodes` | `verification.k:109-111` | sole constructor equation at `verification.k:112-114` |
| `validDate10` | `verification.k:116-118` | sole Boolean equation at `verification.k:119-129` |
| `monthDayOK` | `verification.k:131` | sole Boolean equation at `verification.k:132-147` |

The submitted program contains no loop, comprehension, collection allocation,
mutation, method call, exception construct, floating-point operation, opaque
operation, or proof-local operational bridge. Function entry temporarily
allocates scope location 1; parameter binding and the ten local assignments
write only that scope. Return deletes it and restores environment 0, scope
location 1, the empty stack, `noRet`, empty heap/heap-location 0, `NoExc`, and
exit code 0. Module loading adds `valid_date` to scope 0, which is why the final
scope map is existentially framed in both claims.
