# Stage 5 exhaustive local inventory

Scope: `/tmp/audit-work/33-sort-third/semantic.k` and
`verification.k`, copied byte-for-byte from the candidate. There are no
candidate helper `.k` files beyond these two and `spec.k`. `spec.k` adds three
reachability claims and no semantic or simplification rules.

## Imports, configuration, and local syntax

- `MPY-SYNTAX` imports `INT-SYNTAX` and `STRING-SYNTAX`.
- `SEMANTIC` imports `MPY-SYNTAX`, `INT`, and `MAP`.
- `VERIFICATION` imports `SEMANTIC`.
- Configuration: `<sort-third>` contains `<k> $PGM:Pgm </k>`,
  `<input> $INPUT:Value </input>`, and `<result> .K </result>`.

Every local syntax declaration/production is listed here:

1. `Pgm ::= Program` (subsort).
2. `Program ::= Module(Stmts)` with constructor symbol `Module`.
3. `Stmts ::= List{Stmt, ""}`.
4. `Stmt ::= FuncDef(String, Params, Stmts) | Assign(Expr, Expr) |
   Return(Expr)`, with corresponding constructor symbols.
5. `Params ::= Params(StringList)` with constructor symbol `Params`.
6. `StringList ::= List{String, ","}`.
7. `Expr ::= Name(String) | Int(Int) | Subscript(Expr, Index) |
   Call(Expr, Exprs)`, with constructor symbols `Name`, `IntExpr`,
   `Subscript`, and `Call`.
8. `Exprs ::= List{Expr, ","}`.
9. `Index ::= Expr | Slice(Bound, Bound, Bound)`, with constructor symbol
   `Slice`.
10. `Bound ::= Expr | NoBound`.
11. `Ints ::= List{Int, ","}`.
12. `Value ::= VList(Ints) | VInt(Int)`, with constructor symbols `VList`
    and `VInt`.
13. `ExecResult ::= returned(Value) | finished(Map) | exec(Stmts, Map)`.
    `returned` and `finished` are free constructors; `exec` is a function.
14. The `Value` sort is extended with functions `eval(Expr, Map)`,
    `sliceThird(Value)`, `sortedValue(Value)`, and
    `assignThird(Value, Value)`.
15. The `Ints` sort is extended with functions `thirds(Ints)`,
    `thirdsFrom(Int, Ints)`, `sortInts(Ints)`,
    `insertInt(Int, Ints)`, and
    `replaceThirdInts(Int; Ints; Ints)`.
16. `verification.k` extends `Value` with function
    `contractResult(Ints)`.

There are eleven local `[function]` symbols: `exec`, `eval`, `sliceThird`,
`sortedValue`, `assignThird`, `thirds`, `thirdsFrom`, `sortInts`,
`insertInt`, `replaceThirdInts`, and `contractResult`. There are no local
`[total]` declarations, `[functional]` declarations, `[simplification]`
rules, priority rules/attributes, `owise` rules, fresh values, or opaque
result-bearing symbols. The constructor symbols above are free data
constructors, not opaque summaries.

## Rule-by-rule inventory

| ID | Source | Exact role and domain | Static judgment |
|---|---|---|---|
| S1 | `semantic.k:65-67` | On the exact one-function module `sort_third(P)`, start `exec(BODY, P |-> ARG)` with the configured input. Reads `<input>`, rewrites `<k>`. | Sound entry-harness rule for the submitted one-function module. It omits general Python module loading/call frames, which the submitted term does not exercise. |
| S2 | `semantic.k:69-70` | Consume `returned(V)` and write `V` to an initially empty `<result>`. | Sound return delivery; preserves `<input>`. |
| S3 | `semantic.k:72-73` | `eval(Name(X), RHO)` reads an existing map key and casts it to `Value`. | Sound on reachable environments, whose entries are all `Value`; the key guard is necessary and present. |
| S4 | `semantic.k:74` | Integer AST literal evaluates to `VInt(I)`. | Ordinary truthful literal rule. The submitted `Int(3)` occurs as a slice-bound pattern and does not need general arithmetic. |
| S5 | `semantic.k:75-76` | Full slice `E[:]` evaluates to the same modeled value as `E`. | On the submitted path `E` is an integer list. Because `VList` is immutable value data and there is no reference identity, returning the same term is observationally equivalent to Python's fresh list copy here. The pattern is over-broad for other expression types: e.g. it would model `1[:]` as `1`, while Python raises `TypeError`; that program is outside this exact integer-list theorem. |
| S6 | `semantic.k:77-78` | Slice `E[::3]` becomes `sliceThird(eval(E,RHO))`. | Sound on the submitted positive literal stride and list-valued `E`; unsupported types get stuck at `sliceThird`, rather than fabricating a list. |
| S7 | `semantic.k:79-80` | The textual builtin call `sorted(E)` becomes `sortedValue(eval(E,RHO))`. | Sound for the exact source under the ordinary unshadowed Python builtin environment. General global/builtin rebinding is not modeled. |
| S8 | `semantic.k:82` | `sliceThird(VList(IS))` returns `VList(thirds(IS))`. | Truthful for positions `0,3,6,...`, subject to S15-S18. |
| S9 | `semantic.k:83` | `sortedValue(VList(IS))` returns `VList(sortInts(IS))`. | Truthful ascending integer sorting, subject to S19-S23. |
| S10 | `semantic.k:84-85` | Stride-three assignment weaves replacement list `RS` into `IS` from position zero. | Truthful when replacement length equals the count of stride-three positions. The submitted RHS is `sortInts(thirds(IS))`, which preserves exactly that length. Invalid extended-slice lengths get stuck rather than being given Python's exception state, which is unreachable here. |
| S11 | `semantic.k:87` | Empty statement list yields `finished(RHO)`. | Sound as a terminal marker. No rule consumes `finished`; a no-return module therefore stops visibly, which is unused by the submitted returning body. |
| S12 | `semantic.k:88-89` | Name assignment evaluates RHS in the old environment, then updates the name before executing the rest. | Correct evaluation/update order for `result = l[:]`. |
| S13 | `semantic.k:90-95` | For `X[::3] = E`, read old `X`, evaluate `E` in old `RHO`, replace stride positions, update `X`, then continue; requires `X` bound. | Correct for the exact assignment. RHS reads `result` before the update, as Python does. |
| S14 | `semantic.k:96` | Return evaluates its expression and discards remaining statements. | Correct abrupt-return control for the submitted final statement. |
| S15 | `semantic.k:98` | `thirds(IS)` initializes countdown at 0. | Correct definition entry. |
| S16 | `semantic.k:99` | Any countdown over an empty list returns empty. | Correct base case. |
| S17 | `semantic.k:100` | At countdown 0, retain current head and reset countdown to 2. | Selects index 0 and then skips exactly two elements before the next selection. |
| S18 | `semantic.k:101-102` | At positive countdown, discard one head and decrement. | Correct and strictly descending for reachable countdowns 2 and 1. It intentionally has no negative-count case. |
| S19 | `semantic.k:104` | Sorting the empty integer list returns empty. | Correct base case. |
| S20 | `semantic.k:105` | Sort a nonempty list by sorting its tail and inserting its head. | Standard structurally descending insertion sort. |
| S21 | `semantic.k:106` | Insert into empty list yields singleton. | Correct base case. |
| S22 | `semantic.k:107-108` | If `I <= J`, insert `I` before sorted head `J`. | Correct; guard is disjoint from S23 and preserves ascending order. |
| S23 | `semantic.k:109-110` | If `I > J`, retain `J` and recurse into the tail. | Correct; guard is disjoint from S22, exhaustive over mathematical integers, and structurally descends. |
| S24 | `semantic.k:112` | With both source and replacement lists empty, return empty, regardless of countdown. | Correct base case. |
| S25 | `semantic.k:113-114` | At countdown 0 with nonempty source/replacement, emit replacement head and reset to 2. | Correct stride replacement. |
| S26 | `semantic.k:115-117` | At positive countdown with nonempty source, emit source head and decrement; replacement list is preserved. | Correct and descending for reachable countdowns. |
| V1 | `verification.k:10-11` | `contractResult(IS)` is `VList(replaceThirdInts(0; IS; sortInts(thirds(IS))))`. | Truthful definitional specification: extract positions divisible by 3, insertion-sort those values, and weave them back. It does not rewrite or bypass the program body. |

## Coverage and interaction checks

The submitted term uses `Module`, `FuncDef`, `Params`, statement-list
juxtaposition, both `Assign` forms, `Return`, `Name`, `Int`, `Subscript`,
`Slice`, `NoBound`, and `Call`. Its path is:

`S1 -> S12 -> (S5,S3) -> S13 -> (S7,S6,S3,S8,S15-S18,S9,S19-S23,S10,S24-S26) -> S14 -> S3 -> S2`.

Thus every construct in `solution.mpy` has a declaration and a reachable rule.
`VInt` evaluation and `finished` are declared but not exercised. Missing
semantics for other translator constructs is permitted in generated-semantics
mode and fails at parsing rather than silently fabricating execution.

Local rule overlap is benign:

- S5/S6 have distinct slice-bound syntax.
- S12/S13 and S11/S14 have distinct statement heads.
- S16 versus S17/S18, S19 versus S20, and S21 versus S22/S23 are separated
  by empty/nonempty list structure.
- S17 versus S18 and S25 versus S26 are separated by `N = 0` versus `N > 0`.
- S22 and S23 use disjoint, exhaustive integer guards.
- S24 requires both lists empty; S25 requires both nonempty; S26 requires a
  nonempty source and positive countdown.

No local rule has a priority capable of preempting another. Every recursive
path used by the exact program decreases a finite list or a countdown. The
only partial cases are unsupported or erroneous programs/types, and no
`[total]` attribute claims otherwise.

The imported `INT` comparison/arithmetic and `MAP` lookup/update operations
are the low-level K trust boundary. The Python bridge assumes finite lists of
arbitrary-precision integers, standard unshadowed `sorted`, and no observation
of list identity. Concrete K/Python comparisons in
`stage3-concrete-compare.log` exercise empty lists, stride boundaries,
duplicates/equality, both insertion branches, negatives, and very large
integers.
