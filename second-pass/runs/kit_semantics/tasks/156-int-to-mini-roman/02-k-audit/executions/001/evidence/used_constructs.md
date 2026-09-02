# Used-constructor and rule-path map

The constructor set is mechanically read from the trusted regeneration
`/tmp/audit-work/rebuild/regenerated.mpy`. The active source term contains
`Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Subscript`, `TupleExpr`,
`Str`, `BinOp`, `Int`, `If`, `Compare`, `CmpOp`, and `Return`.

| Constructor/operation | Declaration | Rules used |
|---|---|---|
| `Module` and statement list | `syntax.k:56,61` | `core.k:124-127` loads and sequences the module |
| `FuncDef`, `Params` | `syntax.k:53,57` | `functions.k:14-16` installs the closure in scope 0 |
| `Assign(Name, ...)` | `syntax.k:41` | strict RHS evaluation, then `controls.k:9-11` writes the current scope |
| `Name` | `syntax.k:12` | `core.k:131-154` walks the current/parent scope; all lookups here hit a concrete binding |
| `Int` | `syntax.k:9` | `core.k:194` produces a K `Int` |
| `Str` | `syntax.k:13` | `str.k:13-17` produces an ASCII `IntSeq`; all literals here are ASCII |
| `TupleExpr` | `syntax.k:21` | `tuple.k:14-16` and `core.k:183-191,213-219` evaluate left-to-right and build `tuple(ValSeq)` |
| integer `%`, `//` | `syntax.k:15`; dispatch `core.k:209` | `operators.k:12`; `int.k:15-20`; divisors are the ground nonzero values 1000, 100, 10 |
| `Subscript` | `syntax.k:22` | contexts `subscript.k:27-28`, dispatch at 35, tuple indexing at 37-40, length at `core.k:223-225`; each ground index is 0..9 into a ten-element tuple |
| integer `==` | `Compare`/`CmpOp` at `syntax.k:30,32` | left-to-right contexts `operators.k:15-17`; `int.k:26` |
| `If` | `syntax.k:49` | strict condition plus `controls.k:51-54`; only input 1000 takes the true arm |
| string `+` | `syntax.k:15`; dispatch `core.k:209` | `operators.k:12`; `str.k:20-24`; evaluation is left-to-right from `seqstrict(2,3)` |
| `Return` | `syntax.k:50` | strict expression evaluation then `functions.k:78-90`, which records the value, discards only the remaining callee body, restores the stored caller continuation/environment, and deletes the callee scope |
| `Call` harness | `syntax.k:28` | `call.k:18-21,69-74`; evaluates binding and argument, allocates a concrete callee frame, binds `number`, and stores the exact caller continuation |

The program performs no list allocation, heap mutation, loop, exception,
float, dict, set, sort, comprehension, method, builtin, import, I/O, or opaque
operation. The final claims constrain `.K`, both scopes, both allocators, the
heap, stack, return state, exception state, environment, and exit code.
