# Submitted MPy construct-to-semantics map

The submitted `solution.mpy` contains no loops, collections, imports, floats,
builtins, opaque symbols, allocation, or exceptions. Its constructor set and
the complete paths exercised by the target claims are:

| MPy form | Declaration | Evaluation/control rules |
|---|---|---|
| `Module(Stmts)` | `reference-semantics/semantics/syntax.k:62` | `#loadAll(Module(SS)) => SS` and statement sequencing in `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53-61` | closure installation in the current module scope, `functions.k:14-16` |
| `Call(Name("solve"), N)` | `syntax.k:30` | callee lookup and left-to-right argument evaluation in `call.k:19-21`, `core.k:185-191`; closure frame push in `call.k:69-76` |
| `Name` | `syntax.k:10` | lexical lookup from `<env>` through `<scopes>` in `core.k:130-155` |
| `Assign(Name, Expr)` | `syntax.k:38` with strict RHS | current-frame map update in `controls.k:9-12` |
| `AugAssign(Name, "+", Expr)` | `syntax.k:41` with strict RHS | reads the existing current-frame binding and applies `applyBin` in `controls.k:15-18` |
| `Int` | `syntax.k:7` | `Int(I) => I` in `core.k:194` |
| `Str` | `syntax.k:11` | ASCII code conversion in `str.k:10-14` |
| `BinOp("%",...)`, `BinOp("//",...)` | `syntax.k:13` with left-to-right `seqstrict(2,3)` | dispatch in `operators.k:8`; integer definitions and `pyMod` in `int.k:8-18` |
| `Compare(..., CmpOp("<"|"==",...))` | `syntax.k:31-33` | left then wrapped-right evaluation in `operators.k:11-14`; integer cases in `int.k:21-26` |
| `If` | `syntax.k:46` with strict condition | truthiness and branch selection in `controls.k:43-47`; integer truthiness in `core.k:199-205` |
| `Return(Str(...))` | `syntax.k:47` with strict value | records `retV`, discards the residual function body, pops/restores the frame and returns the value in `functions.k:79-91` |

The active configuration is `core.k:49-60`: `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and
`<exit-code>`. The entry claims pin all cells initially. Function entry creates
one local scope/frame; return removes it and restores the exact pinned
non-scope cells. Module loading intentionally leaves the installed `solve`
binding in scope 0, so the claims existentially frame only the final
`<scopes>` map.
