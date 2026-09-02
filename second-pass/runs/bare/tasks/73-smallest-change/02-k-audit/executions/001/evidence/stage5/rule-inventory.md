# Exhaustive local declaration and rule inventory

Line references are to the source-only scratch copy and are also preserved in
`../stage4/formal-source-numbered.log`.

## `semantic.k`: syntax and configuration

- Lines 12-34 declare `Program` (`Module`), four K list sorts (`Stmts`,
  `Exprs`, `Strings`, `CmpOps`), three statements (`FuncDef`, `If`, `Return`),
  `Params`, `CmpOp`, and nine expressions (`Int`, `Name`, `Call`, `Compare`,
  `Subscript`, `Slice`, `UnaryOp`, `BinOp`, `NoBound`). Every constructor in
  `solution.mpy` has a declaration. There are no unused local statement forms;
  `truth` and generic `eval(BinOp(...))` are not reached by this program's
  operational rules.
- Lines 44-49 declare `<mpy>` with `<k>`, immutable `<input>`, and `<result>`.
  No environment, stack, heap, allocation, I/O, or exception cell exists.
- Lines 55-61 declare operational constructors `run`, `recur`, `finish`, and
  `addResult`; partial functions `eval`, `truth`, and `concatStmts`. None is
  declared `total`. There are no local opaque symbols and no priority rules.

## `semantic.k`: all 21 local rules

1. S1 line 63: `concatStmts(.Stmts,S2) => S2`. True empty concatenation.
2. S2 line 64: cons concatenation. True and structurally decreasing; disjoint
   from S1.
3. S3 lines 66-68: the exact one-function module initializes
   `run(BODY,L,BODY)`. It pins the parsed body and input for concrete execution,
   but no submitted proof claim starts at this `Module` configuration.
4. S4 lines 72-75: the exact `len(arr) <= 1` `If` selects `THEN` when true.
   Correct for the submitted binding and pure condition.
5. S5 lines 76-79: the same `If` selects `ELSE` when `size(L)>1`. S4/S5 are
   disjoint and exhaustive for finite lists.
6. S6 lines 80-85: the exact endpoint-equality `If` selects `THEN` when the
   projected integer endpoints are equal. Correct wherever its guard is
   defined.
7. S7 lines 86-91: the endpoint-equality `If` selects `ELSE` when unequal.
   S6/S7 are disjoint for integer endpoints. In real flow the prior length
   branch ensures both indexes are valid.
8. S8 line 93: returning an integer produces `finish(I)` and discards remaining
   statements. Correct return control for the modeled subset.
9. S9 lines 94-95: returning the exact recursive call evaluates its argument
   and creates `recur(BODY,newL,BODY)`. Correct for the submitted function,
   whose argument is the pure interior slice.
10. S10 lines 96-99: returning `Int(I) + recursive_call` recurses then installs
    `addResult(I)`. This preserves the observable order for the submitted pure
    integer left operand.
11. S11 line 102: `[concrete]` unfolds ground `recur` to `run`. It is the
    concrete recursion mechanism; it is deliberately unavailable in symbolic
    proof. It models unbounded idealized recursion and therefore omits
    CPython's recursion-limit exception.
12. S12 line 103: adds the saved integer after recursive `finish`. Correct.
13. S13 lines 104-105: consumes `finish(I)` only when result is empty and writes
    `I`. Correct for this single-call model.
14. S14 line 108: integer literal evaluation. True.
15. S15 lines 109-110: unary integer negation. True.
16. S16 lines 111-112: integer addition. True for integer operands; generic
    evaluation order/exception behavior is not modeled, but this helper is not
    used for the submitted return expression because S10 handles it.
17. S17 line 113: `len(arr)` is K list size. True for the pinned binding.
18. S18 lines 114-115: list indexing delegates to the K `LIST.get` hook,
    including negative indexes. The submitted accesses are in bounds.
19. S19 lines 116-119: generic `arr[LOW:HIGH]` becomes
    `range(L,LOW,0-HIGH)`, where K `range` removes counts from the front and
    back. This is correct for the only submitted slice `[1:-1]`, but false as
    declared for general `HIGH`. Concrete false-conclusion witness:
    `L=[0,1,2,3], LOW=1, HIGH=0`; the rule proves `[1,2,3]`, while Python
    evaluates `L[1:0]` to `[]`. See `slice-witness-proof.log` and
    `slice-witness-python.log`.
20. S20 lines 122-123: one integer `<=` comparison. True in its projected
    integer domain; unused by the hard-coded operational `If` rule.
21. S21 lines 124-125: one integer equality comparison. True in its projected
    integer domain; unused by the hard-coded operational `If` rule.

## `verification.k`: all declarations and rules

- V-declaration line 9: `minimumPalindromeChanges(List)` is `[function,total]`.
  On finite lists with integer endpoints, V1-V3 are exhaustive, disjoint, and
  decrease length by two. The `total` attribute is broader than the equations:
  K `List` can contain non-integers, and for a length-two Boolean list neither
  integer endpoint projection applies. The intended input domain is integer
  arrays, so this does not falsify an intended-domain result, but the global
  totality declaration lacks coverage.
- V1 lines 11-12: base value zero for length at most one. This is the correct
  mismatch-count base equation and a `[simplification]` rule.
- V2 lines 13-16: equal integer endpoints recurse on the interior with no
  increment. Correct mismatch-count equation and `[simplification]`.
- V3 lines 17-20: unequal integer endpoints add one and recurse on the
  interior. Correct mismatch-count equation and `[simplification]`.
- V-declaration line 24: zero-argument function symbol
  `#smallestChangeBody : Stmts`.
- V4 lines 25-38: expands that symbol to the submitted three-statement body.
  Structural inspection against `solution.mpy` finds the same AST body.

There are no priorities, `owise` rules, local axioms, macros, opaque
result-bearing symbols, or additional helper files.

## `spec.k`: all nine claims

1. C1 lines 9-13: one activation reaches `finish(0)` for length at most one.
2. C2 lines 15-21: one equal-end activation reaches an interior `recur`.
3. C3 lines 23-29: one unequal-end activation reaches an interior `recur`
   followed by `addResult(1)`.
4. C4 lines 34-35: repeats V1 and is reported trivial by `kprove`.
5. C5 lines 37-42: repeats V2 and is reported trivial.
6. C6 lines 44-49: repeats V3 and is reported trivial.
7. C7 lines 53-59: internal-body ground execution for prompt example 1.
8. C8 lines 61-67: internal-body ground execution for prompt example 2.
9. C9 lines 69-75: internal-body ground execution for prompt example 3.

C1-C3 never constrain the eventual result for lists of length greater than one.
C4-C6 concern only the separately defined mathematical function. No claim
connects `run(...)` or a full `Module(...)` execution to
`minimumPalindromeChanges(L)`, and no universal claim reaches `<result>`.
