# Submitted-program construct and rule map

The regenerated `solution.mpy` uses only `Module`, `FuncDef`, `Params`,
`Assign`, `Name`, `Int`, `While`, `Compare`, `CmpOp`, `BinOp`, and `Return`.
The entry claim additionally uses `Call` to invoke the loaded binding.

| Constructor/control | Declaration | Execution rules on the proof path |
|---|---|---|
| `Module` / statement list | `semantics/syntax.k:60-62` | `core.k:124-127` loads and left-to-right sequences statements |
| `FuncDef` / `Params` | `semantics/syntax.k:54-59` | `functions.k:14-16` installs `closureVal(PNS,BODY,L)` in the current scope |
| `Call` | `semantics/syntax.k:29` | `call.k:20-21` evaluates callee then arguments; `call.k:69-74` allocates the exact user frame and pushes its continuation |
| parameter binding | internal declarations `functions.k:8-11` | `functions.k:63-66` binds the one formal to the one evaluated argument |
| `Assign` | `semantics/syntax.k:43` with `[strict(2)]` | K-generated strictness evaluates the RHS first; `controls.k:9-11` updates the current plain scope |
| `Name` | `semantics/syntax.k:10` | `core.k:130-154`; on this path `core.k:131-134` finds each local or module binding |
| `Int` | `semantics/syntax.k:7` | `core.k:194` yields a K mathematical integer |
| `BinOp` | `semantics/syntax.k:12` with `[seqstrict(2,3)]` | `operators.k:12` dispatches after left-to-right operands; `int.k:9` and `int.k:13` perform integer addition/subtraction |
| `Compare` / `CmpOp` | `semantics/syntax.k:20-22` | contexts `operators.k:15-16` evaluate left then right; `operators.k:17` dispatches; `int.k:24` implements `>` |
| `While` / internal `#while` | `semantics/syntax.k:47`; internal declaration `controls.k:65-67` | `controls.k:77-82` evaluates the guard and chooses body/exit; `controls.k:85` resumes the next iteration |
| truth of comparison | `core.k:199` | `core.k:200` maps the comparison's Bool result to itself |
| `Return` | `semantics/syntax.k:50` with `[strict]` | K-generated strictness evaluates `a`; `functions.k:78-90` records the result, discards the remaining callee body, pops the exact saved frame, restores caller state, and places the value before the saved continuation |
| initial builtins scope | `core.k:157` | `core.k:158-181`; the `"fib"` lookup is resolved in module scope before this root is consulted |

Sequential statement semantics is material: after `b = a + b`, the next
statement reads the updated `b`, so `a = b - a` computes the previous `b`.
The proof-local simplification in `verification.k:24` expresses exactly the
integer identity needed to recognize that state transition.

The K compiler generates the heat/cool rules implied by `[strict]` and
`[seqstrict]`; those generated rules are part of the compiler/backend trust
boundary rather than candidate-authored proof extensions.
