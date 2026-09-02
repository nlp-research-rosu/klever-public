# Exhaustive static rule decision

This decision sheet covers every entry listed in
`declaration_inventory.txt`. Counts and attributes are independently summarized
in `static_inventory_summary.log`: 229 syntax declarations, 698 rules, five
contexts, one configuration, 149 function declarations, 110 `total`
annotations, 35 `concrete` rules, 45 priority attributes, 22
`no-evaluators` declarations, eight fixed/local macros, and no
`simplification`, `functional`, or proof-local claim declarations.

The supplied semantics is the fixed execution theory for this condition.
Nevertheless, every module was read for false equations, overlaps, uncontrolled
freshness, answer injection, and relevance to the submitted term. “Valid,
unused” below is a decision for every declaration/rule in that row: its
equations implement the documented MiniPy subset or define an explicitly
partial/opaque operation; none overlaps a used redex or introduces a
contradiction capable of closing these ground claims.

| File | Decision for all inventoried entries | Result/value influence in this proof |
|---|---|---|
| `semantics.k` | Import graph only; `MPY` excludes `MPY-CONCRETE` while `MPY-KRUN` adds it. No rules. | Establishes the proof/concrete boundary. |
| `syntax.k` | AST constructors and strictness/context declarations match the translated term; comprehension macros are unused. | Used constructors are mapped separately in `used_constructs.md`. |
| `core.k` | Value/configuration algebra, guarded allocation/cells, module sequencing, concrete scope-chain lookup, left-to-right argument evaluation, literals, truthiness, and structurally recursive helpers are internally consistent. Fresh allocation is guarded and monotone. | Configuration and load/lookup/evaluation rules are used. No heap allocation or cell rules are reached. |
| `iter.k`, `range.k` | Iterator declaration and guarded arithmetic range rules are structurally decreasing and disjoint on positive/negative step cases. | Unused. |
| `operators.k` | Heat/cool contexts enforce left-to-right comparison evaluation; dispatch and ref-dereference priorities are sort/guard separated. | Integer `%`, `//`, `==`, and string `+` dispatch are used; ref rules are not. |
| `int.k` | Integer arithmetic is ordinary K arithmetic; `pyMod=((a%b)+b)%b` and floor division agree with Python for nonzero divisors. Comparator cases are disjoint by operator. | Used only with positive divisors 1000, 100, and 10 and with equality to 1000. No divide-by-zero path exists. |
| `bool.k` | Truth-preserving short-circuit rules and ref priorities; alternatives are separated by `truthy`/its negation. | Unused. |
| `float.k` | Ordinary concrete IEEE operations plus explicitly opaque proof-side functions. Duplicate mixed arithmetic/conversion equations have identical RHSs. Opaque functions are not oracles for this theorem because no float term occurs in program or postcondition. | Unused named trust boundary; cannot select a branch/result here. |
| `str.k` | ASCII literal conversion, structural concatenation/equality/membership, and lexicographic recursion are disjoint and decreasing. | ASCII literal conversion and concatenation are used and reduce completely to ground `IntSeq`s. |
| `set.k` | Deduplication/membership/subset equations are exhaustive on constructor sequences and structurally decreasing. | Unused. |
| `list.k` | Constructor allocation, concatenation, equality, mutation, and membership fold preserve their documented heap/iterator effects; guarded alternatives are disjoint. | Unused; no list/ref is constructed. |
| `tuple.k` | Tuple literal evaluation is left-to-right; equality/index helpers and target-binding rules are constructor/guard separated. | Tuple construction is used; tuple target binding/methods/iteration are unused. |
| `subscript.k` | Contexts evaluate object then a non-slice index. `normIdx`, access, and slice helpers use disjoint sign/range guards and decreasing sequence recursion. `valSeqAt [total]` is under-specified outside constructor/in-bounds cases, but all reached indices are ground 0..9 into ten-element tuples, so every access reduces by the ordinary equations. | Tuple access is used and fully defined; opaque/OOB totality cannot affect any target. |
| `comprehension.k` | Syntactic desugaring only; macros expand to loops/list construction. | Unused. |
| `methods.k` | String/list methods are guarded, structurally recursive ASCII/subset implementations. Unsupported argument shapes remain stuck rather than fabricating results. | Unused. |
| `controls.k` | Assignment updates only the current concrete scope; the cell priority is guarded. `If` alternatives are exact complements. Loop/control rules preserve the loop continuation and abrupt effects. | Plain assignment and `If` are used; all cell/import/loop/ref rules are unused. |
| `functions.k` | Closure creation/binding/frame lifecycle has exact cell footprints. `Return(V) ~> _` intentionally discards the remaining callee body, stores `V`, then `#pop` restores the caller continuation/environment and removes only the callee scope. | Plain closure, one parameter, return, and pop are used. The stack is ground and constrained empty afterward. |
| `builtins.k` | Registry operations, folds, conversions, iterator constructors, and arithmetic-token helpers are constructor/guard based. `md5hexCodes` is explicitly opaque. No builtin appears in the submitted term. | Entire module unused; opaque MD5 and unsupported `eval` cases cannot influence this theorem. |
| `call.k` | Generic call evaluates callee then arguments. Callable cases are constructor separated. Plain closure call allocates one guarded concrete frame, stores the exact continuation, and delegates body execution to fixed rules. | Plain `closureVal` call rule is used. No builtin/method/type/annotated closure path is reached. |
| `sort.k` | Explicit opaque `sortVS`/`sortKeyVS` proof boundaries and concrete insertion-sort twins; reverse helpers are structurally recursive. | Entire module unused; no opaque sort term can occur in result/control/state. |
| `assert.k` | True assertion continues; false assertion discards the active computation and sets exception/exit state, modeling the subset’s abrupt failure. | Unused; target has no assertion. |
| `dict.k` | Ordered parallel-sequence implementation with guarded lookup/update/equality recursion. Malformed parallel sequences are outside the documented value invariant. | Unused. |
| `concrete.k` | LLVM-only deep equality and keyed sort execution. It is absent from `VERIFICATION` and therefore contributes no proof axiom. | Used only by the independent concrete definition, not by `kprove`. |
| `verification.k` | Exactly three syntax macro productions and their three expansion rules. Mechanical comparison proves the body/binding/call expansion is constructor-identical to trusted regeneration; compiled `allRules.txt` contains none of the macro tokens. | Selects the real body and a result-assignment harness; skips no execution and adds no value equation. |

## Used-path overlap, priority, and totality decision

The used redexes have a single effective fixed-semantics route:

- `%`/`//` receive two ground `Int`s, so float/list/string cases cannot overlap.
- subscript receives a ground `tuple` and ground in-bounds `Int`; dict/ref/slice
  routes cannot overlap.
- `Compare` receives two `Int`s and operator `"=="`; no `noneV`, float, string,
  collection, or identity route overlaps.
- `BinOp("+", str, str)` is sort-disjoint from integer/float/list cases.
- the callee is a concrete `closureVal`, not a builtin/type/method/annotated
  closure.
- assignments occur in ordinary frames without `"$cells"`, so priority cell
  writes are refuted.

All task results are therefore derived by fixed operational rules with ground
arithmetic and sequence equations. There is no proof-local operational bridge,
result-bearing abstraction, loop circularity, simplification, or answer rule.
No inventoried rule yields a false conclusion on a satisfying input in
`1..1000`; consequently there is no unsoundness witness to report.
