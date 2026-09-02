# Stage 5 local K inventory and soundness classification

Scope: the fresh source copies of `semantic.k`, `verification.k`, and `spec.k`
under `/tmp/audit-work/84-solve`.  No candidate-kompiled artifact was used.
The source-extraction command and line-numbered declarations are in
`stage5_declaration_extract.log`.

## Attribute and extension summary

- Function productions: 14 (`evalExpr`, `nthValue`, `evalNthExpr`,
  `evalExprs`, `getInt`, `tupleItems`, `runProgram`, `oracleDigitSum`,
  `oracleBinary`, `oracleBinaryPositive`, `appendOracleBit`, `sameValue`,
  `checkInput`, and `checkRange`).
- Macro productions: one (`solutionProgram`).
- `total`, `functional`, `simplification`, priority, and opaque declarations:
  none.
- Operational rules: 19 in `MPY-SEMANTIC`.
- Verification equations, including the macro equation: 13.
- Reachability claims: 11.
- Additional generated helper K files: none.

None is declared `total`; partiality therefore does not silently assert
coverage outside the equation guards.

## Syntax productions

| ID | Source | Production(s) | Use and assessment |
|---|---|---|---|
| SY1 | `semantic.k:7` | `Pgm ::= Module(FuncDef)` | Used by the submitted module; faithful constructor. |
| SY2 | `semantic.k:8` | `FuncDef ::= FuncDef(String, Params, Stmt)` | Used for `solve`; faithful constructor. |
| SY3 | `semantic.k:9` | `Params ::= Params(String)` | Used for the single `N` parameter. |
| SY4 | `semantic.k:11` | `Stmt ::= Return(Expr)` | The only submitted statement. |
| SY5–SY10 | `semantic.k:13-18` | `Name`, `Int`, `Str`, `BinOp`, `Subscript`, `TupleExpr` expressions | Exactly the expression constructors in `solution.mpy`; no used constructor is missing. |
| SY11–SY12 | `semantic.k:19-20` | singleton and cons `NeExprs` | Represent the nonempty tuple contents. |
| SY13–SY15 | `semantic.k:28-30` | `VInt`, `VStr`, `VTuple` | Sufficient value domain for all submitted expressions. |
| SY16–SY17 | `semantic.k:31-32` | `VNil`, `VCons` | Tuple value representation. |
| F1–F3 | `semantic.k:34-36` | `evalExpr`, `nthValue`, `evalNthExpr` `[function]` | Partial evaluators; every actual call is covered. |
| F4–F5 | `semantic.k:37-38` | `evalExprs`, `getInt` `[function]` | Tuple evaluation and integer projection; actual calls are covered. |
| F6 | `semantic.k:55` | `tupleItems` `[function]` | Truthful projection; unused by the submitted execution path. |
| F7 | `semantic.k:73` | `runProgram` `[function]` | Matches the exact single-function module shape. |
| F8–F11 | `verification.k:7-10` | `oracleDigitSum`, `oracleBinary`, `oracleBinaryPositive`, `appendOracleBit` `[function]` | Independent mathematical specification functions. |
| F12–F14 | `verification.k:11-13` | `sameValue`, `checkInput`, `checkRange` `[function]` | Result comparison and exhaustive finite-domain fold. |
| M1 | `verification.k:17` | `solutionProgram` `[macro]` | Expands to the submitted constructor tree; fresh `kast` byte comparison passes. |

## Operational rules in `semantic.k`

| ID | Lines | Rule | Static judgment |
|---|---:|---|---|
| S1 | 40 | parameter-name lookup | Correct: it returns `N` only when the `Name` string equals the bound parameter string. |
| S2 | 41 | integer literal | Correct. |
| S3 | 42 | string literal | Correct. |
| S4 | 44–45 | integer `+` | Correct for integer operands; all actual operands are integers. |
| S5 | 46–47 | integer `//` via `/Int` | Correct for the nonnegative dividend and positive literal divisors used here. |
| S6 | 48–49 | integer `%` via `%Int` | Correct for the same nonnegative/positive domain. |
| S7 | 51 | tuple expression to `VTuple(evalExprs(...))` | Correct eager value construction for this pure subset. |
| S8 | 52–53 | direct tuple-literal subscript via `evalNthExpr` | Correct on the exact submitted occurrence: all 37 elements are pure string literals and the computed index is in `0..36`. It is over-broad as a general Python rule because it skips unselected element evaluation. For example, outside the submitted program, a first element `1 // 0` followed by selecting a later element would return a value here while Python raises. No such false conclusion is enabled for any intended input of the fixed submitted program. |
| S9 | 56 | `tupleItems(VTuple(VS))` | Correct projection; unused by the target path. |
| S10 | 57 | `getInt(VInt(I))` | Correct projection. Other value kinds remain visibly partial rather than receiving fabricated integers. |
| S11 | 59 | singleton `evalExprs` | Correct. |
| S12 | 60–61 | cons `evalExprs` | Correct and structurally descending. |
| S13 | 63 | singleton `evalNthExpr` at zero | Correct. |
| S14 | 64 | cons `evalNthExpr` at zero | Correct. |
| S15 | 65–67 | positive-index `evalNthExpr` | Correct, guarded by `I > 0`, and structurally descending. The three `evalNthExpr` guards/shapes are disjoint. |
| S16 | 69 | `nthValue` at zero | Correct. |
| S17 | 70–71 | positive-index `nthValue` | Correct, guarded, and structurally descending. |
| S18 | 74–77 | `runProgram` | Binds the actual parameter name and evaluates the actual return expression; it does not replace execution with an oracle. |
| S19 | 86–88 | top-level configuration execution | Consumes the parsed program and places `runProgram(P,N)` in `<result>` while preserving `<input>`; concrete runs reach the expected result. |

Configuration (`semantic.k:79-84`): `<k>` contains the program, `<input>`
contains the only external integer, and `<result>` contains the returned K
value.  There is no heap, allocation, mutation, I/O, exception handler, or call
stack in the submitted one-expression function.  Omitting those cells loses no
observable behavior for this program.

Evaluation-order observation: S8 evaluates the index before selecting one
tuple literal rather than eagerly evaluating the complete tuple before the
index as CPython does.  Every tuple element is a side-effect-free string
literal, the index expression is pure integer arithmetic, all divisors are
positive, and every intended index is in range.  The order difference is thus
semantically inert for this fixed program but limits reuse of the rule as
general Python semantics.

## Verification equations

| ID | Lines | Equation | Static judgment |
|---|---:|---|---|
| V1 | 18–67 | `solutionProgram` macro expansion | Exact current AST, established mechanically by identical expanded `kast` JSON. |
| V2 | 69–70 | one-digit decimal sum | Correct on `0 <= N < 10`. |
| V3 | 71–72 | recursive decimal digit sum | Correct on `N >= 10`; division descends and its guard is disjoint from V2. Together V2–V3 cover all nonnegative inputs. |
| V4 | 74 | binary zero | Correct. |
| V5 | 75–76 | dispatch positive binary conversion | Correct and disjoint from V4. |
| V6 | 77 | positive binary base case | Correct for one. |
| V7 | 78–80 | recursive positive binary conversion | Correct for `N > 1`; division descends, remainder is 0 or 1, and the guard is disjoint from V6. |
| V8–V9 | 81–82 | append bit zero/one | Correct, disjoint, and complete for all reachable remainders. |
| V10 | 84 | string-value equality | Correct for the two reachable `VStr` operands. |
| V11 | 85–86 | `checkInput` | Result-constraining equality between actual AST evaluation and the independent digit-sum/binary specification. It is not an execution bridge or an unconstrained oracle. |
| V12 | 87 | empty `checkRange` | Correct identity for the exclusive upper bound. |
| V13 | 88–89 | recursive `checkRange` | Correct conjunction for `N < LIMIT`, descends by increasing `N`, and does not overlap V12. It is intentionally partial for `N > LIMIT`, which no claim reaches. |

For `0 <= N <= 10000`, the submitted arithmetic index is the sum of the five
decimal positions.  Inputs `0..9999` have maximum 36 at 9999, and 10000 has
index 1; therefore the 37-entry tuple is accessed only at indices `0..36`.

## Claims in `spec.k`

There are eleven unconditional, ground claims:

- C1: `checkRange(0,1000) => true`
- C2: `checkRange(1000,2000) => true`
- C3: `checkRange(2000,3000) => true`
- C4: `checkRange(3000,4000) => true`
- C5: `checkRange(4000,5000) => true`
- C6: `checkRange(5000,6000) => true`
- C7: `checkRange(6000,7000) => true`
- C8: `checkRange(7000,8000) => true`
- C9: `checkRange(8000,9000) => true`
- C10: `checkRange(9000,10000) => true`
- C11: `checkRange(10000,10001) => true`

Their half-open ranges are disjoint and their union is exactly every integer
from 0 through 10000.  The warning that each claim is proven without
reachability rewriting reflects concrete function simplification of a ground
term.  It is not vacuity: changing the actually executed program value for
input zero makes C1 reduce to `false` and produces `WarnStuckClaimState`.

## Static conclusion

No local rule encodes the task answer as an execution rewrite, supplies an
unconstrained result-bearing symbol, bypasses the submitted return expression,
or introduces a false conclusion for an intended input.  The only identified
generality limitation is S8's over-broad lazy tuple-subscript equation; its
skipped evaluations are demonstrably pure literals in the fixed target.
