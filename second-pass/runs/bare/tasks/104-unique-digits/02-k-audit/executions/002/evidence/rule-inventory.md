# Local declaration and rule inventory

The scan source is `stage5-declaration-scan.log`. There are no candidate helper
K files. `semantic.k` contains 16 local rules; `verification.k` contains six;
`spec.k` contains five positive claims.

## `semantic.k`: syntax and configuration

1. `Program`: `Module(Stmts)` and nullary `solutionProgram`. Only
   `solutionProgram` has attributes: `[function, total]`.
2. `Stmts`: generated empty-separated `List{Stmt, ""}`.
3. `Stmt`: `FuncDef(String, Params, Stmts)`,
   `If(Expr, Stmts, Stmts)`, and `Return(Expr)`.
4. `Params`: `Params(Strings)`; `Strings` is `List{String, ","}`.
5. `Expr`: `Name(String)`, `Int(Int)`, `Bool(Bool)`,
   `BinOp(String, Expr, Expr)`, `Compare(Expr, CmpOps)`,
   `Call(Expr, Exprs)`, and `ListComp(Expr, CompFors)`.
6. `Exprs`: `List{Expr, ","}`.
7. `CmpOp`: `CmpOp(String, Expr)`; `CmpOps` is
   `List{CmpOp, ","}`.
8. `CompFor`: `CompFor(Expr, Expr, Exprs)`; `CompFors` is
   `List{CompFor, ""}`.
9. `IntSeq`: `.Ints` and `cons(Int, IntSeq)`.
10. `PyVal`: `pyList(IntSeq)` and `pyBool(Bool)`.
11. `KItem`: `invoke(String, PyVal)`.
12. The sole configuration cell is
    `<k> $PGM:Program ~> invoke("unique_digits", $ARGS:PyVal) </k>`.
    There are no environment, local-variable, stack, iterator, allocation,
    exception, heap, or output cells. No source value sort is declared a
    `KResult`.

These declarations parse all constructors in `solution.mpy`, but parsing is
their only treatment. There are no evaluation rules for `Module`, `FuncDef`,
`If`, `Return`, `Name`, AST `Int`/`Bool`, `BinOp("%", ...)`,
`BinOp("//", ...)`, `Compare`/`CmpOp("==", ...)`, `Call`,
`ListComp`, or `CompFor`. In particular there is no binding/lookup, argument
evaluation, call/return, recursion, comprehension iteration, or `sorted`
builtin rule.

## `semantic.k`: functions and rules

1. `solutionProgram` equation, lines 51–66. The one nullary case expands to
   the exact submitted constructor tree (with empty statement-list
   normalization). This is a truthful definitional alias and its `[total]`
   coverage is complete. Although its comment calls it a macro, it has no
   `[macro]` attribute.
2. `isUniqueDigitsProgram`, lines 68–85, is `[function]`, not `[total]`.
   Its single exact-tree equation returns `true`. It is a sound partial
   syntactic recognizer; no result is specified for any other program.
3. `oddDigits`, `[function, total]`, has four disjoint and exhaustive integer
   cases:
   - line 91: negative `N` returns `false`;
   - line 92: zero returns `true`;
   - lines 93–94: positive even `N` returns `false`;
   - lines 95–96: positive odd `N` recurses on `N /Int 10`.
   The recursion descends for positive integers and correctly computes the
   candidate helper's intended decimal predicate on positive inputs. Direct
   negative and zero inputs are outside the source contract: the negative rule
   does not model CPython recursion, while zero is used as the recursive
   sentinel and matches the submitted helper but not the canonical
   string-of-digits property for a direct zero.
4. `filterOddDigits`, `[function, total]`, has three rules: empty; retain the
   head when `oddDigits(N)`; drop it under `notBool oddDigits(N)`. Structural
   descent, multiplicity preservation, guard disjointness, and coverage hold.
5. `insertSorted`, `[function, total]`, has three rules: insert into empty;
   insert before a head under `N <=Int M`; recur after the head under
   `N >Int M`. The guards are disjoint/exhaustive and recursion descends.
6. `sortInts`, `[function, total]`, has empty and nonempty structural rules;
   the latter insertion-sorts the tail.
7. `uniqueDigitsMeaning`, `[function, total]`, has one equation:
   `sortInts(filterOddDigits(NS))`.
8. The ordinary operational rule at lines 119–121 rewrites
   `P:Program ~> invoke("unique_digits", pyList(NS))`, under the exact-tree
   recognizer, directly to `pyList(uniqueDigitsMeaning(NS))`, while framing an
   arbitrary `<k>` suffix. It reads the program and input and rewrites the only
   cell. It is an operational bridge, not source-language semantics.

No local priority, `owise`, simplification, macro, alias, context, opaque, or
explicit `functional` declaration exists. The `[function]` equations are
functional by their K role.

The operational bridge has no bridge-free connection theorem. There is no
fixed evaluator in this definition from which such a theorem could be proved.
It skips module binding, both function bodies, every branch and recursive call,
the comprehension, and sorting. Its result influences the final result and is
defined by the same `oddDigits`/filter/sort vocabulary to which the
postcondition reduces. The context probe in `stage5-bridge-context.k` confirms
that its `...` accepts a trailing computation. The concrete intended-domain
false-conclusion witness is a list containing the positive 995-digit integer
made entirely of `1`: the bridge returns that integer normally, while the
submitted CPython body raises `RecursionError`; see
`stage3-concrete-compare.log`. Thus the bridge can prove a false normal-return
conclusion about the real generated program.

## `verification.k`: functions and rules

1. `positiveInts`, `[function, total]`: empty returns `true`; a `cons` returns
   `N >Int 0 andBool positiveInts(NS)`. Structural, complete, and truthful.
2. `allDecimalDigitsOdd`, `[function, total]`: the sole equation aliases
   `oddDigits`.
3. `retainAllOddDigitItems`, `[function, total]`: aliases
   `filterOddDigits`.
4. `inIncreasingOrder`, `[function, total]`: aliases `sortInts`.
5. `uniqueDigitsSpec`, `[function, total]`: aliases
   `inIncreasingOrder(retainAllOddDigitItems(NS))`.

The aliases are terminating and total, but they do not independently
characterize membership or sortedness. They deliberately reduce the
postcondition to the same filter/sort term used by the operational bridge.
Consequently they constrain a result, but they do not establish a connection
between that result and source execution.

There are no priorities, simplifications, ordinary operational rules, opaque
symbols, or auxiliary execution claims in `verification.k`.

## `spec.k`: positive claims

1. Universal entry claim for every `IntSeq NS` satisfying `positiveInts(NS)`,
   with exact result `pyList(uniqueDigitsSpec(NS))`.
2. Ground `allDecimalDigitsOdd(97531) => true`.
3. Ground `allDecimalDigitsOdd(1422) => false`.
4. First prompt example with exact output `[1, 15, 33]`.
5. Second prompt example with exact empty output.

Claims 2 and 3 are summary-function checks, not executions of the submitted
`no_even_digit` body. There are no helper execution, loop, invariant,
connection, or derived-lemma claims.

## Imported trust boundary

The local files import K's `INT`, `BOOL`, string syntax, K sequences,
configuration initialization, and generated list productions. The proof trusts
unbounded mathematical integers, integer comparison/division/remainder,
Boolean operations, constructor matching, and generated collection plumbing.
These low-level primitives are acceptable as ordinary K infrastructure. They
do not justify the whole-program bridge or model CPython's recursion limit and
exceptions.
