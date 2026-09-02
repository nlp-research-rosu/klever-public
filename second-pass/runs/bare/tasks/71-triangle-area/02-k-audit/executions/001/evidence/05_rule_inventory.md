# Exhaustive local rule and declaration inventory

Scope: candidate `semantic.k` and `verification.k`. There are no
candidate-authored helper K files. Built-in modules (`rat.md`, integer, rational,
float-token, Boolean, string, list, and map support) are the ordinary low-level
K trust boundary.

## Configuration and syntax declarations

`MPY-SYNTAX` declares:

1. `Program ::= Module(Stmts)`.
2. `Stmts ::= List{Stmt,""}`.
3. `Stmt ::= FuncDef(String,Params,Stmts) | If(Exp,Stmts,) |
   Assign(Exp,Exp) | Return(Exp)`.
4. `Params ::= Params(Strings)` and `Strings ::= List{String,","}`.
5. `Exp ::= Int(Int) | Float(Float) | Name(String) | Call(Exp,Exprs)`.
6. `Exp ::= UnaryOp(String,Exp) [strict(2)] |
   BinOp(String,Exp,Exp) [seqstrict(2,3)] |
   Compare(Exp,CmpOp) [strict(1)]`. These attributes generate heating/cooling
   rules: unary operand first, binary left then right, and comparison left
   first.
7. `CmpOp ::= CmpOp(String,Exp)` and `Exprs ::= List{Exp,","}`.
8. `NumValue ::= VInt(Int) | VRat(Rat)`.
9. `Value ::= NumValue | VFloat(Float) | VSqrt(Rat) | VRounded(Int) |
   VBool(Bool)`.
10. `Values ::= List{Value,","}` and `Args ::= Args(Values)`.

`SEMANTIC` declares the configuration
`<triangle><k>launch($PGM,$ARGS)</k><env>.Map</env><functions>.Map</functions><result>NoResult</result></triangle>`.
The only mutable state is variable bindings, the function table, and the
terminal result. It additionally declares `Result ::= NoResult | Value`,
`Exp ::= Value`, `KResult ::= Value`, `Function ::= function(Strings,Stmts)`,
and the control items `launch`, `exec`, `invoke`, `bind`, `branch`,
`assignTo`, `returnValue`, `compareLE`, and `round2`.

The only `[total]` declaration is `asRat(NumValue)`. Its `VInt` and `VRat`
equations are disjoint and exhaustive. The other local functions are
`sqrtHundredths`, `findSqrtUpper`, `bisectSqrt`, and `finishSqrtRound`.
`sqrtHundredths` has a `[concrete(R), simplification]` equation. No declaration
uses `[functional]`; there are no explicit priority rules. The four
numeric/comparison fallback rules use `[owise]`.

`VERIFICATION` declares `[function]` constants/functions `solutionProgram` and
`heronRadicand(Int,Int,Int)`. There are no opaque declarations beyond the
symbolic `sqrtHundredths(R)` term that intentionally remains unreduced when
`R` is symbolic.

## Every rule in `semantic.k`

| ID / line | Rule | Static assessment |
|---|---|---|
| S1 / 75 | `launch(Module(SS),Args(VS)) => exec(SS) ~> invoke("triangle_area",VS)` | Correct for this one-module, fixed-entry program. |
| S2 / 78 | empty `exec` | Correct sequencing base. |
| S3 / 79 | head/tail `exec` | Correct source-order sequencing. |
| S4 / 81 | load `FuncDef` into `<functions>` | Correct for the sole definition; later same-name definitions overwrite as Python module execution would. |
| S5 / 84 | lookup/invoke body | Correct binding selection for the loaded `triangle_area`; no caller stack is modeled because the submitted program makes no program-defined calls. |
| S6 / 87 | empty `bind` | Correct arity base. |
| S7 / 88 | bind one parameter/value into `<env>` | Correct left-to-right binding for the exact three arguments. Arity errors are unmodeled but are outside all entry claims. |
| S8 / 92 | evaluate `If` guard then `branch` | Correct order. |
| S9 / 93 | true branch executes body | Correct. |
| S10 / 94 | false branch consumes no-body `If` | Correct for translated no-else nodes. |
| S11 / 96 | evaluate assignment RHS | Correct for the used `Name` targets. |
| S12 / 97 | store assignment result | Correct map update. |
| S13 / 100 | evaluate return expression | Correct. |
| S14 / 101 | terminal return discards `_REST`, clears env/functions, sets result | Matches a return from the sole active entry invocation, including discarding remaining statements. It is over-broad for nested calls/arbitrary continuations, but no such configuration is reachable from the submitted program; no false intended-domain result was found from this breadth. |
| S15 / 107 | `Int(I) => VInt(I)` | Correct. |
| S16 / 108 | `Float(F) => VFloat(F)` | Correct token conversion for the used exponent `0.5`. |
| S17 / 109 | variable lookup | Correct for bound names. |
| S18 / 112 | integer unary minus | Correct. |
| S19 / 113 | rational unary minus | Correct, though unused on the valid area path. |
| S20 / 117 | `asRat(VInt(I)) => I` | Correct exact injection. |
| S21 / 118 | `asRat(VRat(R)) => R` | Correct; with S20 it validates `[total]`. |
| S22 / 120 | integer `+` | Correct CPython unbounded-integer addition. |
| S23 / 121 | numeric `+` fallback `[owise]` | Correct exact rational promotion for internal rationals; the `owise` avoids overlap with S22. Float arguments are unsupported. |
| S24 / 125 | integer `-` | Correct. |
| S25 / 126 | numeric `-` fallback `[owise]` | Same promotion assessment as S23. |
| S26 / 130 | integer `*` | Correct. |
| S27 / 131 | numeric `*` fallback `[owise]` | Same promotion assessment as S23. |
| S28 / 135 | `/` on `NumValue` becomes exact `VRat` | **Unsound model of the real Python operation.** Python integer `/` converts to binary64 and may round, overflow, or raise. Direct witness: Python `20000000000000001 / 2 == 1e16`, while S28 produces exact `10000000000000000.5`. End-to-end satisfying witness `(10^16,10^16,1)` is detailed below. |
| S29 / 137 | `** 0.5` becomes `VSqrt(exact-rational)` | A result-bearing exact-mathematics abstraction rather than CPython binary floating exponentiation. It contributes to the same numeric bridge; the end-to-end witness below shows the combined bridge is false. |
| S30 / 142 | evaluate comparison RHS after saved LHS | Correct left-to-right order for the used single-link comparisons. |
| S31 / 143 | integer `<=` | Correct. |
| S32 / 145 | rational `<=` fallback `[owise]` | Correct for internal exact rationals; float inputs are unsupported. |
| S33 / 152 | recognize/evaluate built-in `round(E,2)` | Bypasses general name lookup, but the module does not shadow `round`; correct binding on this program. |
| S34 / 153 | exact `VSqrt` round becomes `VRounded(sqrtHundredths(R))` | Result-bearing operational abstraction. It feeds the final postcondition directly and has no universal K connection theorem to CPython `pow` plus `round`. The precision-loss witness shows the bridge admits a false real-program conclusion. |
| S35 / 154 | `round` of an integer returns that integer | Matches Python for this narrow case; unused by the area path. |
| S36 / 161 | concrete `sqrtHundredths(R)` starts exact scaled search | Ground-only simplification. It is not exercised symbolically in the universal claim, whose RHS repeats the same symbol. LLVM concrete execution leaves this function stuck; Haskell executes it. |
| S37 / 165 | stop upper-bound search when `R < H^2` | Correct under the reached invariant `R >= 0, H > 0`. |
| S38 / 168 | double upper bound when `R >= H^2` | Disjoint/complementary with S37 and terminating under the reached invariant. |
| S39 / 172 | bisection base `H-L <= 1` returns `L` | Correct under the reached floor-square invariant. |
| S40 / 174 | bisection chooses upper half when midpoint square `<= R` | Correct and decreases interval under the reached invariant. |
| S41 / 178 | bisection chooses lower half when `R <` midpoint square | Complementary to S40 and decreases interval. |
| S42 / 183 | round up above midpoint | Correct exact nearest-hundredth test. |
| S43 / 185 | round down below midpoint | Correct and disjoint from S42. |
| S44 / 187 | exact tie and even `L`: keep `L` | Correct ties-to-even for the exact mathematical square root. |
| S45 / 190 | exact tie and odd `L`: increment | Correct and exhaustive with S42–S44. |

S37–S45 are truthful for the invariant established by the sole call from S36.
Outside that call discipline, negative `R` is treated as though its square root
rounded to zero, and nonpositive upper bounds can fail to descend. No valid
triangle reaches those cases, so this is recorded as an out-of-scope reuse and
coverage gap, not as a separate intended-domain unsoundness claim.

## Every rule in `verification.k`

| ID / line | Rule | Static assessment |
|---|---|---|
| V1 / 13 | `heronRadicand(A,B,C)` exact rational Heron product | A truthful mathematical formula and consistent with the K semantics' exact arithmetic. It does not describe CPython's intermediate binary64 values after `/`; all universal-valid claims depend on this mismatch. |
| V2 / 19 | `solutionProgram => Module(...)` | After whitespace normalization, the literal is exactly the trusted-translator output in `solution.mpy`. This pins the actual submitted AST rather than a substitute. |

## Used-construct coverage

| `solution.mpy` construct | Declaration and behavior |
|---|---|
| `Module`, statement list | Syntax 1–3; S1–S3 |
| `FuncDef`, `Params`, string lists | Syntax 3–4; S4–S7 |
| three no-else `If` nodes | Syntax 3 and comparison syntax; S8–S10, S30–S32 |
| `Assign(Name(...),...)` | Syntax 3 and 5; S11–S12, S17 |
| `Return` including early return | Syntax 3; S13–S14 |
| `Int`, `Float(0.5)`, `Name` | Syntax 5; S15–S17 |
| `UnaryOp("-")` | Syntax 6; strict heating, S18 |
| `BinOp` `+`, `-`, `*`, `/`, `**` | Syntax 6; left-to-right heating, S22–S29 |
| `Compare(...,CmpOp("<=",...))` | Syntax 6–7; S30–S32 |
| `Call(Name("round"),...,Int(2))` | Syntax 5 and expression lists; S33–S45 |

Thus the AST is syntactically covered, but semantic coverage is not faithful to
the actual Python numeric model. Valid floating-point side inputs also stop at
`BinOp("+",VFloat(...),VFloat(...))`, while both Python implementations return
normally for `(0.5,0.5,0.75)`.

## False-conclusion witness and state footprint

For `A=B=10^16, C=1`, all three formal inequalities are true. CPython evaluates
`(A+B+C)/2` as binary64 `10^16`, losing the half-unit, so `s-A` is `0.0` and
both the trusted canonical and submitted function return `0.0`.

S28 instead creates exact rational `10^16 + 1/2`; S27, S29, S34, and S36–S45
then compute the exact Heron area and the K execution terminates with
`VRounded(500000000000000000)`, interpreted as
`5000000000000000.00`. A specialized reachability claim for that result also
closes with `#Top`. The bridge changes the observable `<result>` cell; it is
therefore a concrete false conclusion on the candidate's own universal formal
domain, not merely a missing proof or unused-rule concern.

All control rules read/write only `<k>` plus the stated `<env>`, `<functions>`,
or `<result>` cells. There is no heap, allocation, output, or exception cell.
That omission is material for unbounded valid integers: CPython may return
`inf` or raise `OverflowError`, whereas the K model has neither outcome.
