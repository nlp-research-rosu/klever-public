# Exhaustive local K rule review

Source locations below refer to the immutable candidate sources copied to
`/tmp/audit-work/candidate-src`. The raw declaration extraction is in
`05_inventory.log`.

## `semantic.k`: syntax and configuration

- Lines 8–12 define `Program`, whitespace-separated statement lists, parameter
  and string lists, and expression lists. These representations match every
  translated list form in `solution.mpy`.
- Lines 14–19 define all six used statement constructors: function definition,
  assignment, while, if, expression statement, and return.
- Lines 21–29 define all eight used expression constructors plus comparison
  operators: integer, name, binary operation, comparison, subscript, call,
  attribute, and list construction.
- Lines 40–46 define integer/boolean/list/None values, their injection into
  expressions, stored functions, and the optional result.
- Lines 48–62 define 15 internal continuation items. Each appears in the rule
  pairs reviewed below; none is opaque.
- Lines 64 and 68 declare the only semantic functions, `listLength` and
  `getVal`. Neither is marked `total`; their equations are disjoint.
- Lines 73–79 define exactly four cells: computation, environment, function
  table, and return result. Every non-`k` cell is used. The initial computation
  parses the actual program before the entry-driver `start`.

No local declaration has `total`, `functional`, `simplification`, `concrete`,
`priority`, `owise`, `macro`, `alias`, `trusted`, `opaque`, `strict`, or
`seqstrict`. Evaluation order is explicit in continuation rules.

## `semantic.k`: all 42 rules

| # | Lines | Rule role | Static judgment |
|---:|---:|---|---|
| 1 | 65 | `listLength(.List)=0` | True list base equation. |
| 2 | 66 | `listLength(ListItem(_) REST)=1+listLength(REST)` | True structural recursion; strictly descends. |
| 3 | 69 | `getVal(ListItem(V) _,0)=V` | Correct zero-index base case. |
| 4 | 70–71 | positive-index `getVal` recursion | Correct for positive in-bounds indices and strictly descends. It intentionally stays stuck outside that partial domain. |
| 5 | 81 | `Module(SS)` starts statement execution | Correct module sequencing for the submitted one-function module. |
| 6 | 82 | empty `exec` terminates | Correct statement-list base case. |
| 7 | 83 | `exec(S SS)` sequences head then tail | Correct left-to-right statement order. |
| 8 | 85–86 | bind `FuncDef` in `<functions>` | Correct for the submitted top-level function and preserves other entries. |
| 9 | 88–90 | entry `start` selects exact `minPath(grid,k)` binding and initializes its environment | Correct entry-driver bridge for the submitted exact parameter list. It reads the binding installed by rule 8 and does not summarize the body. |
| 10 | 92 | evaluate assignment RHS before store | Correct target evaluation order. |
| 11 | 93–94 | update named environment binding | Correct for every submitted assignment target. |
| 12 | 96 | evaluate expression statement | Correct. |
| 13 | 97 | discard expression value | Correct; only append's `None` is discarded in the target. |
| 14 | 99 | evaluate return expression | Correct. |
| 15 | 100–101 | place return value in `<result>` | Correct in the target's terminal-return context. It does not model abrupt unwinding in arbitrary programs, but no target return has a material suffix. |
| 16 | 103 | evaluate an `If` guard before selecting a branch | Correct. |
| 17 | 104 | true branch | Correct and preserves the continuation. |
| 18 | 105 | false branch | Correct and preserves the continuation. |
| 19 | 107 | evaluate a while guard | Correct. |
| 20 | 108–109 | true guard executes body then reconstructs the loop | Correct loop control and reevaluation. |
| 21 | 110 | false guard exits loop | Correct. |
| 22 | 112 | integer literal to integer value | Correct. |
| 23 | 113–114 | environment name lookup | Correct and binding-sensitive. |
| 24 | 115 | empty list construction | Correct; this is the only list literal used. |
| 25 | 117 | begin binary operation with left operand | Correct explicit left-first evaluation. |
| 26 | 118 | after left value, evaluate right operand | Correct and retains the left value. |
| 27 | 119 | integer addition | Correct on unbounded K integers and target operands. |
| 28 | 120 | integer subtraction | Correct on unbounded K integers and target operands. |
| 29 | 121 | integer multiplication | Correct on unbounded K integers and target operands. |
| 30 | 122 | integer modulo | Correct for the target's nonnegative loop index and positive divisor 2. Python/K differences outside that operand domain are unused. |
| 31 | 124 | begin comparison with left operand | Correct explicit left-first evaluation. |
| 32 | 125 | after left value, evaluate right comparison operand | Correct. |
| 33 | 126 | integer `<` | Correct. |
| 34 | 127 | integer `>` | Correct. |
| 35 | 128 | integer equality | Correct. |
| 36 | 130 | begin subscript with container | Correct Python evaluation order. |
| 37 | 131 | after container, evaluate index | Correct. |
| 38 | 132 | list subscript through `getVal` | Correct for all target accesses; valid-grid guards make them nonnegative and in bounds. Negative indexing and exceptions are intentionally unmodeled but unreachable on the intended target domain. |
| 39 | 134 | recognize one-argument builtin `len` call | Correct fixed builtin boundary for this target. The argument is still evaluated. |
| 40 | 135 | list length result | Correct by rules 1–2. |
| 41 | 137 | recognize `answer.append(argument)` and evaluate the argument | Correct for the submitted simple named receiver; receiver lookup has no target-visible side effect. |
| 42 | 138–139 | append to the bound K list and yield `None` | Correct target state change and return value. |

The 42 rules cover every material constructor and operator in `solution.mpy`.
The only deliberately partial behavior concerns unused language contexts
(out-of-bounds/negative indexing, arbitrary return suffixes, non-target calls,
and Python exceptions). No rule encodes the min-path answer, skips the
program-defined body, introduces a fresh result-bearing oracle, or fabricates a
used operation's result.

## `verification.k`: all declarations and 8 rules

- Lines 8–14 declare six proof-readable value constructors, each as a
  deterministic K function. Lines 35 and 46 add the `validTail` function and
  the `solutionProgram` program constant. There are no opaque symbols,
  priorities, simplification rules, totality declarations, or auxiliary
  reachability claims.

| # | Lines | Extension and class | Static judgment |
|---:|---:|---|---|
| 1 | 16–18 | `grid2`, definitional summary | Exact 2×2 nested `vList` constructor; truthful for all integer arguments. |
| 2 | 20–23 | `grid3`, definitional summary | Exact 3×3 nested `vList` constructor; truthful for all integer arguments. |
| 3 | 25 | `path1`, definitional summary | Defines `[1]`; the ignored display argument cannot affect execution. |
| 4 | 26–27 | `path3`, definitional summary | Defines `[1,M,1]`; exact. |
| 5 | 28–30 | `path5`, definitional summary | Defines `[1,M,1,M,1]`; exact. |
| 6 | 31–33 | `path6`, definitional summary | Defines `[1,M,1,M,1,M]`; exact. |
| 7 | 36–40 | `validTail`, definitional predicate | Exactly says that A/B/C are pairwise-distinct integers in 2..4, hence a permutation of 2,3,4. Guard equations have no overlap because there is one unconditional equation. |
| 8 | 47–122 | `solutionProgram`, definitional program expansion | Rewrites only the proof-local program constant to the exact translated constructor AST. It neither summarizes nor replaces execution. Independent `kast` comparison gives identical AST hashes, and a mutation inside this RHS changes execution and breaks the claim. |

## `spec.k`: all 11 claims

- Claims 1–3 (lines 7–28) are three ground executions: the two prompt examples
  and one longer path on the second 3×3 grid.
- Claims 4–11 (lines 33–87) are the four possible placements of `1` in a 2×2
  grid, split by the two strict orders of its two neighbors. `validTail`
  restricts the other entries to a permutation of 2,3,4. Every claim fixes
  `k=5`.
- Every claim consumes `<k>` to `.K`, fixes `<result>` to a specific list, and
  existentially frames only the final environment and function map. No result
  variable is free. The preconditions are satisfiable; `04_claim_witnesses.json`
  supplies one ground witness for each.

The claims contain no loop invariant, circularity, helper claim, implication-only
postcondition, or proof-local operational bridge. They close by finite symbolic
execution because every formal grid size and path length is fixed.

## Construct mapping and limitations

`solution.mpy` uses `Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Call`,
`While`, `Compare`, `CmpOp`, `If`, `Subscript`, `Int`, `BinOp`, `Expr`,
`Attribute`, `ListExpr`, and `Return`. These map respectively to syntax lines
8–29 and operational rules 5–42 above. Used operators are `+`, `-`, `*`, `%`,
`<`, `>`, and `==`; every one has an explicit rule.

No concrete or symbolic false-conclusion witness was found for a local rule on
the intended valid-grid domain. The model is intentionally not a reusable full
Python semantics, but generated-semantics mode permits that limitation because
all constructs and contexts actually exercised by the submitted program and
claims are covered. This rule-level soundness does not repair the separate,
material theorem-domain restriction identified in Stage 4/7.
