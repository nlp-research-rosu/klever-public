# Submitted construct-to-semantics map

The submitted MPY uses `Module`, `FuncDef`, `Params`, `Assign`, `Name`,
`Call`, `If`, `Compare`, `CmpOp(">")`, `Return`, `Subscript`, `Slice`,
`NoBound`, `UnaryOp("-")`, `Int`, and `BinOp("+")`. The claims begin at the
`Call`, with the exact loaded closure already installed, so module loading and
`FuncDef` execution are not on the claim path.

| Submitted construct/behavior | Declaration | Reached fixed-semantics rules |
|---|---|---|
| AST sorts and strictness | `syntax.k:9-61` | Generated heating/cooling enforces unary strictness, binary left-to-right order, assignment RHS evaluation, `If` condition evaluation, and `Return` expression evaluation. |
| Call and arguments | `core.k:185-191`, `call.k:19-21` | Resolve the callee, evaluate arguments left-to-right, then dispatch. |
| User-function frame | `call.k:69-74`, `functions.k:63-66,78-90` | Allocate a child scope, bind `x` and `shift`, run the actual body, set `retV`, restore the caller state, and return the value. |
| Name lookup/builtins | `core.k:130-181` | Local lookup finds parameters/`s`; parent lookup finds `str` and `len` in `builtinsScope`. |
| `s = str(x)` | `controls.k:9-11`, `call.k:31-32`, `builtins.k:148` | Integer conversion yields `str(strToCodes(Int2String(x)))`, then assignment updates only the callee scope. |
| `len(s)` | `builtins.k:20-25`, `core.k:227-229` | String length is the recursive `isLen` of its code sequence. |
| `shift > len(s)` | `operators.k:14-17`, `int.k:22-27` | Operands evaluate left-to-right; integer greater-than yields a Boolean. |
| `if` | `controls.k:50-54`, `core.k:199-205` | Boolean truthiness selects exactly one branch. |
| Unary negation | `operators.k:10`, `int.k:7` | `-I` becomes `0 -Int I`. |
| Slices | `subscript.k:26-69,71-121` | Base and bounds evaluate in order; CPython-style start/stop adjustment and `buildIS` produce the selected string code sequence. |
| String concatenation | `operators.k:12`, `str.k:20-24` | `seqConcat` appends suffix codes to prefix codes. |
| Return/control | `functions.k:77-90` | `Return(V)` discards the remaining function-body continuation, records `V`, pops exactly one saved frame, and restores all framed cells. |

No rule in `verification.k` matches `Call`, `Return`, a function frame, or any
configuration cell. Thus no proof-local operational bridge skips assignment,
branching, slicing, concatenation, or return. The only proof-local
simplification is the exact-pattern decimal-code abstraction documented in the
rule assessment.
