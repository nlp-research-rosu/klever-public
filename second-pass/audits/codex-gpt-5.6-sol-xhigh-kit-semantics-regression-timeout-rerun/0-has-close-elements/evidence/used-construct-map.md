# Program construct to supplied-semantics map

This map covers every constructor in the byte-identical regenerated
`solution.mpy`. Full source-level declarations and all imported rules are in
`rule-inventory.md`.

| Program construct | Declaration | Execution rules used |
|---|---|---|
| `Module(Stmts)` | `syntax Module`, `syntax Stmts` in `semantics/syntax.k:56-61` | `#loadAll(Module(SS)) => SS` and statement sequencing in `semantics/core.k:123-127` |
| `ImportFrom("typing","List")` | `syntax Stmt ::= ImportFrom(...)` in `syntax.k:41-54` | non-`math` import is a no-op, `controls.k:33-44` |
| `FuncDef`, `Params` | `syntax Stmt ::= FuncDef(...)`, `syntax Params` in `syntax.k:53-60` | closure creation in `functions.k:14-16` |
| `Assign(Name(...), Expr)` | `Assign` is strict in RHS, `syntax.k:41` | plain-frame scope update in `controls.k:9-11`; higher-priority cell write is inapplicable because the frame has no `$cells` marker |
| `Name` | `syntax Expr ::= Name(String)`, `syntax.k:12` | current/parent scope lookup in `core.k:129-154`; `abs` reaches the fixed builtins scope |
| `Bool`, `Int`, `Float` literals | `syntax.k:9-12`; `Float` is added to `Val` in `float.k:20` | literal reductions in `core.k:193-196` and `float.k:19-21` |
| `For(target, iterable, body)` | strict iterable declaration in `syntax.k:45` | loop setup/step in `controls.k:62-74`; list iteration in `list.k:8-10`; target binding is the `Name` case in `tuple.k` |
| nested `If` | strict condition declaration in `syntax.k:49` | truth conversion/branching in `controls.k:50-54`; conditions here are already `Bool` |
| `Compare(..., CmpOp(...))` | `syntax.k:30-32`, evaluation contexts in `operators.k:14-17` | `i < j` dispatches to `int.k:22`; float distance comparison dispatches to opaque `floatLt` at `float.k:46-52` |
| `BinOp("+",...)` | sequentially strict operands in `syntax.k:15` | generic dispatch in `operators.k:12`; integer addition in `int.k:9` |
| `BinOp("-",...)` | same declaration/dispatch | Float subtraction maps to opaque `subF` at `float.k:101-105`; verification's guarded simplification is the identical sort-exposed equation |
| `Call(Name("abs"), ...)` | `Call` in `syntax.k:28` | name lookup, left-to-right callee/argument evaluation in `core.k:183-191` and `call.k:18-32`; Float `abs` maps to opaque `absF` in `float.k:54-56` |
| entry `Call(Name("has_close_elements"), ...)` | same `Call` declaration | closure frame creation and binding in `call.k:69-74` and `functions.k:62-75` |
| `Return(Name("result"))` | strict `Return` in `syntax.k:50` | return sets `retV`, discards the rest of the function body, then restores/deallocates the frame in `functions.k:77-90` |

The used configuration is the complete nine-cell configuration in
`core.k:44-60`: `k`, `env`, `scopes`, `scopeLoc`, `heap`, `heapLoc`, `stack`,
`ret`, `exc`, and `exit-code`. Every positive claim and both operational bridges
pin every one of these cells.
