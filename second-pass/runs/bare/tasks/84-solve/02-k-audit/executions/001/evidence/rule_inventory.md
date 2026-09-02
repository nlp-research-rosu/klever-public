# Exhaustive local rule and declaration inventory

Scope: the fresh source copy at `/tmp/audit-work/src/{semantic.k,verification.k,spec.k}`. Built-in declarations imported from K's `INT`, `STRING`, and `BOOL` modules are trust-boundary primitives, not local rules.

## Local syntax

`MPY-SYNTAX` declares the exact submitted constructor subset:

| ID | Sort | Production | Used by submitted `solution.mpy` |
|---|---|---|---|
| S1 | `Pgm` | `Module(FuncDef)` | Yes |
| S2 | `FuncDef` | `FuncDef(String, Params, Stmt)` | Yes |
| S3 | `Params` | `Params(String)` | Yes |
| S4 | `Stmt` | `Return(Expr)` | Yes |
| S5 | `Expr` | `Name(String)` | Yes |
| S6 | `Expr` | `Int(Int)` | Yes |
| S7 | `Expr` | `Str(String)` | Yes |
| S8 | `Expr` | `BinOp(String, Expr, Expr)` | Yes, operators `+`, `//`, `%` |
| S9 | `Expr` | `Subscript(Expr, Expr)` | Yes |
| S10 | `Expr` | `TupleExpr(NeExprs)` | Yes |
| S11 | `NeExprs` | singleton `Expr` | Yes, tail of the tuple |
| S12 | `NeExprs` | `Expr, NeExprs` | Yes |

`MPY-SEMANTIC` declares:

| ID | Sort | Production/role |
|---|---|---|
| S13 | `Value` | `VInt(Int)` |
| S14 | `Value` | `VStr(String)` |
| S15 | `Value` | `VTuple(VList)` |
| S16 | `VList` | `VNil` |
| S17 | `VList` | `VCons(Value, VList)` |
| F1 | `Value` | `evalExpr(Expr, String, Int) [function]` |
| F2 | `Value` | `nthValue(VList, Int) [function]` |
| F3 | `Value` | `evalNthExpr(NeExprs, Int, String, Int) [function]` |
| F4 | `VList` | `evalExprs(NeExprs, String, Int) [function]` |
| F5 | `Int` | `getInt(Value) [function]` |
| F6 | `VList` | `tupleItems(Value) [function]` |
| F7 | `Value` | `runProgram(Pgm, Int) [function]` |

`VERIFICATION` declares:

| ID | Sort | Production/role |
|---|---|---|
| F8 | `Int` | `oracleDigitSum(Int) [function]` |
| F9 | `Value` | `oracleBinary(Int) [function]` |
| F10 | `Value` | `oracleBinaryPositive(Int) [function]` |
| F11 | `Value` | `appendOracleBit(Value, Int) [function]` |
| F12 | `Bool` | `sameValue(Value, Value) [function]` |
| F13 | `Bool` | `checkInput(Int) [function]` |
| F14 | `Bool` | `checkRange(Int, Int) [function]` |
| M1 | `Pgm` | `solutionProgram [macro]` |

There are no local `[total]`, `[functional]`, `[opaque]`, `[priority]`, `[simplification]`, `[strict]`, or `[seqstrict]` declarations or rules. Partial function coverage therefore remains visible as a stuck term. There are no fresh or existential result symbols.

## Configuration

C1 is `<mpy><k>$PGM:Pgm</k><input>$N:Int</input><result>.K</result></mpy>`. The only mutable transition consumes the whole `Pgm` in `<k>`, preserves `<input>`, and writes `runProgram(P,N)` into an initially empty `<result>`. There is no heap, allocation, I/O, call stack, exception cell, or hidden state.

## `semantic.k` rules

| ID | Source | Rule summary | Judgment on the submitted program and domain |
|---|---|---|---|
| R1 | 40 | Matching `Name(X)` reads the sole parameter value `N` | Sound; exact lexical binding represented by the `X` argument. |
| R2 | 41 | `Int(I)` becomes `VInt(I)` | Sound literal semantics. |
| R3 | 42 | `Str(S)` becomes `VStr(S)` | Sound literal semantics. |
| R4 | 44–45 | `BinOp("+",E1,E2)` recursively evaluates integers and applies `+Int` | Sound for the pure integer operands used. |
| R5 | 46–47 | `BinOp("//",E1,E2)` recursively evaluates integers and applies `/Int` | Sound for intended nonnegative dividends and the submitted positive constant divisors. Division by zero and broader Python numeric behavior are unmodeled, but unused. |
| R6 | 48–49 | `BinOp("%",E1,E2)` recursively evaluates integers and applies `%Int` | Sound for intended nonnegative dividends and submitted positive constant divisors. Broader negative-number behavior is outside the formal domain. |
| R7 | 51 | A tuple expression becomes a recursive `VList` wrapped in `VTuple` | Sound for pure tuple elements. |
| R8 | 52–53 | Tuple-literal subscript evaluates the index then selects/evaluates the indexed AST element | Sound for this tuple of string literals and indices 0–36. It intentionally omits negative/out-of-range behavior and does not eagerly evaluate unselected tuple elements; those differences are unobservable for the submitted pure literals and intended indices. |
| R9 | 56 | `tupleItems(VTuple(VS))` projects `VS` | Sound projection; unused by the submitted proof path. |
| R10 | 57 | `getInt(VInt(I))` projects `I` | Sound and used by arithmetic/indexing. |
| R11 | 59 | Singleton `evalExprs` produces a one-element `VList` | Sound. |
| R12 | 60–61 | Nonempty-tail `evalExprs` produces head followed by recursively evaluated tail | Sound; pure elements make unspecified reduction order observationally irrelevant here. |
| R13 | 63 | Index zero into a singleton expression sequence evaluates that expression | Sound. |
| R14 | 64 | Index zero into a multi-expression sequence evaluates the head | Sound. |
| R15 | 65–67 | Positive index discards one expression and decrements the index | Sound for the in-range 0–36 indices. Strict descent ensures termination. |
| R16 | 69 | `nthValue` at zero returns the head | Sound; unused by the submitted path. |
| R17 | 70–71 | `nthValue` at positive index recurses on the tail | Sound on in-range lists; unused by the submitted path. |
| R18 | 74–77 | `runProgram` invokes the exact one-function `solve`/one-parameter/`Return` module by evaluating its return expression with the argument bound | Sound minimal entry-point semantics for the exact submitted module. It is deliberately not a general Python call model. |
| R19 | 86–88 | Top-level execution consumes the submitted module and places `runProgram(P,N)` in `<result>` | Sound; preserves input and has no other observable cells. |

Overlap/coverage findings:

- R1–R8 dispatch on distinct outer constructors/operator strings on the submitted tree.
- R13 and R14 are separated by singleton versus comma-list grammar; R15 requires a positive index, disjoint from both zero cases.
- R16 and R17 are disjoint by index guard.
- Every function is covered for every ground shape it receives on inputs 0–10000. Unsupported shapes remain stuck because no function is marked total.
- The evaluator is pure. Its lack of explicit Python left-to-right sequencing does not change value, control, state, or exceptions for this loop-free expression with constant nonzero divisors, string-literal tuple elements, and valid indices.

## `verification.k` rules and proof extensions

| ID | Source | Rule summary | Class and judgment |
|---|---|---|---|
| V1 | 18–67 | `solutionProgram` expands to a constructor tree | Compile-time macro, not an execution shortcut. Fresh `kast --expand-macros` evidence proves byte-regenerated `solution.mpy` parses to the identical tree. |
| V2 | 69–70 | Base decimal digit sum for 0–9 is the number itself | Truthful definitional equation; guard is disjoint from V3. |
| V3 | 71–72 | For `N>=10`, digit sum is `N % 10 + digitSum(N / 10)` | Truthful definitional equation over nonnegative integers; strict quotient descent. |
| V4 | 74 | Binary representation of zero is `"0"` | Truthful definitional equation. |
| V5 | 75–76 | Positive binary representation delegates to the positive helper | Truthful; guard disjoint from V4. |
| V6 | 77 | Positive binary representation of one is `"1"` | Truthful base case. |
| V7 | 78–80 | For `N>1`, recurse on `N/2` then append `N%2` | Truthful on positive integers; strict quotient descent and disjoint from V6. |
| V8 | 81 | Appending bit zero appends string `"0"` | Truthful, disjoint from V9. |
| V9 | 82 | Appending bit one appends string `"1"` | Truthful, disjoint from V8. |
| V10 | 84 | `sameValue` compares two represented strings with `==String` | Truthful equality definition. |
| V11 | 85–86 | `checkInput(N)` compares real `runProgram(solutionProgram,N)` with the digit-sum/binary oracle | Definitional checker. It does not replace or preempt program execution; result-bearing program and oracle computations are independent until equality. |
| V12 | 87 | Equal range endpoints produce `true` | Truthful empty-range base case. |
| V13 | 88–89 | For `N<LIMIT`, conjoin `checkInput(N)` with the check of the remaining interval | Truthful finite conjunction; strict `N+1` progress, with guard disjoint from V12. |

V2–V13 are proof-local definitional summaries/checkers, not operational bridges. No rule rewrites a source AST operation to an oracle result. The only result-bearing abstraction on the specification side is fully fixed by terminating equations over every ground value used by the claims.

## Claims

All claims have no variables and no `requires` clause, so their preconditions are the concrete, satisfiable initial terms themselves.

| Claim | Plain-language precondition and postcondition |
|---|---|
| `inputs-00000-00999` | Starting with the ground checker for each integer 0 through 999, it reduces to `true`: every modeled program result equals the modeled binary digit-sum oracle. |
| `inputs-01000-01999` | Same for 1000 through 1999. |
| `inputs-02000-02999` | Same for 2000 through 2999. |
| `inputs-03000-03999` | Same for 3000 through 3999. |
| `inputs-04000-04999` | Same for 4000 through 4999. |
| `inputs-05000-05999` | Same for 5000 through 5999. |
| `inputs-06000-06999` | Same for 6000 through 6999. |
| `inputs-07000-07999` | Same for 7000 through 7999. |
| `inputs-08000-08999` | Same for 8000 through 8999. |
| `inputs-09000-09999` | Same for 9000 through 9999. |
| `input-10000` | Starting with the ground checker for 10000 alone, it reduces to `true`. |

The intervals are adjacent, exclusive at each upper bound, and their union is exactly the intended integer domain 0–10000. The destination `true` is result-constraining: a false `sameValue` prevents the conjunction from becoming `true`. The fresh wrong-result mutation demonstrates that the actual `VStr("1100")` residual at input 147 does not satisfy `VStr("1101")`.
