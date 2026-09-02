# Used constructor and rule map

The submitted `solution.mpy` contains one `Module`, one `FuncDef`, `Params`,
`Return`, nested `BinOp("-")`, `Name`, `Call`, `Attribute`, `Subscript`, and
`Int` constructors. The target starts after module loading at the exact closure
invocation; the fixed `FuncDef` rule is the constructor-level link.

| Constructor/operation | Declaration | Fixed rules used | Audit result |
|---|---|---|---|
| `Module`, statement sequence | `semantics/syntax.k:56-61` | `core.k:124-127` | Module loading is omitted only after the exact `FuncDef`-to-closure link below; no result operation is skipped. |
| `FuncDef`, `Params`, parameter list | `syntax.k:53-60` | `functions.k:14-16` | The rule binds `closureVal(PNS,BODY,L)`. Mechanical comparison found the same name, `("s","n")`, body, and defining environment `0`. |
| `closureVal` invocation/frame | `core.k:25-42`; `functions.k:8-11` | `call.k:69-74`; `functions.k:63-90` | Exact argument binding, new frame, saved continuation, return, frame pop, and restoration execute under fixed rules. |
| `Return` | `syntax.k:50` `[strict]` | `functions.k:78-90` | The expression evaluates before `retV`; `#pop` restores caller control cells. |
| `BinOp("-")` | `syntax.k:15` `[seqstrict(2,3)]` | `operators.k:12`; `int.k:13` | Left-to-right operands cool to values, then integer subtraction is exact. |
| `Name("s"|"n"|"int")` | `syntax.k:12` | `core.k:129-181` | Parameters resolve in the callee frame and `int` falls through to the fixed builtin scope. |
| `Call` and arguments | `syntax.k:28`; `core.k:185-188` | `call.k:20-32`; `core.k:189-191` | Callee then arguments evaluate left-to-right; dispatch distinguishes closure, bound method, and type object. |
| `Attribute(...,"split")` | `syntax.k:29` `[strict(1)]` | `call.k:16` | Receiver evaluates first and becomes a bound method; no textual-name shortcut is present. |
| no-arg `split()` | fixed method symbols | `methods.k:72-86`; `core.k:117-121`; `list.k:18-20` | Fixed recursive whitespace split executes and allocates a real list on each call. |
| `Subscript(...,0|3)` | `syntax.k:22`; `subscript.k:26-29` contexts | `subscript.k:31-41`; `core.k:223-225` | Heap list is dereferenced and both indices are in bounds because the precondition fixes exactly five tokens. |
| `Int(0|3)` | `syntax.k:9` | `core.k:194` | Literal constructor becomes the corresponding K integer. |
| `int(token)` | fixed type/builtin symbols | `call.k:32`; `builtins.k:151-160` | Single- and multi-digit paths compute decimal values; nonempty `allDigit` guards exclude the fixed semantics' invalid-token overbreadth. |
| Input `str(CS)` and token facts | `core.k:13-16,25-42` | `methods.k:75-86,121-138`; `core.k:227-229` | Precondition is satisfiable and defines exact phrase tokens plus arbitrary-length nonnegative ASCII numerals. |

No candidate-local syntax, function, total/functional declaration, opaque
symbol, priority rule, simplification, ordinary semantic rule, or auxiliary
claim exists in `verification.k`.
