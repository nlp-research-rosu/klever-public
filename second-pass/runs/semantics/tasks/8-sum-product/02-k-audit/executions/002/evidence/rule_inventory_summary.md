# Static inventory summary

The exact rule-head and special-attribute inventory is reproducible with
`bash /audit-output/evidence/inventory_rule_heads.sh`. Across supplied semantics,
candidate verification, and candidate specs there are 234 syntax-declaration
heads, 707 rule heads, five explicit contexts, one configuration, and two
claims. Continuation alternatives on a syntax head remain on that head and were
reviewed from the complete source.

| Source | Syntax | Rules | Contexts | Config | Claims | Audit disposition |
|---|---:|---:|---:|---:|---:|---|
| `semantics.k` | 0 | 0 | 0 | 0 | 0 | Assembly only; `MPY` is the proof import and `MPY-KRUN` adds concrete-only rules. |
| `assert.k` | 0 | 3 | 0 | 0 | 0 | Assertion success/failure/deref; used only by concrete regression tests. |
| `bool.k` | 0 | 13 | 1 | 0 | 0 | Boolean operators and short-circuiting; unused by the target proof. |
| `builtins.k` | 38 | 137 | 0 | 0 | 0 | Builtin registry operations/folds and helper functions; target only depends on the builtins-scope value through configuration, not a builtin call. |
| `call.k` | 3 | 21 | 0 | 0 | 0 | Callee/argument routing, dereference, closure-call frames; ordinary closure route is used. |
| `comprehension.k` | 3 | 7 | 0 | 0 | 0 | Macro expansion; unused. |
| `concrete.k` | 5 | 16 | 0 | 0 | 0 | LLVM-only deep equality/keyed-sort rules; unused by proof and target. |
| `controls.k` | 3 | 34 | 0 | 0 | 0 | Assignment, augmented assignment, import, expression discard, and for-loop rules are used; remaining branch/while/control rules are inert. |
| `core.k` | 37 | 46 | 0 | 1 | 0 | Values/configuration, sequencing, lookup, argument evaluation, literals, and helpers; used portions preserve evaluation order and state. |
| `dict.k` | 12 | 28 | 0 | 0 | 0 | Unused. |
| `float.k` | 34 | 121 | 0 | 0 | 0 | Float primitives/opaque proof symbols; unused because all target values are `Int`. |
| `functions.k` | 4 | 15 | 0 | 0 | 0 | Definition, parameter binding, return, and frame pop are used and preserve caller continuation/state. |
| `int.k` | 1 | 16 | 0 | 0 | 0 | Integer `+` and `*` rules used; exact mathematical operations. |
| `iter.k` | 1 | 0 | 0 | 0 | 0 | Iterator protocol declarations only. |
| `list.k` | 5 | 27 | 0 | 0 | 0 | Fixed `.ValSeq`/`vCons` iterator rules are material; they do not match candidate `intVals`. Other list rules are unused. |
| `methods.k` | 27 | 75 | 0 | 0 | 0 | Unused. |
| `operators.k` | 0 | 10 | 2 | 0 | 0 | Generic operator dispatch is bypassed for `AugAssign`, whose control rule calls `applyBin` directly; other rules unused. |
| `range.k` | 2 | 6 | 0 | 0 | 0 | Unused. |
| `set.k` | 6 | 12 | 0 | 0 | 0 | Unused. |
| `sort.k` | 6 | 19 | 0 | 0 | 0 | Opaque sort trust boundary; unused. |
| `str.k` | 5 | 28 | 0 | 0 | 0 | The concrete docstring literal evaluates and is discarded; other string rules unused. |
| `subscript.k` | 15 | 40 | 2 | 0 | 0 | Unused. |
| `syntax.k` | 16 | 0 | 0 | 0 | 0 | Declares all translated constructors and strictness; target mapping is detailed in `REVIEW.md`. |
| `tuple.k` | 4 | 21 | 0 | 0 | 0 | Tuple construction and loop-target binding are used. |
| `verification.k` | 7 | 12 | 0 | 0 | 0 | Three exact program macros; opaque `intVals`; two iterator bridges; six truthful fold equations; one staged loop-summary rule. |
| `spec.k` | 0 | 0 | 0 | 0 | 2 | General loop and end-to-end reachability claims. |

There are no `functional`, `simplification`, or `anywhere` declarations in the
inventoried sources. Candidate priorities consist only of the staged loop rule
at priority 40; candidate macros are the three program-term abbreviations.
Candidate `total` functions are `intSeqSumFrom`, `intSeqProductFrom`, and
`lastInt`, each with disjoint empty/cons cases and strict structural descent.

Fixed opaque/empirical primitives are confined to float operations in
`float.k`, `sortVS`/`sortKeyVS` in `sort.k`, and `md5hexCodes` in `builtins.k`;
none occurs in either target claim's execution path. The proof-local opaque
constructor `intVals(IntSeq)` is material and is reviewed separately because it
has no defining equation to the fixed `.ValSeq`/`vCons` representation.
