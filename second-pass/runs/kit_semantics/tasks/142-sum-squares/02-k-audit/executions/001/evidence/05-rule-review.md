# Static rule review and disposition key

This document explains the per-record dispositions in
`05-k-dispositions.csv`; the complete source blocks and IDs are in
`05-k-inventory.md`. Together they enumerate all 26 K source files in scope:
235 syntax declarations, one configuration, five explicit contexts, 714
rules, and three claims. The source inventory also records every module,
import, `requires`, priority, `owise`, `total`, `function`, `symbol`,
`no-evaluators`, `concrete`, and simplification attribute.

## Supplied-semantics boundary

The proof imports `MPY`, the launcher-selected, integrity-checked supplied
semantics. `MPY-CONCRETE` is imported only by the fresh LLVM runtime build.
No candidate rule was found in the supplied tree. The candidate and trusted
trees have identical entry types, paths, and bytes.

Per-file source counts and disposition:

| File | Syntax | Rules | Review disposition |
|---|---:|---:|---|
| `semantics.k` | 0 | 0 | Assembly imports checked; `MPY` excludes `MPY-CONCRETE`. |
| `syntax.k` | 16 | 0 | Declarations/strictness attributes checked; the program uses the subset mapped below. |
| `core.k` | 37 | 46 | Configuration and material execution rules checked. |
| `iter.k` | 1 | 0 | Iterator protocol declaration checked. |
| `operators.k` | 0 | 10 | Material dispatch/evaluation rules checked. |
| `int.k` | 1 | 16 | Integer `%`, `*`, `+`, `==`, and `pyMod` checked. |
| `list.k` | 5 | 27 | The two list iterator rules are material; other heads are constructor-disjoint. |
| `tuple.k` | 4 | 21 | The simple `Name` target-binding rule is material; other heads are constructor-disjoint. |
| `controls.k` | 3 | 34 | Assignment, branch, for-loop, and loop-continuation rules checked. |
| `functions.k` | 4 | 15 | Definition, binding, return, and frame-pop rules checked. |
| `call.k` | 3 | 21 | Callee/argument evaluation and ordinary closure dispatch checked. |
| `bool.k` | 0 | 13 | Heads are absent from this program; fixed, constructor-disjoint overloads. |
| `builtins.k` | 38 | 137 | No builtin call occurs in the rewritten program; helper heads are absent. |
| `range.k` | 2 | 6 | No `rangeObj` occurs in the rewritten program. |
| `assert.k` | 0 | 3 | Used only in reviewer concrete smoke code, not in the proof definition path. |
| `comprehension.k` | 3 | 7 | No comprehension constructor occurs. |
| `dict.k` | 12 | 28 | No dict constructor/helper occurs. |
| `float.k` | 34 | 121 | No Float or float helper occurs. |
| `methods.k` | 27 | 75 | No attribute/method call occurs. |
| `set.k` | 6 | 12 | No set constructor/helper occurs. |
| `sort.k` | 6 | 19 | No `sorted` call or sort helper occurs. |
| `str.k` | 5 | 28 | No string value/operator occurs. |
| `subscript.k` | 15 | 40 | No `Subscript` occurs in the submitted rewrite. |
| `concrete.k` | 5 | 16 | Runtime-only; excluded from `VERIFICATION`. |

The fixed opaque heads (`float.k`, `sort.k`, and `md5hexCodes`) and the
compiler's non-exhaustive-totality warnings (`mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt`) are absent from the submitted constructor
term, the claims, and every proof-local summary. They cannot influence the
branch, result, heap, or control of these claims. This is a scoped semantics,
not a claim that the supplied language is complete Python.

## Constructor-to-semantics mapping

The macro-expanded submitted module uses `Module`, `FuncDef`, `Params`,
`Assign`, `Int`, `For`, `Name`, `If`, `Compare`, `CmpOp`, `BinOp`,
`AugAssign`, and `Return`, plus the statement/parameter list constructors.
The entry adds `#loadAll`, `Call`, `ref`, `list`, and `ValSeq`; the proof uses
the fixed configuration cells and frame constructors.

Material rules are:

- `core.k`: configuration; `isRefV` (used by `allInts`); module loading and
  statement sequencing at lines 125–127; lookup at 131–132 (the cell lookup is
  pruned because the frame contains no `$cells`); `builtinsScope` at 158;
  left-to-right argument evaluation at 189–191 with `appendVal` at 214–215;
  integer literal at 194; integer truth at 202; and the `applyBin`/`applyCmp`
  declarations at 208–210.
- `syntax.k`: `BinOp` is `seqstrict(2,3)`; `Assign`, `AugAssign`, `For`, `If`,
  and `Return` evaluate exactly their annotated expression positions. The two
  explicit `Compare` contexts in `operators.k` evaluate left then right.
- `call.k`: generic call at 20, cooled-callee argument route at 21, and ordinary
  `closureVal` frame creation at 69. The callee is looked up before the single
  argument is evaluated; arguments are accumulated left to right.
- `functions.k`: definition binding at 14, ordinary parameter binding at
  63–64, return at 78, and exact frame restoration/pop at 85. The return rule
  sets `retV`, discards the remaining `#endcall` suffix, and `#pop` restores the
  caller environment, scope location, stack, and returned value.
- `controls.k`: ordinary assignment at 9; ordinary `AugAssign` at 20; `If` and
  `#branch` at 52–54; `For`, `#loop`, done/yield steps at 69–73; loop
  continuation at 85; and one-time heap-reference dereference for `For` at
  106. Cell/ref special cases have false guards on the theorem's frames.
- `list.k`: empty/cons iterator steps at 9–10.
- `tuple.k`: ordinary `Name` loop-target binding at 32. Its higher-priority
  cell-target twin is pruned by the absent `$cells` marker.
- `operators.k`: `BinOp` dispatch at 12, ordered comparison contexts at 15–16,
  and comparison dispatch at 17. Ref-deref overloads are irrelevant after the
  one-time `For` dereference because each yielded element is constrained to
  `Int`.
- `int.k`: fixed `+` at 9, `*` at 14, `%` at 15, `pyMod` at 20, and `==` at
  26. The only modulus divisors are concrete nonzero 3 and 4.

This path performs the actual function binding, call, parameter bind, list
iteration, each branch and arithmetic operation, return, and frame pop. No
candidate K-cell rule skips a material operation or alters a cell.

## Candidate proof-extension rules

The 19 candidate rules and eight local syntax declarations are K1179–K1214 in
the exhaustive inventory.

1. `sumSquaresLoopBody`, `sumSquaresFunctionBody`, and `sumSquaresDef`
   (K1179–K1184) are compile-time macros. Fresh `kast --expand-macros` outputs
   for the trusted regeneration of `solution.mpy` and
   `Module(sumSquaresDef)` have the same SHA-256 and compare byte-identically.
   They are not runtime bridges.
2. `allInts` (K1185–K1187) is a structurally recursive predicate over the
   disjoint `.ValSeq`/`vCons` constructors. On cons it requires the generated
   Int-sort predicate, rejects refs redundantly, and descends to the tail.
   It covers arbitrary finite length and exactly the intended integer-element
   domain of this semantics.
3. `definedProjectInt` and `projectIntTotal` (K1188–K1197) implement a guarded
   total-projection idiom. `definedProjectInt` is exactly `isInt`; the
   `#Ceil` rule gives the existing partial Val-to-Int subsort projection that
   exact definedness domain. Both orientation rules are guarded by that
   predicate, the statically sorted Int rule is identity, and the idempotence
   rule cannot change a value. The symbol is unconstrained off-domain, but no
   result-influencing path uses it off-domain. A fresh opposite ground
   interpretation, `projectIntTotal(2) => 3`, gets stuck with actual value 2.
4. The two guarded `applyBin` simplifications (K1198–K1201) overlap the fixed
   `MPY-INT` multiplication/addition equations only when the Val operands are
   Int injections. Projection identity then makes both right sides identical
   to the fixed rule. The multiplication guard constrains both operands; the
   addition guard constrains the Val addend while the accumulator is already
   statically `Int`. They are pure derived equations, not K-cell operational
   bridges. Fresh fixed-vs-extended concrete outputs are byte-identical.
5. `squareContribution` (K1202–K1208) has three pairwise-disjoint and exhaustive
   guards: `%3 == 0`; `%3 != 0` and `%4 == 0`; or both nonzero. Its right sides
   exactly match the program's square, left-associated cube, and unchanged
   contributions. Index 12 selects the square case, as required by source
   precedence.
6. `sumSquaresAcc` (K1209–K1214) is structurally recursive on `ValSeq`. Empty
   returns the accumulator. The Int-head case increments the index and adds
   exactly `squareContribution`; its recursion strictly descends. The non-Int
   fallback totalizes the helper with the complementary guard and is
   unreachable from `allInts`.

No guards overlap with disagreeing right sides. All total functions used in
the theorem have exhaustive constructor/guard coverage. There is no
proof-local priority rule, arbitrary continuation, exception rule, allocation
rule, call shortcut, return shortcut, heap rewrite, or unconstrained
result-bearing oracle.

## Claims and cells

- `SPEC.loop-invariant` (K1218–K1219) starts at the real `#loop` term with the
  exact target and body and the exact `Return(...) ~> #endcall` continuation.
  The stack contains exactly the real call frame. The environment, scope
  location, return, exception, exit, heap, heap location, and stack
  transitions match fixed frame-pop behavior. Heap and allocation counter are
  preserved. The arbitrary final scope map is not an observable result and is
  produced only after the fixed pop.
- `SPEC.sum-squares` (K1220–K1221) loads the exact module, resolves its actual
  binding, calls it with a heap reference to an arbitrary all-Int `ValSeq`,
  permits arbitrary disjoint heap context, and preserves the heap and
  allocation counter. Its post-state K value is the accumulator summary, not a
  free result.
- `SPEC.sum-squares-bare` (K1222–K1223) is the supplied semantics' explicitly
  supported read-only bare-list representation. It is supporting evidence;
  the heap-referenced claim is the primary source-level theorem.

Satisfying witnesses exist:

- loop: `VS=.ValSeq`, `INDEX=0`, `ACC=0`, `SC=.Map`, `INPUT=list(.ValSeq)`,
  `CURRENT=0`, `HEAP=.Map`, `NEXT=0`;
- primary: `VS=.ValSeq`, `H=0`, `HEAP=.Map`, `NEXT=1`;
- bare: `VS=.ValSeq`.

The prompt examples and an index-12 common-multiple witness reduce under
`sumSquaresAcc` to 6, 0, -126, and 4, matching trusted Python and candidate
Python. A mutation that changes the actual executed constructor body
(`result=2`) reaches 2 and is rejected against the original empty-list result
0.

## Soundness decision

No materially unsound local rule was found, so there is no false-conclusion
witness to report against an inventoried rule. The observed compiler warnings
are either unused variables or non-exhaustive total helpers whose heads are
constructor-disjoint from this proof. The only result-bearing opaque local
symbol is `projectIntTotal`; its guard, subsort connection, identity rules,
fixed/extended execution comparison, and rejected opposite interpretation
make its theorem-local use constrained rather than oracle-like.
