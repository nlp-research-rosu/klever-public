# Exhaustive local K inventory and static judgments

Source reviewed: clean copies at `/tmp/audit-work/reconstruction/semantic.k`,
`verification.k`, and `spec.k`. There are no other candidate K helper files.

## `semantic.k`: syntax, configuration, attributes, and opaque terms

- Lines 7–22 declare the submitted IR constructors: `Module(Stmts)`;
  `Params(String)`; expression constructors `Int`, `Name`, `BinOp`, `Compare`,
  `TupleExpr`; `CmpOp`; statement constructors `FuncDef`, `Assign`, `If`,
  `Return`; and the juxtaposed `Stmts` list. These are exactly the constructor
  kinds used by `solution.mpy`; no used constructor is missing.
- Lines 31–40 declare value constructors `VInt`, `VBool`, `VTuple`, return
  markers `noReturn` and `returned`, and control terms `run`, `exec`, and
  `finish`.
- Lines 42–47 configure `<mpy>` with `<k>`, `<env>`, and `<return>` cells. The
  source subset needs no heap, I/O, exception, or allocation cell.
- Lines 49–52 declare four partial K functions: `eval`, `lookupValue`,
  `getInt`, and `getBool`. None is declared `[total]` or `[functional]`; there
  are no simplification, `owise`, priority, macro, or anywhere rules.
- The zero-argument `[symbol]` attributes mark algebraic constructors and
  control markers. They do not create fresh values or oracles. The compiler
  warns that this old spelling omits `klabel`, but compilation succeeds and
  the attribute does not assert an equation.

## `semantic.k`: every rule

1. Line 54, `getInt(VInt(I)) => I`: truthful projection; every program use
   receives `VInt`.
2. Line 55, `getBool(VBool(B)) => B`: truthful projection; every condition is
   a modeled comparison producing `VBool`.
3. Line 57, `eval(Int(I), _) => VInt(I)`: faithful integer literal.
4. Line 58, `lookupValue((X |-> V) REST, X) => V`: faithful lookup of the
   unique Map binding for `X`; all reachable program reads are bound.
5. Line 59, `eval(Name(X), ENV) => lookupValue(ENV,X)`: faithful name lookup.
6. Line 61, binary `+`: faithful unbounded-integer addition.
7. Line 63, binary `-`: faithful unbounded-integer subtraction.
8. Line 65, binary `*`: faithful unbounded-integer multiplication.
9. Line 67, binary `//`: uses `/Int`. Every reachable dividend is
   nonnegative and every divisor is a positive literal (2, 10, 11, 100), so K
   integer division agrees with Python floor division on the theorem domain.
10. Line 69, binary `%`: every reachable dividend is nonnegative and modulus
    is positive (2 or 10), so K modulus agrees with Python.
11. Line 72, comparison `<`: faithful integer comparison.
12. Line 74, comparison `<=`: faithful integer comparison.
13. Line 76, comparison `>`: faithful integer comparison.
14. Line 78, comparison `>=`: faithful integer comparison.
15. Line 80, comparison `==`: faithful integer equality for the integer-only
    uses in this program.
16. Line 83, tuple evaluation: faithfully evaluates the two pure expressions
    to a two-component tuple. The source operands have no effects, so recursive
    function evaluation does not lose an observable ordering effect.
17. Lines 85–88, `run`: matches the exact module shape, function binding
    `"even_odd_palindrome"`, and parameter `"n"`; installs `n`, resets the
    local environment/return state, executes the real body, then schedules
    `finish`. The source module has only this side-effect-free definition, so
    omitting a separate module-definition step is inert.
18. Line 90, `exec(.Stmts) => .`: consumes an empty statement list.
19. Lines 91–92, returned-state `exec`: discards a scheduled statement list
    after return. On the overlap with empty statements it agrees with rule 18.
20. Lines 94–96, assignment: evaluates the pure RHS in the old environment,
    updates the named local, and continues with the exact tail.
21. Lines 98–102, true `If`: evaluates the supported Boolean guard, runs the
    true list, then the original tail.
22. Lines 103–107, false `If`: complementary to rule 21 and preserves the
    same tail.
23. Lines 109–111, `Return`: evaluates the expression, records it, and drops
    statements in the current list. Rule 19 drops any separately scheduled
    outer suffix, matching Python function return control.
24. Lines 113–114, `finish`: exposes the recorded return value at the front of
    `<k>` and restores `noReturn`; it neither fabricates nor changes the value.

The arithmetic/operator rules are disjoint by literal operator. The two `If`
guards are Boolean complements. Statement rules either use disjoint head
constructors or disjoint return states. No semantic rule encodes a palindrome
count, bypasses a used source statement, or introduces an unconstrained value.

## `verification.k`: declarations and opaque terms

- Lines 6–67 declare the partial function `solutionProgram` and its single
  equation. Its RHS is an exact constructor alias for the trusted regenerated
  `solution.mpy`, as mechanically checked in `09-program-term-identity.log`.
  It names data; it does not replace execution.
- Lines 71–73 declare partial functions `reverseDigits`, `evenPalindrome`,
  and `oddPalindrome`. No function is `[total]` or `[functional]`; no
  simplification, priority, macro, opaque fresh-value, or anywhere declaration
  exists.
- Lines 94–96 declare harness KItems `verifyRange`, `expect`, and `verified`.
  `expect` is a blocking result check and `verified` is the terminal marker;
  neither has an unconstrained interpretation that affects a result.

## `verification.k`: every rule

1. Lines 8–67, `solutionProgram`: exact program-term alias; accepted as a
   definitional summary, not an operational bridge.
2. Lines 75–76, one-digit `reverseDigits`: identity for `0 <= N < 10`.
3. Lines 77–78, two-digit `reverseDigits`: correct reversal for
   `10 <= N < 100`, including a trailing zero.
4. Lines 79–82, three-digit `reverseDigits`: correct hundreds/tens/ones
   reversal for `100 <= N < 1000`.
5. Line 83, `reverseDigits(1000) => 1`: exact boundary value.
   Rules 2–5 have disjoint guards and cover every oracle use `1..1000`.
6. Lines 85–86, `evenPalindrome(N) => 1`: returns one exactly for an even
   palindrome.
7. Lines 87–88, its complement returning zero.
8. Lines 89–90, `oddPalindrome(N) => 1`: returns one exactly for an odd
   palindrome on the positive domain.
9. Lines 91–92, its complement returning zero. Each positive/complement pair
   is disjoint and exhaustive once `reverseDigits` reduces.
10. Lines 98–104, active `verifyRange`: for `N <= MAX`, executes `P` at `N`,
    requires its returned tuple to equal the cumulative reference counts
    through `N`, then advances by one with those same increments.
11. Lines 106–107, completed `verifyRange`: produces `verified` only after
    `N > MAX`; its guard is disjoint from rule 10.
12. Lines 109–110, `expect`: removes only an exactly matching returned tuple
    and clears the local environment for the next independent call. Any wrong
    even or odd component remains stuck. Genuine `finish` has already restored
    `<return>` to `noReturn`.

The harness rules are proof machinery, not source-language rules. They do not
accelerate or replace `run(P,N)`: the active rule places the actual run ahead
of `expect`, and `expect` cannot fire until normal execution yields the exact
tuple. The only proof-side mathematical boundary is the explicitly defined
digit-reversal oracle, whose guarded equations are elementary and whose finite
domain is independently checked against the trusted canonical implementation.

## `spec.k`: claim

The sole claim (lines 6–12) starts at the exact ground state
`verifyRange(solutionProgram,1,1000,0,0)` with an empty environment and
`noReturn`, and requires the exact terminal marker `verified` with those cells
restored. There is no `requires`, `ensures`, existential RHS variable, framed
cell, or implication. The precondition is satisfiable by the literal initial
configuration. Although the final tuple is checked internally rather than
placed on the claim RHS, every executed call must pass the exact two-component
`expect` rule before the range can advance.
