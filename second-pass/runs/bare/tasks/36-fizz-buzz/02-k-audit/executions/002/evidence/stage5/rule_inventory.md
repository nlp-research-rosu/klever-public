# Exhaustive local declaration and rule inventory

Scope: fresh scratch copies of `semantic.k`, `verification.k`, and `spec.k`.
There are no generated helper K files. Imported `domains.md` and K builtin
modules are recorded as the primitive trust boundary, not candidate-local
rules.

## `semantic.k`: syntax and configuration

1. `Program ::= Module(Stmts)`: the submitted top-level constructor.
2. `Stmts ::= List{Stmt, ""}`: ordered, separator-free statement sequence,
   including `.Stmts`.
3. `Stmt ::= FuncDef(String, Params(String), Stmts)`: the submitted one-argument
   function definition shape.
4. `Stmt ::= Assign(Expr, Expr)`.
5. `Stmt ::= While(Expr, Stmts)`.
6. `Stmt ::= If(Expr, Stmts, Stmts)`.
7. `Stmt ::= Return(Expr)`.
8. `Expr ::= Name(String)`.
9. `Expr ::= Int(Int)`.
10. `Expr ::= Bool(Bool)`.
11. `Expr ::= BinOp(String, Expr, Expr)`.
12. `Expr ::= Compare(Expr, CmpOp)`.
13. `Expr ::= BoolOp(String, Expr, Expr)`.
14. `CmpOp ::= CmpOp(String, Expr)`.
15. Continuations: `assignTo`, `binLeft`, `binRight`, `compareLeft`,
    `compareRight`, `orElse`, `ifThenElse`, `whileBody`, and literal
    `returnValue`.
16. Configuration: `<fizz>` contains `<k>` program, integer `<input>`, map
    `<env>`, and integer `<result>` initialized to zero. Each cell is read or
    changed by a local rule or appears in the theorem.

No syntax declaration is `[function]`, `[total]`, `[functional]`,
`[simplification]`, `[priority]`, or opaque in this module.

## `semantic.k`: all 27 ordinary operational rules

1. Module entry matches exactly `fizz_buzz(n)`, starts its actual body, and
   initializes the four locals. Extra initialization of `x` is unobservable
   before its first read in this program and supplies the explicit model state.
2. Nonempty statement sequence schedules its head before its tail.
3. Empty statement sequence becomes `.K`.
4. `Name(X)` reads the exact map binding.
5. Assignment schedules RHS evaluation before the update.
6. Integer assignment updates the existing exact binding.
7. Binary operation schedules the left operand.
8. After the left integer, binary operation schedules the right operand.
9. `+` uses unbounded K integer addition.
10. `%` uses K integer remainder when divisor is nonzero.
11. `//` uses K integer division when divisor is nonzero.
12. Comparison schedules the left operand.
13. After the left integer, comparison schedules the right operand.
14. `<` returns the corresponding Boolean.
15. `>` returns the corresponding Boolean.
16. `==` returns the corresponding Boolean.
17. Binary `or` schedules only its left operand first.
18. A true left `or` result short-circuits to true.
19. A false left `or` result schedules the right operand.
20. `If` schedules its guard.
21. A true guard selects the then-statements.
22. A false guard selects the else-statements.
23. `While` schedules its guard.
24. A true while guard schedules body then the same loop.
25. A false while guard terminates the loop.
26. `Return` schedules its expression.
27. The integer return result clears the remaining function computation and
    writes `<result>`, preserving the other cells.

All evaluation rules are left-to-right. No priorities, simplifications,
opaque symbols, or operational proof bridges occur. Rules 10 and 11 are used
only with nonnegative dividends and positive literal divisors in the submitted
program, where K and Python arithmetic coincide. The broad return rule has the
correct abrupt-control effect for the only modeled, top-level function.

## `verification.k`: functions, equations, simplification, and macros

1. `fizzEnd(Int) [function,total]`: two disjoint, exhaustive equations,
   `N < 0 -> 0` and `N >= 0 -> N`.
2. `digitSevens(Int) [function,total]`: three disjoint, exhaustive equations.
   Nonpositive inputs map to zero. Positive inputs divide by ten and add one
   exactly when the removed base-10 digit is seven. Positive recursion strictly
   decreases.
3. `fizzContribution(Int) [function,total]`: three disjoint, exhaustive
   equations partition multiples of 11, nonmultiples of 11 that are multiples
   of 13, and all remaining integers.
4. `fizzFrom(Int,Int) [function,total]`: two disjoint, exhaustive equations.
   It is zero at/after the endpoint and otherwise adds the current contribution
   and increments the start. The recursive distance to `N` strictly decreases.
5. `(A +Int B) +Int C => A +Int (B +Int C) [simplification]`: true
   associativity over mathematical integers, oriented toward right association.
   The number of additions nested on a left spine decreases. It neither
   changes a program constructor nor supplies a result oracle.
6. `INNER-LOOP [macro]`: exact constructor expansion of submitted
   `solution.mpy` lines 11–15.
7. `OUTER-LOOP [macro]`: exact constructor expansion of submitted
   `solution.mpy` lines 5–17, invoking the exact inner macro.

There are four total function declarations, ten ordinary function-defining
equations (two `fizzEnd`, three `digitSevens`, three `fizzContribution`, and
two `fizzFrom`), one simplification equation, and two compile-time macro
expansion rules: thirteen local rules total. There are no `[functional]`
declarations, priority rules, opaque symbols, fresh values, or operational
rules that rewrite execution to a summary.

## `spec.k`: three reachability claims

1. Inner-loop circularity: for `X >= 0`, the exact loop followed by arbitrary
   `REST` preserves `REST`, `i`, and `n`, sets `x` to zero, and adds
   `digitSevens(X)` to `count`.
2. Outer-loop circularity: for `0 <= I <= N` and `x = 0`, the exact loop
   followed by arbitrary `REST` preserves `REST` and `n`, sets `i` to `N`,
   restores `x = 0`, and adds `fizzFrom(I,N)` to `count`.
3. Entry claim: for every K integer `N` (no precondition), executing the exact
   submitted module from the initial configuration terminates its computation,
   binds the four modeled locals, and returns `fizzFrom(0,N)`.

The loop claims summarize exact fixed-semantics configurations and are proved
as reachability circularities; they are not semantic shortcut rules. The entry
claim depends on both. Ground satisfying witnesses and macro-expanded KORE
identity are recorded in stage 4 evidence.

## Construct coverage map

- `Module`/`FuncDef`: entry rule 1.
- Ordered statement lists and empty branches: rules 2–3.
- `Assign`/`Name`/`Int`: rules 4–6.
- `BinOp("+","%","//")`: rules 7–11.
- `Compare("<",">","==")`: rules 12–16.
- `BoolOp("or")`: rules 17–19.
- `If`: rules 20–22.
- `While`: rules 23–25.
- `Return`: rules 26–27.

Concrete runs at negative/zero inputs and at `N=78` collectively exercise
module entry, assignments, all three binary operators, all three comparisons,
both `or` outcomes (including short circuit), both `if` outcomes, both loop
outcomes, empty statement lists, and return. No submitted constructor is
unmapped.

## Static conclusion

Every local equation is true on its complete guard; total-function guards are
complete and pairwise disjoint; recursive equations descend; the sole
simplifier is ordinary integer associativity. Every operational rule agrees
with the submitted program on every integer input. No rule encodes the task
answer, fabricates a used result, replaces program execution with an oracle, or
admits a concrete false conclusion on the intended domain. Therefore no
unsoundness witness exists to report. The language is intentionally minimal
and would reject unsupported Python constructors; missing unused Python
semantics is outside the generated-semantics requirement.
