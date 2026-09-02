# Reviewer rule inventory

This inventory covers every local declaration in the candidate's
`semantic.k` and `verification.k`. Imported K `INT`, `BOOL`, and `STRING`
domains are recorded as trusted primitives rather than local rules.

## `semantic.k`: syntax and configuration

- `Program`: `Module(Stmt)`.
- `Stmt`: `FuncDef(String, Params, Stmt)` and `Return(Expr)`.
- `Params`: `Params(String)`.
- `Expr`: `Name(String)`, `Int(Int)`, `BinOp(String, Expr, Expr)`,
  `BoolOp(String, Expr, Expr)`, and `Compare(Expr, CmpOp)`.
- `CmpOp`: `CmpOp(String, Expr)`.
- `Value`: `IntValue(Int)` and `BoolValue(Bool)`.
- `Result`: `noResult` or a `Value`.
- Configuration: `<mpy>` contains `<k> Program`, `<input> Int`, and
  `<result> Result`.
- The constructor productions have only `[symbol(...)]` attributes. There
  are no local priority, associativity, strictness, simplification, opacity,
  `functional`, or `total` declarations.

Every submitted constructor is covered: `Module`, `FuncDef`, `Params`,
`Return`, `BoolOp("and",...)`, `Compare`, `Name`, `Int`, `BinOp("%",...)`,
and `CmpOp` with `">="` or `"=="`.

## `semantic.k`: rules and functions

1. Entry harness: the exact one-function module named
   `is_equal_to_sum_even` consumes `<k>`, reads `<input> N`, and changes
   `noResult` to `eval(E, X, N)`. It preserves `<input>` and has no other
   state cells.
2. `eval(Name(X), X, N) => IntValue(N)`.
3. `eval(Int(I), _, _) => IntValue(I)`.
4. `eval(BinOp(OP,L,R),X,N)` delegates to `evalBin(OP,eval(L),eval(R))`.
5. `evalBin("%",IntValue(I),IntValue(J)) => IntValue(I %Int J)` when
   `J =/=Int 0`.
6. `eval(Compare(L,CmpOp(OP,R)),X,N)` delegates to `evalCompare`.
7. Integer `">="` delegates to K `>=Int`.
8. Integer `"=="` delegates to K `==Int`.
9. `eval(BoolOp(OP,L,R),X,N)` delegates to `evalBool`.
10. Boolean `"and"` delegates to K `andBool`.

`eval`, `evalBin`, `evalCompare`, and `evalBool` are `[function]`, but not
`[total]`. Their intentional partiality leaves unsupported constructors,
operators, wrong types, unbound names, and division by zero stuck.

The recursive evaluator is eager, whereas Python `and` is short-circuiting.
For this exact submitted body, the right operand is the pure, total expression
`n % 2 == 0` with constant nonzero divisor `2`; it has no state, control,
exception, or allocation effect. Therefore eagerness produces the same result
and observable state over every intended integer input. This is not asserted
for other bodies.

## `verification.k`

1. `sumFourPositiveEvens(Int) : Bool [function,total]` has one unguarded
   equation to `N >=Int 8 andBool N %Int 2 ==Int 0`. The equation covers all
   `Int` inputs, does not recurse, and merely defines the symbol.
2. `canonicalWitnessesAreValid(Int) : Bool [function,total]` has one
   unguarded equation spelling out positivity, evenness, and sum equality for
   `(N - 6, 2, 2, 2)`. It covers all `Int` inputs, does not recurse, and merely
   defines the symbol.
3. `checkCanonicalWitnesses(Int) : KItem` has one operational rule that
   consumes the proof-local checker and changes `noResult` to
   `BoolValue(canonicalWitnessesAreValid(N))`. It preserves `<input>`. This
   defines a proof-local arithmetic checker; it does not match, replace, or
   preempt any submitted-program term.

There are no opaque symbols, fresh values, priorities, `[simplification]`
rules, derived rewrite lemmas, or overlapping equations. Both `[total]`
functions have unconditional exhaustive equations. No local rule has an
identified false conclusion on its match domain.
