# Exhaustive local K inventory

Scope: the clean scratch copies of `semantic.k`, `verification.k`, and
`spec.k`. There are no other candidate K helper files.

## Modules and configuration

- `MPY-SYNTAX` imports `INT-SYNTAX` and `STRING-SYNTAX`.
- `DIGIT-SUM-SEMANTICS` imports `MPY-SYNTAX`, `INT`, `BOOL`, `STRING`,
  `MAP`, and `K-EQUAL`.
- `SEMANTIC` imports `DIGIT-SUM-SEMANTICS` and
  `DIGIT-SUM-VERIFICATION`.
- `DIGIT-SUM-VERIFICATION` imports `INT`, `BOOL`, `STRING`, and
  `K-EQUAL`.
- `SPEC` imports `SEMANTIC` and `DIGIT-SUM-VERIFICATION`.
- The configuration has exactly four state cells: `<k>` for computation,
  immutable `<input>`, local `<env>` map, and `<result>`. There is no heap,
  I/O, exception, call stack, or function-binding cell.

## Local syntax and declarations

| ID | Location | Declaration |
|---|---|---|
| D01 | `semantic.k:7` | `Program ::= Module(Stmts)` with symbol `Module` |
| D02 | `semantic.k:10` | `Stmts ::= List{Stmt, ""}`; juxtaposition is sequencing |
| D03 | `semantic.k:12` | `Stmt ::= FuncDef(String, Params, Stmts)` with symbol `FuncDef` |
| D04 | `semantic.k:13` | `Stmt ::= Assign(Expr, Expr)` with symbol `Assign` |
| D05 | `semantic.k:14` | `Stmt ::= For(Expr, Expr, Stmts)` with symbol `For` |
| D06 | `semantic.k:15` | `Stmt ::= If(Expr, Stmts, Stmts)` with symbol `If` |
| D07 | `semantic.k:16` | `Stmt ::= Return(Expr)` with symbol `Return` |
| D08 | `semantic.k:18` | `Params ::= Params(String)` with symbol `Params` |
| D09 | `semantic.k:20` | `Expr ::= Name(String)` with symbol `Name` |
| D10 | `semantic.k:21` | `Expr ::= Int(Int)` with symbol `IntExpr` |
| D11 | `semantic.k:22` | `Expr ::= Str(String)` with symbol `Str` |
| D12 | `semantic.k:23` | `Expr ::= BinOp(String, Expr, Expr)` with symbol `BinOp` |
| D13 | `semantic.k:24` | `Expr ::= Call(Expr, Expr)` with symbol `Call` |
| D14 | `semantic.k:25` | `Expr ::= Compare(Expr, CmpOps)` with symbol `Compare` |
| D15 | `semantic.k:27` | `CmpOps ::= List{CmpOp, ","}` |
| D16 | `semantic.k:28` | `CmpOp ::= CmpOp(String, Expr)` with symbol `CmpOp` |
| D17 | `semantic.k:39-41` | `Value ::= intVal(Int) | strVal(String) | boolVal(Bool)` |
| D18 | `semantic.k:42` | `Result ::= noResult | Value` |
| D19 | `semantic.k:44-47` | K items `execute`, `execStmt`, `loopString`, `addUpper` |
| D20 | `semantic.k:49` | `eval(Expr, Map) : Value [function]` |
| D21 | `semantic.k:50` | `addValues(Value, Value) : Value [function]` |
| D22 | `semantic.k:51` | `ordValue(Value) : Value [function]` |
| D23 | `semantic.k:52` | `compareLE3(Value, Value, Value) : Value [function]` |
| D24 | `semantic.k:53` | `stringOf(Value) : String [function]` |
| D25 | `semantic.k:54` | `truthOf(Value) : Bool [function]` |
| D26 | `semantic.k:55` | `pythonUpperOrd(String) : Int [function]` |
| D27 | `verification.k:9` | `upperAsciiSum(String) : Int [function]` |
| D28 | `verification.k:10` | `upperAsciiContribution(String) : Int [function]` |

No local declaration has `[total]`, `[functional]`, `[opaque]`, `[macro]`,
`[anywhere]`, `[owise]`, `[priority]`, or a numeric priority. There are no
fresh symbols. D01 and D03-D14/D16 use `[symbol(...)]`; the two `List`
declarations bring their normal unit/concatenation syntax into the compiled
definition.

## Ordinary semantic rules

| ID | Location | Rule and audit conclusion |
|---|---|---|
| R01 | `semantic.k:57` | `eval(Int(I), _) => intVal(I)`. Faithful literal evaluation. |
| R02 | `semantic.k:58` | `eval(Str(S), _) => strVal(S)`. Faithful literal evaluation. |
| R03 | `semantic.k:61` | Lookup of the key most recently installed by map update. `[simplification]`; faithful for K map update. |
| R04 | `semantic.k:62-63` | Lookup skips a different map-update key. Guard `X =/=String Y`; faithful and structurally descending. `[simplification]`. |
| R05 | `semantic.k:64-65` | Lookup in a concrete map fragment, guarded so `X` is absent from the frame. Faithful for a unique K map key. |
| R06 | `semantic.k:66-67` | Only `BinOp("+",...)` is modeled, and delegates to R09. Faithful for the actually used integer operands. |
| R07 | `semantic.k:68-69` | Only syntactic `Call(Name("ord"), ARG)` is modeled. It pins that syntax to the primitive rather than modeling Python binding, acceptable only for this closed generated term. |
| R08 | `semantic.k:70-72` | The exact two-link `<=` comparison delegates to R11. It eagerly evaluates pure `eval` terms and does not model Python short-circuit or effects. Reachable target operands are single-character strings, but the declaration/rule match domain is broader. |
| R09 | `semantic.k:74` | Adds two `intVal` values with mathematical integer addition. Faithful on its match domain. |
| R10 | `semantic.k:75` | Applies K `ordChar` to any `strVal(S)` without a length-one guard. Faithful only for length-one strings; invalid strings yield backend failure or bottom. |
| R11 | `semantic.k:76-78` | Compares code points of three strings without length-one guards. For reachable target characters it agrees with the ASCII bounds test; it is not a general Python string-comparison rule. |
| R12 | `semantic.k:79` | Projects a string value. Faithful. |
| R13 | `semantic.k:80` | Projects a Boolean value. Faithful, though unused by the target execution because R19 bypasses it. |
| R14 | `semantic.k:81-85` | `pythonUpperOrd(C)` computes `ord(C)` for code points 65–90, else 0. Correct for a length-one `C`; unguarded and partial elsewhere. |
| R15 | `semantic.k:97-100` | A module containing exactly the `digitSum(s)` binding is treated as an immediate call on `<input>`, binding `"s"` and executing `BODY`. This is an explicit single-entry execution convention, not Python module-definition behavior. |
| R16 | `semantic.k:102` | Empty statement execution terminates. Faithful. |
| R17 | `semantic.k:103` | Nonempty statements execute head then tail, preserving left-to-right statement order. Faithful. |
| R18 | `semantic.k:105-106` | Name assignment evaluates the modeled pure expression and updates `<env>`. Faithful for the supported, exception-free target expressions. |
| R19 | `semantic.k:111-123` | **Task-specific operational bridge.** It recognizes the complete target `if` syntax and directly updates `total` through `pythonUpperOrd`, skipping `Compare`, the selected branch, `BinOp`, and `Call`. It accepts arbitrary environments and continuations. No bridge-free connection theorem exists. Concrete false-domain witness: the same rule with `X = "s"` and input `""` should short-circuit to total 0 in Python, but K evaluates `ordChar("")` and yields `#Bottom`; see `stage5-if-short-circuit-witness.log`. The submitted loop never invokes R19 because R22 skips the body entirely. |
| R20 | `semantic.k:125-127` | `For(Name(X), ITER, BODY)` becomes `loopString` after projecting `ITER` as a string. It does not itself bind the loop variable. Its fidelity depends entirely on R21/R22/R23. |
| R21 | `semantic.k:129` | Empty `loopString` terminates without binding the target. This agrees with Python for a never-entered loop. |
| R22 | `semantic.k:130-148` | **Task-answer operational bridge.** It matches the exact target body, consumes one string character, schedules `addUpper`, and recurs. It never binds `"char"` and never executes the matched `If`/assignment/call body. Its `...` admits every continuation. No bridge-free universal connection theorem exists. Concrete false state/control witness: for input `"A"` and the admitted continuation `return char`, Python returns `"A"` but K has only `s` and `total` in `<env>` and gets stuck evaluating `Name("char")`; see `stage5-loop-context-witness.log`. On the submitted `return total` continuation, finite concrete tests show its arithmetic summary agrees with the ASCII-only implementation. |
| R23 | `semantic.k:150-154` | Adds `pythonUpperOrd(C)` to a uniquely framed integer `total`. Correct for the length-one substrings produced by R22, but it is the summary effect replacing the source body. |
| R24 | `semantic.k:156-158` | Return discards the remaining continuation, clears locals, and writes the evaluated result. Abrupt continuation discard matches return; clearing locals is this model's final-state convention. |

R19 and R22 materially bypass the property-bearing computation. R22 is the
rule actually used by the submitted program and duplicates the proof contract's
ASCII contribution rather than executing the submitted loop body. The finite
`krun` comparison supports its value on tested inputs but is not a universal
connection theorem.

## Verification functions and simplifications

| ID | Location | Rule and audit conclusion |
|---|---|---|
| R25 | `verification.k:12` | `upperAsciiSum("") => 0 [simplification]`. True. |
| R26 | `verification.k:13-16` | Nonempty `S` contributes its first K character then recurses on the suffix. Guard is disjoint from R25 and length descends. `[simplification]`. It defines an ASCII-only sum, not Python `str.isupper`. |
| R27 | `verification.k:18-22` | Contribution is `ord(C)` exactly for code points 65–90. `[simplification]`. True for length-one `C`; unguarded and partial otherwise. All calls from R26 use a length-one substring. |
| R28 | `verification.k:25` | `(I +Int J) +Int K => I +Int (J +Int K) [simplification]`. Mathematical integer associativity, oriented toward right association; true and terminating on left nesting. |

R25-R28 have no pairwise conflicting overlaps: R25/R26 have disjoint guards;
R27 is the sole contribution equation; R28 preserves integer value.

## Claims

| ID | Location | Plain-language statement |
|---|---|---|
| C01 | `spec.k:10-26` | For every K string `S`, starting with the exact submitted constructor module, input `S`, empty environment, and no result, execution terminates with empty computation/environment and result `intVal(upperAsciiSum(S))`. There is no precondition. |
| C02 | `spec.k:30-51` | For every suffix `S`, integer accumulator `A`, input string `INPUT`, and frame map not containing `total`, the exact task-specific `loopString` followed by `return total` finishes with result `A + upperAsciiSum(S)` and empty environment. |

Satisfying states are nonempty: C01 admits `S = ""`; C02 admits `S = "AB"`,
`A = 7`, `INPUT = "witness-input"`, and
`FRAME = ("other" |-> intVal(99))`. C02's destination is then 138. The
entry theorem at `S = "AB"` similarly requires 131; fresh concrete K and both
Python implementations return 131. At the equally satisfying input `S = "É"`,
the theorem requires 0 and agrees with the submitted implementation, while the
trusted canonical requires 201.
