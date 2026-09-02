# `solution.mpy` construct-to-semantics map

| Submitted construct | Declaration | Execution rules |
|---|---|---|
| `Module(Stmts)` | `semantics/syntax.k` (`Module`, `Stmts`) | `core.k`: initial `#loadAll`, `#loadAll(Module(SS))`, statement sequencing, `.Stmts` |
| `FuncDef`, `Params` | `syntax.k` | `functions.k`: function definition creates `closureVal`; `call.k`: closure call creates frame; `functions.k`: parameter bind and frame pop |
| `Name` | `syntax.k` | `core.k`: `Name` becomes `#look`; lookup walks current scope then builtins |
| `Assign` | `syntax.k`, strict RHS | `controls.k`: current-scope update (cell case is irrelevant here) |
| `Call`, argument list | `syntax.k` | `call.k`: evaluate callee then arguments; `core.k`: left-to-right `#evalArgs`; `call.k`: dispatch |
| builtin `len(str)` | `core.k` builtins scope; `builtins.k` `applyBuiltin`/`seqLen` | `call.k`: builtin routing; `builtins.k`: `seqLen(str(IS)) => isLen(IS)`; `core.k`: structural `isLen` |
| `If`, `Compare`, `<`, `==` | `syntax.k` | strictness/contexts plus `controls.k` branch rules, `operators.k` compare dispatch, `int.k` integer comparison equations |
| `Int`, `Bool` | `syntax.k` | `core.k` literal rules |
| `While` | `syntax.k` | fixed semantics in `controls.k`: `While => #while`, condition evaluation, body/loop label, exit |
| `BinOp("%", ...)` | `syntax.k`, sequential strictness | `operators.k` dispatch; `int.k`: `%` to `pyMod` and its equation |
| `AugAssign("+", ...)` | `syntax.k`, strict RHS | `controls.k`: current binding update via `applyBin`; `int.k`: integer addition |
| `Return` | `syntax.k`, strict expression | `functions.k`: sets `retV`, discards remaining callee continuation, pops frame, restores caller |
| `primeLoopBody`, `primeBody`, `primeLengthClosure` | `verification.k` proof-local function syntax | exact constructor abbreviations; their equations do not replace execution |
| `#primeLoopEntry`, capture continuations | `verification.k` proof-only `KItem` syntax | three priority bridges intercept `While`, read `n`/`divisor`, discard the continuation and frame/state |
| `noDivisorsFrom` | `verification.k` proof-local function | guarded base/composite/recursive mathematical equations using `pyMod` |
