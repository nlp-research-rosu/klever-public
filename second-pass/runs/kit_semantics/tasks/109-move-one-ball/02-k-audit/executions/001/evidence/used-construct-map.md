# Used-constructor and rule map

This map is reviewer-authored. Paths are relative to
`/tmp/audit-work/problem-109-independent`.

| Submitted constructor / effect | Declaration | Rules that execute it in the proof import closure |
|---|---|---|
| `Module` | `reference-semantics/semantics/syntax.k:61` | `core.k:124-127` loads and sequences statements |
| `FuncDef`, `Params`, closure binding | `syntax.k:53,57`; `core.k:31` | `functions.k:14-16` binds the exact parameter/body/defining-scope closure |
| `Call`, argument list | `syntax.k:28`; `core.k:185-188` | `call.k:20-21,69-74`; `core.k:189-191`; `functions.k:63-66,78-90` evaluate the callee and arguments left-to-right, create/bind/pop the frame, and restore the caller |
| `Name` lookup | `syntax.k:12`; `core.k:130` | `core.k:131-154` walks the scope chain; the exact plain local frame takes the direct lookup rule |
| `If` | `syntax.k:49` with strict condition | `controls.k:51-54`; `core.k:199-205`; `bool.k:8` evaluates `not arr` through list truthiness and selects one branch |
| `Return` | `syntax.k:50` with strict expression | `functions.k:78-90` records the result, discards the remaining callee body, pops the exact frame, and restores the caller |
| `Bool`, `Int` literals | `syntax.k:9,11` | `core.k:194-195` |
| `Assign(Name, value)` | `syntax.k:41` with strict RHS | `controls.k:9-18`; on the exact plain frame the ordinary map update applies |
| `Subscript(list, 0)` | `syntax.k:22`; `subscript.k:27-28` contexts | `subscript.k:35,37-39`; `normIdx` at `21-23`; `vsLen` at `core.k:223-225`; in-bounds `valSeqAt` at `subscript.k:11-14` |
| `For` over a bare `list(VS)` | `syntax.k:45` with strict iterable | `controls.k:65,69-74`; list iterator `list.k:9-10`; name-target binding `tuple.k:31-41` |
| `BinOp("+", ...)` | `syntax.k:15` with `seqstrict(2,3)` | `operators.k:12`; integer plus integer/Boolean `int.k:9-12` |
| `Compare("<", ...)`, `Compare("<=", ...)` | `syntax.k:30,32`; contexts `operators.k:15-16` | dispatch `operators.k:17`; fixed integer cases `int.k:22-27`; the two guarded proof-local symbolic sort-refinement equations at `verification.k:39-42,60-63` |
| Input `list(VS)` and list iteration | `core.k:18,25-34` | direct bare-list iterator `list.k:9-10`; no heap allocation, mutation, or opaque sort is used |
| Configuration, scopes, stack, return, exception and exit state | `core.k:49-60` | call/frame rules above plus ordinary assignment/lookup rules; the entry claim fixes every material initial cell |

The submitted term contains no float, string, dict, set, comprehension, sort,
method, mutation, exception-producing assert, import, or opaque-symbol
operation.
