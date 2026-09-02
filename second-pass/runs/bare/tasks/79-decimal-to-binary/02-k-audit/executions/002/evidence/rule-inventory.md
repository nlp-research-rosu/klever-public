# Exhaustive local K inventory

This inventory covers `/candidate/semantic.k`, `/candidate/verification.k`, and
`/candidate/spec.k`. Imported K domain modules are part of the external
toolchain trust boundary, not local declarations.

## Local syntax and configuration

| File/line | Declaration or production | Attributes / role |
|---|---|---|
| `semantic.k:7` | `Program ::= Module(Stmt)` | `symbol(moduleProgram)` |
| `semantic.k:9-11` | `Stmt ::= FuncDef(String,Params,Stmt) \| Return(Expr)` | `symbol(functionDefinition)`, `symbol(returnStatement)` |
| `semantic.k:13` | `Params ::= Params(String)` | `symbol(parameters)` |
| `semantic.k:15-22` | `Expr ::= Int(Int) \| Str(String) \| Name(String) \| BinOp(String,Expr,Expr) \| Call(Expr,Expr) \| Subscript(Expr,Slice)` | constructor symbols |
| `semantic.k:24-26` | `Slice ::= Slice(Bound,Bound,Bound)`; `Bound ::= Expr \| NoBound` | constructor symbols |
| `semantic.k:35` | `Env ::= bind(String,Int)` | one-binding environment |
| `semantic.k:37-40` | `Val ::= intVal(Int) \| strVal(String) \| binVal(String) \| negativeBinVal(String)` | value/internal wrapper constructors |
| `semantic.k:42-45` | `Val ::= eval(Expr,Env) \| addValues(Val,Val) \| callBin(Val) \| suffixFrom(Val,Int)` | all four have `[function]`; none is `[total]` or `[functional]` |
| `semantic.k:47` | `String ::= binDigits(Int)` | `[function]`, partial outside nonnegative integers |
| `semantic.k:49-54` | `<python><k>$PGM</k><arg>$ARG</arg><result>.K</result></python>` | complete local state |
| `verification.k:9` | `String ::= decimalToBinarySpec(Int)` | `[function]`, two exhaustive guarded equations |

There are no local `total`, `functional`, `simplification`, `concrete`,
`priority`, `owise`, `macro`, `alias`, or opaque declarations.

## Operational and function rules

| ID | File/line | Complete domain and effect | Audit classification |
|---|---|---|---|
| S1 | `semantic.k:56-63` | Exact module/function/parameter/`Return(E)` shape, initial result `.K`; consumes `<k>` and writes `eval(E,bind("decimal",I))` | Entry operational rule |
| S2 | `semantic.k:65` | Any `Int(I)` and environment; returns `intVal(I)` | Structural evaluator equation |
| S3 | `semantic.k:66` | Any `Str(S)` and environment; returns `strVal(S)` | Structural evaluator equation |
| S4 | `semantic.k:67` | `Name(X)` with exactly matching `bind(X,I)`; returns `intVal(I)` | Binding lookup equation |
| S5 | `semantic.k:68-69` | `BinOp("+",LEFT,RIGHT)`; recursively evaluates both and applies `addValues` | Pure-expression evaluation equation |
| S6 | `semantic.k:70` | Exact syntactic builtin name `bin`, one argument; evaluates the argument and applies `callBin` | Builtin-call evaluation equation |
| S7 | `semantic.k:71-72` | Slice with integer start and omitted stop/step; evaluates base and applies `suffixFrom` | Subscript evaluation equation |
| S8 | `semantic.k:74` | Two integer values; mathematical integer addition | Value equation |
| S9 | `semantic.k:75` | Two string values; string concatenation | Value equation |
| S10 | `semantic.k:78-79` | `intVal(I)`, `I >= 0`; returns internal nonnegative-bin wrapper over `binDigits(I)` | Model of Python `bin` |
| S11 | `semantic.k:81-82` | `intVal(I)`, `I < 0`; returns negative-bin wrapper over `binDigits(-I)` | Model of Python `bin` |
| S12 | `semantic.k:84` | `binVal(S)` at slice start 2; returns `S` | Slice equation for `"0b" + S` |
| S13 | `semantic.k:85` | `negativeBinVal(S)` at slice start 2; returns `"b" + S` | Slice equation for `"-0b" + S` |
| S14 | `semantic.k:87-88` | `0 <= I < 2`; returns `Int2String(I)` | Binary-digit base equation |
| S15 | `semantic.k:89-90` | `I >= 2`; recurses on `I / 2`, appends `I % 2` | Binary-digit recursive equation |
| V1 | `verification.k:11-13` | `I >= 0`; `"db" + binDigits(I) + "db"` | Definitional specification summary |
| V2 | `verification.k:14-16` | `I < 0`; `"dbb" + binDigits(-I) + "db"` | Definitional specification summary |

The guarded pairs S10/S11, S14/S15, and V1/V2 are disjoint. The first and
third pairs cover all `Int`; S14/S15 cover every nonnegative `Int`, the only
domain on which `binDigits` is reached. S15 strictly decreases its nonnegative
argument. All other evaluator equations have disjoint outer constructors or
value constructors.

## Claims

| Claim | Precondition | Postcondition |
|---|---|---|
| `spec.k:6-32` | symbolic `I >= 0` | exact submitted term terminates with `strVal(decimalToBinarySpec(I))` |
| `spec.k:34-60` | symbolic `I < 0` | exact submitted term terminates with `strVal(decimalToBinarySpec(I))` |
| `spec.k:62-87` | fixed argument `15` | `strVal("db1111db")` |
| `spec.k:89-114` | fixed argument `32` | `strVal("db100000db")` |
| `spec.k:116-141` | fixed argument `-5` | `strVal("dbb101db")` |

There are no auxiliary claims, circularities, loop summaries, proof-local
ordinary rewrites, operational bridges, or simplification lemmas.
