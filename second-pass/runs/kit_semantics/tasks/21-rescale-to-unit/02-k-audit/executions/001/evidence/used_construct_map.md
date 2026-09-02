# Used constructor-to-semantics map

All paths are relative to `/tmp/audit-work/proof`.

| Submitted constructor/operation | Declaration | Executing/defining rules |
|---|---|---|
| `Module`, statement sequence | `reference-semantics/semantics/syntax.k:56-61`; `core.k:124` | `core.k:125-127` (`#loadAll`, head sequencing, empty sequence) |
| Initial configuration/cells | `core.k:25-42` | `core.k:49-60`; `builtinsScope` at `core.k:157-181` |
| `ImportFrom("typing","List")` | `syntax.k:41-54` | non-math import is the `[owise]` no-op at `controls.k:36` |
| `FuncDef`, `Params`, closure binding | `syntax.k:53-60`; `core.k:31` | `functions.k:14-16` |
| User-function call and parameter binding | `syntax.k:28`; `call.k:19`; `functions.k:8-11` | callee/arguments left-to-right at `call.k:20-21` and `core.k:189-191`; closure frame at `call.k:69-74`; bind at `functions.k:63-66` |
| `Name` lookup for function, argument, locals, and builtins | `syntax.k:12`; `core.k:130` | `core.k:131-154`; builtin frame at `core.k:157-181` |
| `Assign(Name(...), ...)` | `syntax.k:41` (`strict(2)`) | `controls.k:9-18` |
| `min(numbers)` / `max(numbers)` routing | `call.k:29-30`; builtin fold declarations at `builtins.k:75-94`; float fold declarations at `float.k:243,250` | builtin routing at `call.k:29-30`; initial iterator at `builtins.k:77,87`; float seed/step/done at `float.k:244-255`; list iterator at `list.k:9-10` |
| Empty `ListExpr` result allocation | `syntax.k:17`; `list.k:13` | argument evaluation at `list.k:14`; fresh heap allocation at `list.k:15` and `core.k:117-121` |
| `Subscript(numbers, Int(0))` | `syntax.k:22,38-39`; `subscript.k:11,21,37` | evaluation contexts at `subscript.k:27-28`; dispatch/indexing at `subscript.k:35,38`; `valSeqAt`/`normIdx` at `subscript.k:12-23`; integer literal at `core.k:194` |
| `For(Name("number"), numbers, BODY)` | `syntax.k:45`; `controls.k:65-67`; target binder at `tuple.k:31` | strict iterable evaluation from syntax; enter/step/done at `controls.k:69-74`; list iteration at `list.k:9-10`; target write at `tuple.k:32-41` |
| `Expr(Call(Attribute(result,"append"),...))` | `syntax.k:29,52`; `methods.k:10`; call dispatch at `call.k:24` | attribute cooling at `call.k:16`; append heap write/`noneV` at `list.k:53-55`; expression result discard at `controls.k:48` |
| Nested `BinOp("-",...)` then `BinOp("/",...)` | `syntax.k:15` (`seqstrict(2,3)`); dispatch at `core.k:209` | generic dispatch at `operators.k:12`; float subtraction/division at `float.k:103-109`; guarded dynamic subtraction twin at `verification.k:34-37` |
| `Return(Name("result"))`, frame pop | `syntax.k:50`; `functions.k:8-11` | return and return state at `functions.k:78-81`; frame restore/pop at `functions.k:85-90` |
| Result-list accumulation | `list.k:18` | actual append uses `valSeqConcat` at `list.k:53-55`; proof summary uses the identical operation at `verification.k:89-108` |

The proof-only declarations and rules are all in `verification.k`; the complete
inventory and per-record decision are in `rule_inventory.tsv`.
