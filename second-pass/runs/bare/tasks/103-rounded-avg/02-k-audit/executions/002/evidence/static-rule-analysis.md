# Static rule inventory and audit notes

This inventory was reconstructed from the source files copied from `/candidate`;
it does not rely on the candidate's report or compiled artifacts. Line references
are to the immutable candidate sources.

## Local syntax and declarations

`semantic.k` module `MPY-SYNTAX`:

- `Module`: `Module(Stmts)`.
- `Stmts`: zero-or-more `Stmt` list with an empty separator.
- `Stmt`: `FuncDef(String, Params, Stmts)`, `If(Expr, Stmts, Stmts)`,
  and `Return(Expr)`.
- `Params`: `Params(Strings)`.
- `Strings`: comma-separated `String` list.
- `Expr`: `Int(Int)`, `Name(String)`, `UnaryOp(String, Expr)`,
  `BinOp(String, Expr, Expr)`, `Compare(Expr, CmpOps)`, and
  `Call(Expr, Exprs)`.
- `Exprs`: comma-separated `Expr` list.
- `CmpOp`: `CmpOp(String, Expr)`.
- `CmpOps`: comma-separated `CmpOp` list.

`semantic.k` module `SEMANTIC`:

- `PyVal`: `intVal(Int)`, `boolVal(Bool)`, `ratVal(Int, Int)`,
  and `binVal(Int)`.
- `Result`: `noResult` and `result(PyVal)`.
- `KItem`: `boot(Module, Int, Int)`, `exec(Stmts)`, `execStmt(Stmt)`,
  `choose(Stmts, Stmts)`, and `doReturn`.
- Function productions, all carrying `[function]`: `eval(Expr, Map)`,
  `unary(String, PyVal)`, `binary(String, PyVal, PyVal)`,
  `compare(String, PyVal, PyVal)`, `callBuiltin(String, PyVal)`,
  and `roundValue(PyVal)`.
- Configuration: one `<py>` cell containing `<k>`, `<env>`, and `<result>`.

`verification.k`:

- Function constant `roundedAvgProgram : Module`.
- Functions `renderBinary(PyVal) : String` and
  `unsignedBits(Int) : String`.

There are no local `[total]`, `[functional]`, `[simplification]`, priority,
or opaque declarations. Imported K `INT`, `BOOL`, `STRING`, and `MAP`
operations are trusted primitives.

## Constructor coverage for `solution.mpy`

The submitted term uses `Module`, `FuncDef`, `Params`, `Stmts`, `If`,
`Compare`, `CmpOp`, `Name`, `Return`, `UnaryOp`, `Int`, `Call`, `Exprs`, and
`BinOp`. Each has local syntax. Its execution uses the boot, sequencing,
if/choose, return, expression traversal, unary-minus, integer-addition,
integer-greater-than, division, round, and bin rules inventoried below.
No used constructor lacks a rule.

## `semantic.k` rules

1. Lines 67–69, `boot`: for the one accepted top-level two-argument
   `rounded_avg` binding, binds its two formal names to `intVal(N/M)` and
   executes the exact body. This reads/writes `<k>` and `<env>` and preserves
   `<result>`. Faithful for the submitted singleton module.
2. Line 71, `exec(.Stmts)`: terminates an empty statement list. Faithful.
3. Line 72, `exec(S REST)`: executes the head before the tail. Faithful.
4. Lines 74–76, `If`: evaluates its condition in the current environment and
   then schedules `choose`. Faithful for the pure expressions in this program.
5. Line 77, true `choose`: selects the then branch. Faithful.
6. Line 78, false `choose`: selects the else branch. Faithful. Rules 5 and 6
   are disjoint and cover Boolean conditions.
7. Lines 80–81, `Return`: evaluates the return expression and schedules
   `doReturn`. Faithful.
8. Lines 82–83, `doReturn`: discards the remaining computation and writes the
   result. This is the intended abrupt effect of a top-level function return;
   the minimal semantics has no caller, exception, output, heap, or stack cell.
9. Line 85, `eval(Int)`: injects an integer literal. Faithful.
10. Line 86, `eval(Name)`: retrieves the matching map binding. Faithful for
    the unique `n` and `m` bindings established by rule 1.
11. Line 87, `eval(UnaryOp)`: structurally evaluates the operand then applies
    the named unary operation. Faithful on the used pure operand.
12. Lines 88–89, `eval(BinOp)`: structurally evaluates both operands then
    applies the named binary operation. The source language is left-to-right;
    the order is not observable for the submitted pure, non-mutating operands.
13. Lines 90–91, one-element `eval(Compare)`: evaluates the two operands and
    applies the named comparison. Faithful for the submitted single `>`.
14. Line 92, unary `Call(Name(F), E)`: evaluates the argument and dispatches
    a named builtin. It intentionally pins the standard `round` and `bin`
    bindings; this is faithful for the submitted function, whose environment
    cannot shadow those names, but is not a reusable model of general Python
    name lookup.
15. Line 94, unary `-` on `intVal`: ordinary integer negation. Faithful.
16. Line 95, binary `+` on integer values: ordinary arbitrary-precision
    integer addition. Faithful.
17. Lines 96–97, binary `/` on integer values: replaces Python true division
    (which produces an IEEE-754 binary64 `float` or raises overflow) with the
    exact value `ratVal(I,J)`. **Materially unsound for the actual submitted
    Python program over the claimed domain.** Witness:
    `N=M=9007199254740993` satisfies the `integral-midpoint` claim. Python
    evaluates `(N+M)/2` to `9007199254740992.0` and returns that integer's
    binary string, while this rule preserves the exact rational and the K run
    returns `binVal(9007199254740993)`. At `N=M=10**309`, Python raises
    `OverflowError` but this rule returns a rational and the K semantics
    terminates normally. See `07-k-concrete-compare.log`.
18. Line 98, integer `>`: ordinary comparison. Faithful.
19. Line 99, `round` dispatch: forwards its semantic argument to
    `roundValue`. Locally consistent, but because rule 17 supplies an exact
    rational instead of the Python float, this dispatch participates in the
    false program conclusion witnessed above.
20. Line 100, `bin` dispatch: represents `bin(I)` as `binVal(I)`. This is an
    abstract result representation. It is exact on the intended nonnegative
    return path conditional on the renderer rules below.
21. Lines 104–105, exact-rational round-down case: for `D>0` and remainder
    below one half, returns the quotient. Mathematically valid on the reachable
    positive domain.
22. Lines 106–107, exact-rational round-up case: for remainder above one half,
    returns quotient plus one. Mathematically valid on the reachable domain.
23. Lines 108–111, exact-rational tie/even case: at a half with an even lower
    neighbor, returns the lower neighbor. Mathematically valid.
24. Lines 112–115, exact-rational tie/odd case: at a half with an odd lower
    neighbor, returns the upper neighbor. Mathematically valid.

For reachable `I>0,D=2`, rules 21–24 are disjoint and exhaustive: the doubled
remainder is `<`, `>`, or `== D`, and the equality case is partitioned by
quotient parity. Their local mathematics does not repair rule 17's missing
binary64 conversion.

## `verification.k` rules

1. Lines 10–21, `roundedAvgProgram`: a definitional constant for the exact
   submitted constructor term. The independent KAST comparison reports equal
   normalized constructor trees in `11-program-pinning.log`. It does not
   summarize or bypass the body.
2. Lines 28–29, `renderBinary(binVal(I))` for `I>=0`: adds the `0b` prefix to
   `unsignedBits(I)`. Truthful for Python's nonnegative `bin`.
3. Line 30, `unsignedBits(0)`: returns `"0"`. Truthful.
4. Line 31, `unsignedBits(1)`: returns `"1"`. Truthful.
5. Lines 32–33, `unsignedBits(I)` for `I>=2`: recurses on `I/2` and appends
   the remainder bit. Truthful and descending.

Rules 3–5 are pairwise disjoint and, with rule 2's guard, cover every
nonnegative payload. The universal entry claims constrain an abstract
`binVal` payload; only payloads 3, 15, and 26 have separate reachability claims
to concrete strings. Thus the general `binVal`-to-Python-string interpretation
is a transparent but informal representation bridge rather than the main
problem computation.

## Claims

- `reversed`: positive `N,M` with `N>M` returns `intVal(-1)`.
- `integral-midpoint`: positive `N<=M` with even `N+M` returns
  `binVal((N+M)/2)`.
- `half-even-down`: positive `N<=M`, odd `N+M`, and even lower neighbor
  returns the lower-neighbor `binVal`.
- `half-even-up`: the corresponding odd lower-neighbor case returns the
  upper-neighbor `binVal`.
- Four ground prompt examples constrain results for `(1,5)`, `(7,5)`,
  `(10,20)`, and `(20,33)`.
- Three ground renderer claims constrain `binVal(3/15/26)` to the documented
  strings.

The four symbolic guards partition all positive pairs in the exact-rational K
model. Satisfying witnesses are respectively `(2,1)`, `(1,5)`, `(2,3)`, and
`(1,2)`. The large singleton witness above also satisfies
`integral-midpoint`, and its claimed payload disagrees with both real Python
implementations.
