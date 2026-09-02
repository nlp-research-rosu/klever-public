# `solution.mpy` construct-to-semantics map

This map is based on the byte-identical trusted retransliteration recorded in
`02_translate_identity.log`. Line references below are to the scratch copy,
which is byte-identical to the candidate's supplied-semantics tree.

| Submitted construct | Declaration | Fixed behavior used by real module execution | Use in submitted claims |
|---|---|---|---|
| `Module(Stmts)` | `semantics/syntax.k:61` | Configuration and `#loadAll`, `semantics/core.k:49-60,124-127` | **Bypassed**; no claim starts from `#loadAll(Module(...))`. |
| `FuncDef`, `Params` | `semantics/syntax.k:53,57` | Function binding, `semantics/functions.k:14-16` | **Bypassed**; the claim's scope has no `triples_sum_to_zero` binding. |
| statement sequencing | `semantics/syntax.k:56` | `semantics/core.k:125-127` | Used inside the manually embedded closure body. |
| `For` | `semantics/syntax.k:45` (`strict(2)`) | iterator loop, `semantics/controls.k:65-74`; list/range iteration in `list.k:9-10`, `range.k:20-24` | Used for all three copied loops. |
| `Name` | `semantics/syntax.k:12` | scope-chain lookup, `semantics/core.k:130-154` | Used for `l`, loop indices, `range`, and `len`. |
| `Call` | `semantics/syntax.k:28` | callee then left-to-right arguments, `semantics/call.k:19-32` and `core.k:185-191` | Used inside the copied body; normal call of the submitted named function is bypassed. |
| `len` | builtin binding in `semantics/core.k:157-181` | `semantics/builtins.k:20-26` | Computes list length for each range bound. |
| `range` | builtin binding in `semantics/core.k:157-181` | `semantics/builtins.k:176-180`, `range.k:9-24` | Produces the three index ranges. |
| `BinOp("+",...)` | `semantics/syntax.k:15` (`seqstrict(2,3)`) | dispatch `operators.k:12`; integer addition `int.k:9` | Computes `i+1`, `j+1`, and the triple sum. |
| `Subscript` | `semantics/syntax.k:22` | left-to-right contexts and list indexing, `subscript.k:27-41`; `valSeqAt`, `subscript.k:11-14` | Reads the three indexed integer elements. Range construction keeps indices in bounds. |
| `Compare(...,"==",0)` | `semantics/syntax.k:30,32` | evaluation contexts/dispatch `operators.k:14-17`; integer equality `int.k:26` | Selects the early-`True` branch. |
| `If` | `semantics/syntax.k:49` (`strict(1)`) | truthiness/branch, `controls.k:51-54` | Executes the early return exactly when the integer equality is true. |
| `Return` | `semantics/syntax.k:50` (`strict`) | return and frame pop, `functions.k:77-90` | Returns `true` early or `false` after all loops. |
| `Bool` | `semantics/syntax.k:11` | literal reduction, `core.k:193-196` | Supplies the two possible results. |

The proof-only `#runTriples` declaration/rule is at `verification.k:29-61`.
It creates `closureVal(...)` directly and calls it with `list(VS)`. The rule
copies the submitted function body accurately, but it neither parses/loads
`solution.mpy` nor executes `FuncDef` binding and `Name`-based dispatch.
