# Submitted-program construct map

The source of truth for this table is the regenerated, byte-identical
`solution.mpy`. “Relevant rule” names the fixed supplied-semantics path; line
numbers refer to the scratch copy below `/tmp/audit-work/candidate-src`.

| Submitted construct | Declaration | Relevant fixed rules |
|---|---|---|
| `Module`, statement sequence | `syntax.k:56-61` | `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53-60` | `functions.k:14-16` |
| direct closure entry in claims | `core.k:31`; `functions.k:8-11` | `call.k:69-74`, `functions.k:63-66,78-90` |
| `Assign(Name, ...)` | `syntax.k:41` | `controls.k:9-18` |
| `Name` and builtin lookup | `syntax.k:12`; `core.k:130` | `core.k:131-181` |
| `Str`, internal `str(IntSeq)` | `syntax.k:13`; `core.k:13-15` | `str.k:13-17` |
| `Int` | `syntax.k:9` | `core.k:194` |
| `For` over a string | `syntax.k:45`; `controls.k:65` | `controls.k:69-74`, `str.k:8-10`, `tuple.k:31-41` |
| `Call` and left-to-right arguments | `syntax.k:28`; `core.k:185-188`; `call.k:19` | `call.k:20-32`, `core.k:189-191` |
| `Attribute(..., "swapcase")` | `syntax.k:29` | `call.k:16,24`, `methods.k:21` |
| ASCII case conversion | `methods.k:112-164` | `isUpperC`, `isLowerC`, `swapC`, `mapSwap` equations |
| `ord` / `chr` | builtin bindings at `core.k:165-166` | `builtins.k:143-145` |
| `BoolOp("or", ...)` | `syntax.k:16` | `bool.k:16-25` |
| `Compare(..., "==")` | `syntax.k:30-32` | `operators.k:15-17`, `int.k:26` |
| `If` | `syntax.k:49` | `controls.k:51-54` |
| `BinOp("+", Int, Int)` | `syntax.k:15` | `operators.k:12`, `int.k:9` |
| `AugAssign` of strings | `syntax.k:44` | `controls.k:20-31`, `str.k:20-24` |
| `Return` and restoration | `syntax.k:50` | `functions.k:78-90` |

No submitted construct is serviced by `float.k`, `sort.k`, the MD5 primitive in
`builtins.k`, or another opaque/no-evaluator declaration.
