# Used `.mpy` construct map

All paths below are relative to `/tmp/audit-work/reconstruction`. The submitted
term uses only the following language path:

| Construct | Declaration | Evaluation/control rules |
|---|---|---|
| `Module` / statement list | `reference-semantics/semantics/syntax.k:56-61` | `core.k:124-127` |
| `FuncDef`, `Params`, closure | `syntax.k:53-60`, `core.k:31` | `functions.k:14-20` |
| `Expr` docstring statement | `syntax.k:52` | `controls.k:46-48` |
| `Str` / string value | `syntax.k:13`, `core.k:13-15` | `str.k:13-17` |
| `Name` | `syntax.k:12` | `core.k:129-181` |
| `Int` | `syntax.k:9` | `core.k:193-196` |
| `Compare`, `CmpOp`, integer `<` | `syntax.k:30-32` | `operators.k:14-17`, `int.k:22` |
| `If` | `syntax.k:49` (`strict(1)`) | `controls.k:50-54` |
| `Assign(Name, ...)` | `syntax.k:41` (`strict(2)`) | `controls.k:8-18` |
| `BinOp` integer/string `+` | `syntax.k:15` (`seqstrict(2,3)`) | `operators.k:12`, `int.k:9`, `str.k:20-24` |
| `Call` and left-to-right args | `syntax.k:28` | `call.k:18-32`, `core.k:183-191` |
| user closure call/frame | `core.k:31`, `functions.k:8-11` | `call.k:69-74`, `functions.k:62-90` |
| builtin `range` | `core.k:167`, `core.k:185` | `builtins.k:176-180`, `range.k:9-24` |
| builtin/type `str(int)` | `core.k:180`, `call.k:32` | `builtins.k:147-149`, `str.k:13-17` |
| `For`, binding, iterator protocol | `syntax.k:45`, `controls.k:65-67`, `iter.k:8` | `controls.k:69-74`, `tuple.k:30-41`, `range.k:20-24` |
| `Return` / frame pop | `syntax.k:50`, `functions.k:8-11` | `functions.k:77-90` |

Important pinning result: the entry claims begin at `Call(...)` with a
manually seeded `closureVal`; they do not begin at `#loadAll($PGM)` and neither
the proof `kompile` nor `kprove` command names `solution.mpy`.
