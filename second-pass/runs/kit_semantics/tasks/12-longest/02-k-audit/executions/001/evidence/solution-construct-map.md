# `solution.mpy` construct-to-semantics map

| Submitted constructor | Declaration | Material rules / generated evaluation |
|---|---|---|
| `Module(Stmts)` | `semantics/syntax.k:61` | Initial configuration `core.k:49`; `#loadAll` and statement sequencing `core.k:124-127` |
| `ImportFrom("typing",...)` | `syntax.k:43` | Non-math import is runtime no-op, `controls.k:36`; this removes only typing metadata |
| `FuncDef` | `syntax.k:53` | Closure binding in current module scope, `functions.k:14-16` |
| `Params("strings")` | `syntax.k:57-60` | Parameter binding `functions.k:63-66` |
| `If` | `syntax.k:49 [strict(1)]` | Guard evaluated before either branch; branch formation/selection `controls.k:51-54` |
| `UnaryOp("not",...)` | `syntax.k:14 [strict(2)]` | Dispatch `operators.k:10`; Boolean result `bool.k:8`; list truthiness `core.k:204` |
| `Name` | `syntax.k:12` | Current/parent/builtin lookup `core.k:130-154`; the claim fixes the scope chain and excludes module shadowing of `len` |
| `Return` | `syntax.k:50 [strict]` | Abruptly selects `#pop`, `functions.k:78-79`; frame pop/restoration `functions.k:85-90` |
| `NoneVal` | `syntax.k:27` | `noneV`, `core.k:196` |
| `Assign` | `syntax.k:41 [strict(2)]` | RHS first, then current-scope write `controls.k:9-11` |
| `Subscript(Name("strings"),Int(0))` | `syntax.k:22`, `Index ::= Expr` at `syntax.k:38` | Object then index contexts `subscript.k:27-28`; `Int` literal `core.k:194`; dispatch `subscript.k:35`; list indexing `subscript.k:38`; index normalization `subscript.k:21-23`; in-bounds recursion `subscript.k:11-14`; sequence length `core.k:223-225` |
| `For` | `syntax.k:45 [strict(2)]` | Iterable evaluated once; loop setup/step `controls.k:65-74`; list iterator `list.k:9-10`; name target binding `tuple.k:31-34` |
| `Call` | `syntax.k:28` | Callee before arguments `call.k:19-21`; left-to-right argument loop `core.k:185-191`; closure dispatch `call.k:69-74`; builtin fallback `call.k:31` |
| `Call(Name("len"),...)` | above | Builtin binding in `core.k:157-181`; `applyBuiltin("len",...)` and fixed `seqLen` equations `builtins.k:17-26`; guarded proof bridge `verification.k:76-78` agrees on strings |
| `Compare(...,CmpOp(">",...))` | `syntax.k:30,32` | Left then right contexts and dispatch `operators.k:14-17`; integer greater-than `int.k:24` |
| `.Stmts` / constructor juxtaposition | `syntax.k:56` | Free list identity/associativity; explicit `.Stmts` in claims is the same identity that the translator omits textually |

The only source-body value operation with a proof-local operational bridge is
string `seqLen`. Assignment, iteration, lookup, call/return, control flow,
subscript access, and scope/frame state changes all execute through supplied
rules.
