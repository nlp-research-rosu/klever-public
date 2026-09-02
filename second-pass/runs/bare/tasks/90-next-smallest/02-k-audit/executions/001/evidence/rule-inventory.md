# Reviewer rule inventory

Source hashes and line-numbered sources are in `provenance.log` and
`static-inventory.log`. There are no generated helper K source files beyond
`semantic.k`; candidate `*-kompiled/` trees are compiled output and were not
trusted or copied.

## Local syntax and state

| Location | Declaration | Audit classification |
|---|---|---|
| `semantic.k:7` | `Program ::= Module(Stmts)` | Exact top-level constructor used by `solution.mpy`. |
| `semantic.k:8` | `Stmts ::= List{Stmt,""}` | Statement sequence; actual body has two statements. |
| `semantic.k:9-11` | `Stmt ::= FuncDef(String,Params,Stmts) \| Assign(Expr,Expr) \| Return(Expr)` | Exactly the three statement forms used. |
| `semantic.k:12` | `Params ::= Params(String)` | Exactly the one-parameter form used. |
| `semantic.k:13-19` | `Expr ::= Name \| Int \| NoneVal \| Call \| Compare \| Subscript \| IfExp` | Covers every and only relevant submitted expression constructor. |
| `semantic.k:20` | `CmpOp ::= CmpOp(String,Expr)` | Covers the submitted single `>` comparison. |
| `semantic.k:24-25` | `IntList ::= nil \| cons(Int,IntList)` | Formal domain: every finite list of mathematical integers. |
| `semantic.k:33-40` | `PyVal ::= Int \| Bool \| none \| pyList \| pySet \| invalidIndex \| iteVal`; `itemAt` function | Value domain. `invalidIndex` is a sentinel, not a Python exception. `itemAt` is declared `[function,total]`. |
| `semantic.k:42` | `Outcome ::= noResult \| PyVal` | Initialization/result carrier. |
| `semantic.k:44-58` | `KItem` control constructors | Internal sequencing frames for statements, calls, comparison, indexing, and the conditional. |
| `semantic.k:60-66` | `<mpy><k><input><distinct><result>` configuration | Minimal state for this exact program; no heap, output, or exception cell exists. |
| `semantic.k:124-125` | `uniqueSort`, `insertUnique` `[function,total]` | Ground recursive definitions of sorted duplicate elimination. |
| `semantic.k:136` | `lenInt` `[function,total]` | Ground recursive list length. |
| `verification.k:8` | `secondSmallest` `[function,total]` | Proof-local definitional name for the exact conditional result term. |

No local symbol is declared `[functional]` or `[simplification]`; there are no
priority, `owise`, or local opaque declarations.

## Ordinary operational rules

| Rules | Role and decision |
|---|---|
| `semantic.k:70-71` | Harness rule invokes the exact sole `next_smallest(lst)` body using `<input>`. Sound for the submitted module; it is not a general Python module/call semantics. |
| `semantic.k:73-74` | Empty/left-to-right statement execution. Sound for the submitted two-statement body. |
| `semantic.k:76-79` | Evaluate and assign the sole local `distinct`. Sound and preserves other cells. |
| `semantic.k:81-83` | Evaluate the final return expression and set `<result>`. Sound for a final return; it would not model abrupt return before later statements. |
| `semantic.k:85-90` | Look up `lst`/`distinct`, and evaluate integer/None literals. Exact for used bindings and literals. |
| `semantic.k:92-98` | One-argument `set`, `sorted`, and `len` call frames. `set` keeps the source sequence inside `pySet`; the following `sorted` applies `uniqueSort`, so the used composition has the intended result. |
| `semantic.k:100-104` | Left-to-right single comparison and `>` for integers. The operand bookkeeping computes left `>Int` right. |
| `semantic.k:106-110` | Left-to-right base/index evaluation and `itemAt`. Correct for the fixed nonnegative index 1 when in range. |
| `semantic.k:115-121` | Eagerly evaluate condition, then branch, else branch, and build `iteVal`. This is not Python short-circuit evaluation. For this submitted program the branches are state-free and terminating in this semantics, so the selected final value agrees on the intended integer-list domain; however, the empty/singleton case speculatively evaluates an out-of-range subscript. |
| `semantic.k:152-153` | Concrete `iteVal(true/false)` selection. Guards are disjoint and exhaustive over ground Bool. Module-level `[concrete]` keeps symbolic proof terms unsplit. |

## Function equations and proof-local rule

| Rules | Coverage, overlap, descent, and decision |
|---|---|
| `semantic.k:126-127` | `uniqueSort` covers `nil`/`cons`; cons recursion strictly shortens the list. |
| `semantic.k:128-134` | `insertUnique` covers nil and all integer trichotomy cases. `<`, `==`, `>` guards are disjoint; recursion strictly shortens the sorted tail. Equations implement ascending insertion with duplicate elimination. |
| `semantic.k:137-138` | `lenInt` covers nil/cons and strictly descends. |
| `semantic.k:140-143` | `itemAt` handles index zero, positive descent, and exhaustion via `invalidIndex`. Its `[total]` declaration is over-broad: a nonempty list with a negative index matches no rule, and Python negative indexing is not modeled. The submitted program uses only index 1. Returning `invalidIndex` on exhaustion also replaces Python `IndexError`; that result is hidden by the eager conditional on exactly the empty/singleton submitted executions. |
| `verification.k:9-12` | Unconditional definition of `secondSmallest(L)` as `iteVal(lenInt(uniqueSort(L)) > 1, itemAt(uniqueSort(L),1), none)`. It is total by definition and does not bypass execution. It is not an independent theorem that `uniqueSort` has the human-facing sorted-set meaning. |

All helper equations except `secondSmallest` and the two concrete `iteVal`
rules carry `[concrete]`; no equation carries `[simplification]`. There are 40
rules in `semantic.k`, one rule in `verification.k`, and one entry claim in
`spec.k`.
