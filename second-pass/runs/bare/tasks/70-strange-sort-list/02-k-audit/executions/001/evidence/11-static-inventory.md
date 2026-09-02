# Exhaustive local declaration and rule inventory

Sources reviewed: `/tmp/audit-work/src/semantic.k`,
`/tmp/audit-work/src/verification.k`, and `/tmp/audit-work/src/spec.k`.
Line numbers below refer to those scratch copies.

## Attributes and special declarations

- There are 33 `syntax` declaration statements in `semantic.k` and three in
  `verification.k`.
- Twenty-one semantic symbols and all three verification symbols carry
  `[function]`.
- There are no `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
  `[priority]`, `[owise]`, `[anywhere]`, `[macro]`, or `[alias]` attributes.
- There are no opaque or fresh result symbols and no helper claims in
  `verification.k`.
- `spec.k` contains 39 unlabeled reachability claims and no rules.

## Syntax and configuration inventory

### `MPY-SYNTAX` in `semantic.k`

1. Line 7: `Module ::= Module(Stmts)`.
2. Line 9: `Stmts ::= List{Stmt, ""}`.
3. Lines 10–13: `Stmt ::= FuncDef | Assign | If | Return`.
4. Line 15: `Params ::= Params(String)`.
5. Lines 17–25: `Expr ::= Name | Int | ListExpr() | ListExpr(Expr,Expr) |
   Call | Compare | BinOp | UnaryOp | Subscript`.
6. Line 26: `CmpOp ::= CmpOp(String,Expr)`.
7. Lines 27–28: `Index ::= Expr | Slice(Bound,Bound,Bound)`.
8. Line 29: `Bound ::= Expr | NoBound`.

This is a lower, constructor-tree IR matching the trusted translator output.
Every constructor in `solution.mpy` is declared. `Assign` is declared but is
not used by the submitted program. Missing general Python syntax is outside the
chosen subset and is not silently accepted.

### Runtime values and configuration in `semantic.k`

9. Lines 41–42: `PList ::= nil | cons(Int,PList)`.
10. Lines 44–46: `PVal ::= pInt | pBool | pList`.
11. Lines 48–50: `Outcome ::= pending | normal(Map) | returned(PVal)`.
12. Line 51: `Outcome ::= PVal`.
13. Lines 53–59: `<python>` configuration containing exactly `<program>`,
    `<input>`, `<entry>`, and `<result>`.

There is no `<k>` cell. The `<result>` cell is the computation-bearing cell:
its initial `pending` term rewrites to `invoke(...)` and then to the final
`PVal`. This is a big-step functional semantics, not a conventional
small-step `<k>` semantics.

### Semantic function declarations in `semantic.k`

14. Line 67: `invoke(String,PVal,Module) : PVal [function]`.
15. Line 70: `invokeFind(String,PVal,Stmts,Module) : PVal [function]`.
16. Line 79: `returnedValue(Outcome) : PVal [function]`.
17. Line 82: `exec(Stmts,Map,Module) : Outcome [function]`.
18. Line 86: `continue(Outcome,Stmts,Module) : Outcome [function]`.
19. Line 90: `execStmt(Stmt,Map,Module) : Outcome [function]`.
20. Line 97: `branch(PVal,Stmts,Stmts,Map,Module) : Outcome [function]`.
21. Line 102: `eval(Expr,Map,Module) : PVal [function]`.
22. Line 118: `makePair(PVal,PVal) : PVal [function]`.
23. Line 121: `apply(String,PVal,Module) : PVal [function]`.
24. Line 127: `equal(PVal,PVal) : PVal [function]`.
25. Line 130: `plus(PVal,PVal) : PVal [function]`.
26. Line 133: `negate(PVal) : PVal [function]`.
27. Line 136: `index(PVal,Index,Map,Module) : PVal [function]`.
28. Line 144: `length(PList) : Int [function]`.
29. Line 148: `nth(PList,Int) : Int [function]`.
30. Line 152: `append(PList,PList) : PList [function]`.
31. Line 156: `dropLast(PList) : PList [function]`.
32. Line 161: `interior(PList) : PList [function]`.
33. Line 165: `sortInts(PList) : PList [function]`.
34. Line 169: `insertInt(Int,PList) : PList [function]`.

The declarations are intentionally partial outside the submitted program's
well-typed paths; none claims `[total]`.

### Verification function declarations in `verification.k`

35. Line 9: `solutionProgram : Module [function]`.
36. Line 33: `weaveEnds(PList) : PList [function]`.
37. Line 40: `strangeSpec(PList) : PList [function]`.

`solutionProgram` is a definitional constant. `weaveEnds` and `strangeSpec`
are result-bearing mathematical summaries, but neither replaces program
execution.

## Rule inventory and decisions

The decision “sound in scope” means the equation is true for every match
reachable from the fixed submitted program on a `PList` of mathematical
integers. A “scope gap” is not labeled unsound because no false conclusion
witness exists on that intended domain.

### Startup, lookup, calls, and control (semantic rules 1–14)

1. Lines 61–64, `pending => invoke(ENTRY,pList(INPUT),PGM)`: starts the selected
   entry with the exact program/input. Sound in scope; reads all three input
   cells and writes only `<result>`.
2. Line 68, `invoke => invokeFind`: exposes the module definitions. Definitional
   and sound.
3. Lines 71–73, matching `invokeFind`: binds the sole formal parameter to the
   argument and executes the matching body. Sound for both one-argument
   submitted functions.
4. Lines 74–77, nonmatching `invokeFind`: scans past a different function name.
   Guard is disjoint from rule 3. Sound for the fixed module, whose names are
   unique. Scope gap: a broader Python model would need “last definition wins”
   behavior for duplicate top-level names.
5. Line 80, `returnedValue(returned(V)) => V`: extracts a function return.
   Sound; every reachable submitted function path returns.
6. Line 83, `exec(.Stmts,ENV,_) => normal(ENV)`: empty suite fall-through.
   Sound.
7. Line 84, nonempty `exec`: executes the head statement and continues with the
   tail. Sound sequential composition.
8. Line 87, `continue(returned(V),...)`: propagates return and discards the
   remaining statements. Sound control effect.
9. Line 88, `continue(normal(ENV),REST,DEFS)`: continues after fall-through.
   Sound.
10. Lines 91–92, assignment: evaluates the RHS in the old environment and
    updates a named local. Sound for this reduced value language, but unused by
    `solution.mpy`.
11. Line 93, return: evaluates the expression and produces `returned`. Sound.
12. Lines 94–95, if dispatch: evaluates the condition and delegates to
    `branch`. Sound for the submitted comparisons.
13. Line 98, true branch: executes `THEN`. Sound.
14. Line 99, false branch: executes `ELSE`. Sound. Rules 13–14 are disjoint and
    cover the submitted boolean conditions.

There is no abrupt-control operational bridge in `verification.k`; rules
8–14 are the generated semantics itself. There are no output, heap, exception,
or allocation cells to preserve because the submitted program uses none.

### Expression evaluation (semantic rules 15–33)

15. Line 103, name lookup: returns the mapped `PVal`. Sound for `ordered` and
    `lst`, which are installed by rule 3. Missing-name exceptions are outside
    this subset and become stuck rather than fabricated.
16. Line 104, integer literal: maps to mathematical integer. Sound and aligned
    with arbitrary-precision Python integers.
17. Line 105, empty list literal: maps to `nil`. Sound.
18. Lines 106–107, two-element list literal: evaluates both elements and calls
    `makePair`. Sound for the only nonempty literal in the program.
19. Lines 108–109, one-argument call: evaluates the argument and calls
    `apply`. Sound for all calls in the program. Expression evaluation is pure
    here, so the functional evaluator does not hide an observable evaluation
    order.
20. Lines 110–111, integer equality comparison: evaluates operands and calls
    `equal`. Sound for the two length tests.
21. Lines 112–113, list `+`: evaluates both operands and calls `plus`. Sound for
    the returned pair concatenated with the recursive result.
22. Line 114, unary minus: evaluates then negates. Sound for literal `-1`.
23. Lines 115–116, subscript: evaluates the base and delegates the index syntax.
    Sound for the three exact index forms used.
24. Line 119, `makePair(pInt(I),pInt(J))`: constructs `[I,J]`. Sound.
25. Line 122, `apply("len",pList(L),_)`: returns `length(L)`. Sound for the
    unshadowed builtin in the fixed program.
26. Line 123, `apply("sorted",pList(L),_)`: returns insertion-sorted `L`. Sound
    for the unshadowed builtin on integer lists.
27. Lines 124–125, other `apply`: calls a program-defined function. The guard is
    disjoint from rules 25–26 and selects `strange_sorted` in the fixed program.
    Scope gap, not an intended-domain unsoundness: a broader Python language
    would resolve names through bindings and allow builtin shadowing.
28. Line 128, `equal(pInt(I),pInt(J))`: mathematical integer equality. Sound.
29. Line 131, list `plus`: persistent append. Sound for Python list value
    equality; object identity is unmodeled and not observable in this program.
30. Line 134, integer negation: `0 -Int I`. Sound.
31. Line 137, nonnegative direct index: `nth(L,I)`. Sound for the used `I=0`.
    The rule is partial rather than false for unsupported negative/out-of-range
    direct indices because `nth` then remains stuck.
32. Lines 138–139, syntactic negative index: uses `length(L)-I`. Sound for the
    used `I=1` and a nonempty list. Unsupported out-of-range cases become stuck.
33. Lines 140–141, exact slice `[1:-1]`: returns `interior(L)`. Sound for every
    integer list.

Expression rules have disjoint outer constructors. `apply` guards are disjoint,
and the three `index` patterns are syntactically disjoint for the submitted
forms.

### Mathematical list operations (semantic rules 34–49)

34. Line 145, `length(nil)=0`; and
35. Line 146, `length(cons(_,L))=1+length(L)`: disjoint, exhaustive, descending,
    and mathematically sound.
36. Line 149, `nth(cons(I,_),0)=I`; and
37. Line 150, `nth(cons(_,L),N)=nth(L,N-1)` for `N>0`: disjoint and descending.
    They are sound where defined; empty/negative/out-of-range indices are
    intentionally uncovered and no `[total]` claim is made.
38. Line 153, `append(nil,L2)=L2`; and
39. Line 154, `append(cons(I,L1),L2)=cons(I,append(L1,L2))`: disjoint,
    exhaustive, descending, and sound.
40. Line 157, `dropLast(nil)=nil`;
41. Line 158, `dropLast(cons(_,nil))=nil`; and
42. Line 159, recursive length-at-least-two case: disjoint, exhaustive,
    descending, and sound.
43. Line 162, `interior(nil)=nil`; and
44. Line 163, `interior(cons(_,L))=dropLast(L)`: disjoint, exhaustive, and
    exactly remove the first and last elements.
45. Line 166, `sortInts(nil)=nil`; and
46. Line 167, recursive insertion sort: disjoint, exhaustive, descending, and
    sound.
47. Line 170, insertion into empty list;
48. Line 171, insert before head when `I<=J`; and
49. Line 172, retain head and recurse when `I>J`: the guards are disjoint and
    exhaustive over mathematical integers; recursion descends. These are the
    ordinary insertion-sort equations.

### Verification rules 1–5

1. Lines 10–29, `solutionProgram => Module(...)`: a proof-local definitional
   constant, not an execution shortcut. Fresh KORE comparison in
   `10b-program-pinning-success.log` establishes equality to the submitted
   translated AST; `10c-body-sensitivity.log` shows a material body mutation
   breaks that equality.
2. Line 34, `weaveEnds(nil)=nil`.
3. Line 35, singleton `weaveEnds` returns the singleton.
4. Lines 36–38, longer `weaveEnds`: emits the head, then the last element, then
   recurses on the interior. The three patterns are disjoint and exhaustive;
   the recursive list is shorter by two. The equation is the stated
   alternating-low/high operation when its input is sorted.
5. Line 41, `strangeSpec(L)=weaveEnds(sortInts(L))`: a transparent,
   terminating definitional summary of the natural contract.

Rules 2–5 affect the postcondition but never rewrite the executing program.
There is no opaque oracle and no circular operational bridge from the program
to `strangeSpec`.

## Submitted claim inventory

- Claim 1: concrete empty input.
- Claim 2: every singleton integer list.
- Claims 3–4: every length-2 integer list, split by `A<=B` versus `A>B`.
- Claims 5–10: every length-3 integer list, split into six insertion-sort path
  conditions.
- Claims 11–34: every length-4 integer list, split into 24 insertion-sort path
  conditions.
- Claims 35–37: the three prompt examples (claim 37 duplicates claim 1).
- Claims 38–39: two concrete length-5 inputs.

The guards within each symbolic length family are disjoint and exhaustive.
`09b-claim-partitions.log` records zero uncovered assignments and zero overlaps
over a representative set containing all strict/equality order patterns for up
to four variables. This is also immediate structurally because each insertion
decision is partitioned by complementary `<=Int` and `>Int` guards.

No claim quantifies over an arbitrary `PList`, and there is no loop/recursion
invariant claim. Therefore the claim set proves no theorem for general list
length 5 and no theorem at all for length 6 or greater.
