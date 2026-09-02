# Candidate-local static review

The complete machine-generated declaration index is
`stage5-rule-inventory.tsv` (707 rules, 232 syntax declarations, five
contexts, one configuration, and two claims across the supplied tree plus
candidate proof sources). No `functional` or `simplification` attributes occur.

## `verification.k`

| Lines | Extension | Class | Static decision |
|---|---|---|---|
| 8-12 | `nextDuplicates` total function and two equations | Definitional summary | Sound. Equality and disequality guards are disjoint and exhaustive on K `Int`; the results are exactly the program's increment/reset update. |
| 16-18 | `intVals` constructor and empty/cons rewrites | Definitional representation | Sound. Constructor cases are disjoint, exhaustive for finite `IntSeq`, and structurally descending. `intVals` is not opaque or a result oracle. |
| 22-27 | `#intValsNext` plus three iterator rules | Operational representation bridge | Sound. Empty produces `#iterDone`; cons yields its integer head and list-wrapped represented tail. Only `<k>` changes; all other cells are framed. These cases equal one unfolding of `intVals` followed by supplied `list.k` lines 9-10. |
| 29-39 | `scanSorted` total function and two equations | Definitional summary | Sound. Empty preserves incoming `RESULT`; cons composes descent detection, duplicate update/threshold, `prev`, and recursion on the strict tail. Constructor cases are disjoint/exhaustive and recursive descent terminates. |
| 42-46 | `nonNegativeInts` total function and two equations | Domain predicate | Sound. Empty is true; cons tests the head and recurses on the strict tail. This is exactly the finite non-negative-integer domain. |
| 54-117 | priority-40 loop bridge | Operational bridge | Sound for the actual entry claim, with an evidence limitation. It matches the exact loop body/control/callee/local state, returns `scanSorted`, removes only callee scope 1, restores env/scope allocator/stack/ret, and preserves empty heap, heap allocator, exception, exit code, module closure, and builtin scope. The base proof establishes the same transition for the exact `builtinsScope`. The rule is syntactically broader because it admits a `BUILTINREST`; the body can only read correctly pinned `isinstance` and `int`, so no false conclusion witness was found, and the actual entry state is the exact supplied `builtinsScope`. The fresh generalized proof in `stage5-prove-generalized-loop.log` stuck on symbolic map lookup and therefore does not establish the broader form. |

No candidate-local opaque symbol, `functional`, `simplification`, or
`concrete` rule exists. The only candidate-local priority rule is the loop
bridge above.

## Claims

| Claim | Static decision |
|---|---|
| `SPEC.loop-invariant` | Satisfiable (e.g. the state after the first element of `[0,0]`), result-constraining, exact loop/body/control state, and machine-proved against the definition that lacks the entry bridge. |
| `SPEC.is-sorted` | Satisfiable (empty input), parser-level identical program load, named call through the loaded closure, result fixed to `scanSorted(true,-1,0,INPUT)`, and domain fixed by `nonNegativeInts(INPUT)`. |

## Used supplied-semantics path

| Program construct | Declaration / operational rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statements/expressions | `syntax.k` lines 9-61 |
| configuration and module/statement loading | `core.k` lines 44-60 and 123-127 |
| integer/Boolean literals and unary minus | `core.k` lines 193-196; `operators.k` line 10; `int.k` line 7 |
| names and builtin fallback | `core.k` lines 129-181 |
| assignment and augmented assignment | `controls.k` lines 8-31; `int.k` line 9 |
| `if` control and Boolean truth | `controls.k` lines 50-54; `core.k` lines 198-205 |
| integer `<`, `==`, `>` comparisons | `operators.k` lines 14-17; `int.k` lines 22-27 |
| call evaluation/binding/return | `call.k` lines 18-32 and 69-74; `core.k` lines 183-191; `functions.k` lines 13-20, 62-90 |
| `isinstance(value, int)` | `builtins.k` lines 287-297, reached through ordinary lookup/call dispatch |
| `for` loop and target binding | `controls.k` lines 62-74; `tuple.k` lines 30-41 |
| list iteration | `list.k` lines 8-10 plus candidate's exact `intVals` representation bridge |

The used rules preserve left-to-right call arguments, strict RHS evaluation,
callee lookup, local binding, loop sequencing, and frame return/pop state. The
input is a read-only bare algebraic list, so no heap allocation or mutation is
on the proof path. The opaque float, digest, and sorting primitives indexed in
`stage5-rule-inventory.tsv` have no matching construct in `solution.mpy`; none
can affect control or the returned result here.
