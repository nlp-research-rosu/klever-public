# Exhaustive local K inventory and adjudication

This inventory covers the fresh source copies at
`/tmp/audit-work/{semantic.k,verification.k,spec.k}`. Imported K standard
modules are accounted for as primitives, not as candidate-local rules.

## Syntax and configuration

`semantic.k` lines 8–25 declare:

- `Program`: `Module(Stmts)` and the external driver
  `Run(Program, Expr, Expr)`.
- `Stmts`: an empty-separated `Stmt` list; `Strings`: a comma-separated
  `String` list.
- `Stmt`: `FuncDef(String, Params, Stmts)` and `Return(Expr)`.
- `Params`: `Params(Strings)`.
- `Expr`: `Int`, `Bool`, `Name`, `UnaryOp`, `BinOp`, `Compare`, and `IfExp`.
- `CmpOp`: the comparison-tag/comparator pair.

`semantic.k` line 34 declares the entire configuration: one `<k>` cell,
initially containing a `Program`. Lines 36–38 declare internal values `VInt`
and `VBool`, plus the immutable environment constructors `emptyEnv` and
`bind`. There are no store, heap, I/O, allocation, exception, call-stack, or
other state cells.

`verification.k` declares the constant syntax `chooseNumProgram` (line 4), the
Boolean functions `noEvenInRange` (line 22) and `chooseNumContract` (line 30),
and continuation item `checkChooseNum` (line 40).

All candidate-local attributes are `[function]`: `lookup`, `negate`,
`subtract`, `modulo`, `compare`, `truth`, `eval`, `chooseNumProgram`,
`noEvenInRange`, and `chooseNumContract`. There are no local `total`,
`functional`, `simplification`, `concrete`, `owise`, opaque, priority, or
precedence declarations. The only reachability claims are the eight entry
claims in `spec.k`; there are no helper, loop, or circularity claims.

## `semantic.k` rules

| ID | Lines | Rule | Domain/overlap review | Adjudication |
|---|---:|---|---|---|
| S1 | 41 | `lookup` matching latest name | Matches when latest key equals query. Disjoint from S2's guard. | Correct lexical lookup. |
| S2 | 42–43 | `lookup` skipping a nonmatching binding | Guard is string disequality; recursively descends to the older environment. | Correct; partial at `emptyEnv`, which is unreachable for used names. |
| S3 | 46 | `negate(VInt(I))` | Integer-only; computes `0 -Int I`. | Correct for unary minus. |
| S4 | 49 | `subtract(VInt(I),VInt(J))` | Integer-only. | Correct integer subtraction. |
| S5 | 52 | `modulo(VInt(I),VInt(J))` | Delegates to K `%Int`; no zero-divisor exception model. Actual divisor is literal positive `2`. | Correct on every submitted-program state in the intended domain; broader exceptional behavior is unmodeled. |
| S6 | 55 | `compare(">",...)` | Tag-disjoint from S7. | Correct integer greater-than. |
| S7 | 56 | `compare("==",...)` | Tag-disjoint from S6. | Correct integer equality. |
| S8 | 59 | `truth(VBool(B))` | Boolean-only. | Correct unwrapping. |
| S9 | 62 | `eval(Int(I),ENV)` | Environment intentionally ignored. | Correct literal evaluation. |
| S10 | 63 | `eval(Bool(B),ENV)` | Environment intentionally ignored; `Bool` is unused by `solution.mpy`. | Correct. |
| S11 | 64 | `eval(Name(NAME),ENV)` | Delegates to S1/S2. | Correct; `x` and `y` are both bound by S18. |
| S12 | 65 | unary-minus evaluation | Delegates to recursive evaluation and S3. | Correct on the used integer operand. |
| S13 | 66–67 | subtraction evaluation | Pure recursive operands, then S4. | Correct. Python's left-to-right order has no observable distinction here because operands are pure and total on the intended states. |
| S14 | 68–69 | modulo evaluation | Pure recursive operands, then S5. | Correct for the submitted `% 2`. |
| S15 | 70–71 | comparison evaluation | Pure recursive operands, then S6/S7. | Correct for the submitted `>` and `==`. |
| S16 | 72–73 | true conditional-expression branch | Guard requires the condition to evaluate to true; only `THEN` remains. | Correct lazy branch selection. |
| S17 | 74–75 | false conditional-expression branch | Guard is Boolean negation of S16; the guards are disjoint and exhaustive for used Boolean conditions. | Correct lazy branch selection. |
| S18 | 80–84 | `Run` sole two-argument direct-return function | Matches exactly one `FuncDef`, exactly two parameters, and exactly one `Return(E)` body; binds both integer arguments and preserves any continuation with `...`. | Correct custom entry driver for the actual translated program. It ignores the sole function's name, which is harmless for this exact direct-entry driver and claim. |

The expression-evaluation rules are equational/pure. Although there are no
strictness attributes, the only multi-operand expressions used by the program
have no side effects, allocation, I/O, or intended-domain exceptions, so
operand rewrite order cannot change the result or state. Conditional branches
are lazy because only the selected branch is placed on the right-hand side.

## `verification.k` rules

| ID | Lines | Rule | Class and scope | Adjudication |
|---|---:|---|---|---|
| V1 | 5–18 | `chooseNumProgram => Module(...)` | Definitional constant. Its complete constructor token stream is independently extracted and equals regenerated `solution.mpy`. | Correct and does not bypass execution. |
| V2 | 23–25 | `noEvenInRange(X,Y)` | Mathematical definitional summary over all K integers. | Correct: an integer interval is empty, or a nonempty interval lacks an even number exactly when it is an odd singleton. |
| V3 | 31–38 | `chooseNumContract(X,Y,R)` | Mathematical predicate, not an execution replacement. | Correct: a non-sentinel result is in range, even, and has its next even successor above `Y`; the sentinel branch uses V2. |
| V4 | 41–42 | result then `checkChooseNum` | Proof-local pure continuation construct; reads the computed `VInt`, replaces it with V3's `VBool`, and preserves any later continuation. | Correct. It runs after, rather than instead of, the submitted program. |

V2 proof: if `X>Y`, the interval is empty. If `X=Y` and `X` is odd, its sole
member is not even. Conversely, if `X<=Y` and the interval is not an odd
singleton, it is either an even singleton or has at least two consecutive
integers, one of which is even.

V3 proof: for even `R`, all larger even integers are at least `R+2`. Thus
`R<=Y<R+2` is equivalent to saying no larger even integer remains in the
interval. Together with `X<=R`, evenness, and the sentinel clause, this is the
prompt's result property on positive integer endpoints.

## Submitted-construct coverage

The regenerated `solution.mpy` uses `Module`, one `FuncDef`, two `Params`, one
`Return`, `IfExp`, `Compare`, `CmpOp` tags `>` and `==`, `Name` for `x` and
`y`, `UnaryOp` tag `-`, `BinOp` tags `%` and `-`, and integer literals `0`,
`1`, and `2`. Concrete entry uses `Run` with two `Int` arguments. Every item is
declared above and reaches S18, S9/S11–S17, and the appropriate primitive
rules. The unused local `Bool` expression production and `VBool` literal path
do not stand in for any submitted computation.

## Soundness conclusion

No local rule encodes an unproved answer in place of program execution, creates
an unconstrained result-bearing symbol, fabricates a value for an unmodeled
used construct, or has a false conclusion on the intended positive-integer
input domain. Therefore there is no unsound-rule witness to report. The
narrower limitation is that this deliberately small semantics does not model
general Python behavior (notably errors, mutation, general calls, or arbitrary
operators); those behaviors are absent from this submitted program and its
intended states.
