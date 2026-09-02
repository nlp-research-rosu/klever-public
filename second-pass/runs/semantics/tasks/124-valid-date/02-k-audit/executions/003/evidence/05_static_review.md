# Static review notes

The exhaustive machine-readable inventory is
`05_rule_inventory.tsv`. Its `assessment` column is the reviewer’s disposition
for every local configuration, syntax declaration, context, rule, and claim.
The trusted supplied semantics contains no simplification rules or auxiliary
claims. `verification.k` contains no `<k>` rewrite, priority rule,
simplification rule, opaque symbol, or claim: its seven equations are
definitional functions.

## Material constructor and rule map

| Program construct | Declaration | Material execution rules |
|---|---|---|
| `Module`, statement sequence | `semantics/syntax.k:56-61` | `core.k` `#loadAll`, statement-head sequencing, and `.Stmts` elimination |
| `FuncDef`, closure binding | `syntax.k:41-54`; `core.k` `closureVal` | `functions.k` plain `FuncDef`; `verification.k` exact `validDateModule`, `validDateClosure`, and `validDateBody` equations |
| `Call(Name("valid_date"), ...)` | `syntax.k:9-30` | `call.k` callee evaluation, shared left-to-right argument evaluation, plain-closure frame allocation, parameter binding, and return/pop |
| `Name` | `syntax.k:9-30` | `core.k` current-scope lookup followed by parent/builtins lookup |
| integer and Boolean literals | `syntax.k:9-30` | `core.k` literal rules |
| `len(date)` | `syntax.k` `Call` | `builtinsScope` binds `len`; `call.k` routes the builtin; `builtins.k` `applyBuiltin("len",...)`, `seqLen(str(...))`; `core.k` `isLen` |
| `ord(date[i])` | `syntax.k` `Call`, `Subscript` | `builtinsScope` binds `ord`; `subscript.k` left-to-right contexts, `normIdx`, `applyIndex(str,...)`, and `intSeqAt`; `builtins.k` singleton-string `ord` |
| `Compare` | `syntax.k:9-32` | `operators.k` left/right contexts and `applyCmp`; `int.k` exact integer `<`, `<=`, `>`, `==`, `!=` |
| `BoolOp("or",...)` | `syntax.k:9-30` | `bool.k` head-only evaluation and short-circuiting rules |
| `BinOp` `+`, `-`, `*` | `syntax.k:9-30` | `seqstrict(2,3)`, `operators.k` dispatch, and exact `int.k` arithmetic |
| `Assign(Name, ...)` | `syntax.k:41-54` | `controls.k` current-frame map update |
| `If` | `syntax.k:41-54` | strict guard evaluation plus `controls.k` `#branch` selection using `truthy(Bool)` |
| `Return` | `syntax.k:41-54` | strict result evaluation, `functions.k` `retV`, `#pop`, caller continuation and environment restoration |

For all reachable task states, subscripts occur only after `isLen(CS) == 10`;
therefore indices 0–9 are in bounds and the partial `intSeqAt` equations cover
every use. The not-length-ten branch returns before any subscript. Calls to
`ord` always receive the singleton string constructed by `applyIndex(str, I)`.
All user-defined calls use the closure installed by `#loadAll`; the module
scope is pinned at location 0 and the builtins scope at -1.

## Candidate-local equation review

| Equation | Classification and decision |
|---|---|
| `validDateBody` | Definitional summary only. Its RHS is mechanically identical to the trusted regenerated function body after normalizing the empty `Stmts` list spelling. It does not intercept execution. |
| `validDateClosure` | Definitional constructor for the same one-parameter body and defining scope 0. |
| `validDateModule` | Definitional constructor for exactly `Module(FuncDef("valid_date", Params("date"), validDateBody))`. |
| `digitCode` | Total Boolean equation `48 <= C <= 57`; one unguarded rule, no overlap. |
| `dateNumber` | Total base-10 equation for two ASCII code points; one unguarded rule. |
| `dateLimit` | Total nested conditional: 29 for month 2, 30 for 4/6/9/11, otherwise 31. |
| `validDate10` | Total conjunction exactly matching separators, eight ASCII digits, month range, positive day, and the month limit. It names the postcondition but does not replace any program computation. |

There are no proof-local operational bridges, result-bearing opaque symbols,
fresh oracles, priority rules, or assumed lemmas. All candidate equations are
single-rule unguarded definitions, so their coverage is complete and there are
no pairwise overlaps.

## Supplied-semantics boundaries and witnesses

The selected semantics is an intentionally partial Python model. Most of its
rules are unused here; the inventory marks them as such rather than treating
them as proof evidence. The broadest concrete fidelity gap is the unguarded
multi-character `int(str)` fold: under the supplied semantics, codes for
`"ab"` reduce numerically (to 540), while CPython raises `ValueError`. This is
a concrete false-behavior witness for that unused fixed rule. Unsupported
imports are also modeled as no-ops; `import definitely_missing` witnesses the
difference from CPython’s `ModuleNotFoundError`. These fixed rules cannot match
the submitted program, which uses neither `int(str)` nor imports, and no
candidate rule routes execution to them.

Other unused opaque values (`sortVS`, keyed sort, MD5, and symbolic floating
operations) are explicit supplied-semantics trust boundaries. No opaque symbol
occurs in the program path, helper formula, or postcondition. The material
rules listed above use constructor recursion and K’s ordinary integer/Boolean
theory and agree with CPython for every reachable operation in this program.
