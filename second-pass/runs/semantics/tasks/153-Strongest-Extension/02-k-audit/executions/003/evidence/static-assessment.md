# Static rule assessment

The exhaustive declaration-level inventory is `rule-inventory.tsv`. It contains
1,137 line-addressable records: 718 rules, 233 syntax declarations, five
contexts, one configuration, four claims, and all module/import/require
structure. Every record includes its source line, attributes, normalized text,
and a block hash. This note supplies the assessment for those records.

## Supplied-semantics inventory

The candidate's `reference-semantics/` is byte-for-byte and entry-for-entry
identical to the trusted mounted tree. The proof imports `MPY`, not
`MPY-CONCRETE`. The supplied rules are therefore the fixed operational
baseline, not candidate proof extensions. They were reviewed file by file as
follows:

| File | Rules | Syntax / context / config | Program-path assessment |
|---|---:|---:|---|
| `semantics.k` | 0 | assembly only | Imports the fixed proof module `MPY`; `MPY-CONCRETE` is reachable only through `MPY-KRUN`. |
| `syntax.k` | 0 | 16 syntax | Declares every submitted AST constructor. Strictness gives RHS evaluation for assignment/return/if/for and left-to-right binary evaluation. |
| `core.k` | 46 | 37 syntax + config | Used values/configuration, sequencing, lookup, literal evaluation, argument evaluation, and sequence helpers preserve the relevant state. Heap/cell cases are term-disjoint on the entry path. |
| `iter.k` | 0 | 1 syntax | Declares the iterator protocol used by both loops. |
| `range.k` | 6 | 2 syntax | Not used by the submitted program. |
| `operators.k` | 10 | 2 contexts | Generic unary/binary/comparison dispatch is used; the ref-dereference cases are not reached by the claim's unboxed list/string values. |
| `int.k` | 16 | 1 syntax | The used `+`, `-`, and `>` equations are ordinary integer arithmetic and have no overlap on the used sorts. Other operators are unused. |
| `bool.k` | 13 | 1 context | Only Boolean values/truthiness feed `If`; short-circuit rules are unused. |
| `float.k` | 121 | 34 syntax | Opaque/concrete float boundaries are unused and cannot influence this theorem. |
| `str.k` | 28 | 5 syntax | String iteration and concatenation are used and structurally correct for the `IntSeq` model. `strToCodes` accepts only ASCII literals; this becomes a source-domain adequacy defect for Python Unicode, documented below. |
| `set.k` | 12 | 6 syntax | Unused and term-disjoint. |
| `list.k` | 27 | 5 syntax | The two list iterator rules are used and preserve order; other list operations are unused. |
| `tuple.k` | 21 | 4 syntax | The `#bindTgt(Name(...), V)` rule is used by `For` and updates exactly the current scope. Tuple-specific cases are unused. |
| `subscript.k` | 40 | 15 syntax + 2 contexts | The list index-0 path is used. It selects the first element for the entry claim's nonempty three-element list. Total-but-underspecified out-of-bounds behavior is not reached by that claim, but the source implementation itself would raise on an empty list. |
| `comprehension.k` | 7 | 3 syntax | Unused by the submitted rewrite. |
| `methods.k` | 75 | 27 syntax | The used `isupper`/`islower`, `hasUpper`/`hasLower`, and ASCII range predicates agree with the supplied ASCII model. Other methods are unused. |
| `controls.k` | 34 | 3 syntax | Used assignment, integer augmented assignment, `If`, and `For` rules have the expected evaluation order and scope effects. Import/while/control-transfer/ref cases are unused. |
| `functions.k` | 15 | 4 syntax | Used parameter binding, return, and frame pop restore environment, scope and continuation. Closure-cell cases are unused. |
| `builtins.k` | 137 | 38 syntax | No builtin is called by the program. Opaque md5 and all other builtin boundaries are term-disjoint. |
| `call.k` | 21 | 3 syntax | Fixed call evaluation resolves the callee before arguments and closure calls allocate/pop a scope. This is the behavior displaced by one proof-local shortcut. |
| `sort.k` | 19 | 6 syntax | Opaque sort primitives are unused and cannot influence the theorem. |
| `assert.k` | 3 | 0 syntax | Not part of the submitted function path. |
| `dict.k` | 28 | 12 syntax | Unused and term-disjoint. |
| `concrete.k` | 16 | 5 syntax | Included only in the independently built LLVM definition, never in any proof definition. |

No supplied opaque float, sort, or digest symbol occurs in `solution.mpy`,
`verification.k`, or `spec.k`. No supplied unused rule overlaps a used
constructor/sort/operation in a way that changes the audited path.

## Construct mapping

| Submitted constructor | Declaration and operational rules |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll` and `Stmts` sequencing |
| `FuncDef`, `Params` | `syntax.k`; `functions.k` closure binding; `call.k` closure invocation |
| `Assign`, `AugAssign`, `Name` | `syntax.k`; `controls.k` assignment; `core.k` lexical lookup |
| `Int`, `Str` | `syntax.k`; `core.k` integer literal; `str.k` ASCII literal-to-code conversion |
| `For` over `str` / `list` | `controls.k`; `iter.k`; iterator cases in `str.k` and `list.k`; name target binding in `tuple.k` |
| `If` | strict syntax plus `controls.k` branch rules and `core.k` Boolean truthiness |
| `Call`, `Attribute` | `call.k` callee/argument evaluation and method dispatch |
| `isupper`, `islower` | `methods.k` predicate equations and ASCII character helpers |
| integer `+`, `-`, `>` | `operators.k` dispatch and `int.k` equations |
| `Subscript(..., 0)` | `subscript.k` evaluation contexts, list `applyIndex`, `valSeqAt` |
| string `+` | `operators.k`; `str.k` `applyBin` and `seqConcat` |
| `Return` | strict syntax; `functions.k` return/pop rules |

## Candidate function equations and declarations

The six syntax declarations at `verification.k:8-10,23,29-31,54-57,91` add
ten mathematical/body/scope symbols. There are no candidate
`[simplification]`, `[functional]`, `[concrete]`, or opaque
`[no-evaluators]` symbols.

| Lines | Extension | Assessment |
|---|---|---|
| 12-21 | `charContribution`, `strengthAcc`, `extensionStrength` | Correct recursive ASCII score; constructors are covered and recursion descends. |
| 24-26 | `lastCharacter` | Correct final-character fold, preserving the prior value for an empty suffix. |
| 33-39 | `bestExtension` | Correct stable first-maximum fold on `str` elements; guards `>` and `<=` are disjoint and exhaustive on integers. |
| 41-47 | `bestStrength` | Correct corresponding maximum strength; guards are disjoint/exhaustive. |
| 49-51 | `lastExtension` | Correct final-element fold on `str` elements. |
| 59-89 | four body equations | Mechanical macro expansion equals both regenerated function bodies; see `pinning.log`. |
| 92-100 | `solutionScope` | Correct names, parameters, bodies and definition environment for the submitted module. |

`bestExtension`, `bestStrength`, and `lastExtension` are declared `[total]`
but have no equation for a `ValSeq` whose head is not `str`. That declaration
is broader than the equations. Every use in all four claims is explicitly a
sequence of `str`, so the gap does not fabricate a value on the claimed path;
it remains a proof-theory hygiene limitation.

## Candidate operational bridges

| Line | Match / displaced behavior | Complete assessment |
|---:|---|---|
| 107 | Nonempty character `#loop` | Replaces fixed iteration/body execution with the proven score/final-character fold and preserves the continuation. The earlier character-loop claim checks the exact body and arbitrary continuation, heap and stack, but fixes particular scope identifiers/shape; no bridge-free theorem covers the raw rule's broader `L`, parent and framed cells. No false result witness was found on the entry path, so this is recorded as a context-containment evidence gap, not labeled an unsound equation. |
| 142 | `Call(Name("_extension_strength"), Name(X))` | **Unsound over its stated match domain.** It fires before callee lookup and checks only that `X` is a local string; it does not require the helper name to resolve to `solutionScope`. `spec-binding-witness.k` binds the same local name to a function returning 999. Extended semantics proves the false destination 1 (`#Top`), while fixed semantics gets stuck at 999. This shortcut contributes at the exact syntactic calls in the selection loop. |
| 156 | `#applyK` of the exact helper closure | Exact parameters, body, argument and default environment are pinned, and the earlier helper claim supports its value on the real path. The raw rule nevertheless omits the allocation freshness/state/continuation premises of the fixed call rule, so the helper claim is not a universal connection theorem for every configuration matched by this bridge. This is a context/state evidence gap; no additional false conclusion is asserted without a witness. |
| 171 | Exactly-three-element selection `#loop` | The fold equations are truthful and the prior selection claim proves the corresponding exact loop state. The rule guards module/builtin scopes, body and score relation, but omits the helper claim's fixed scope-location/ret/exc context. On the entry path those omitted cells have the claimed values. This is a context-containment evidence gap, not an unsupported unsoundness allegation. |

All four bridges have priority 40 and therefore preempt the ordinary semantics
on matches. The named-call witness is a Gate-A rule-validity failure. The other
three are result-constraining on the entry path but lack universal
bridge-free connection theorems over their complete raw match domains.

## Claims

The four claims at `spec.k:8,48,73,137` are inventoried individually in
`rule-inventory.tsv`. Their meanings are:

1. A nonempty remainder of the helper's character loop updates score by the
   recursive ASCII contribution and leaves the final character.
2. With the submitted global binding unshadowed, the helper call returns the
   ASCII strength.
3. Starting from any accumulator satisfying the score relation, an
   exactly-three-string selection loop produces the stable fold summary.
4. From fixed empty runtime state, a call with exactly three string values
   returns `class + "." + first maximum by ASCII strength`.

All preconditions are satisfiable (`pinning.log`), all four freshly reconstructed
proofs close (`reconstruction.log`), and the result is non-vacuous
(`non-vacuity.log`). The fourth claim does not cover arbitrary nonempty list
lengths, and its `IntSeq` variables are not constrained to ASCII even though
its summary uses ASCII-only predicates.
