# Used-constructor and rule map

This map was reconstructed from `solution.mpy`, `spec.k`, and the trusted
supplied semantics. The exhaustive lexical inventory is in
`stage5-rule-inventory-with-counts.log`.

| Submitted constructor / effect | Declaration | Rules reached by the theorem | Audit result |
|---|---|---|---|
| `Module`, statement sequence | `semantics/syntax.k:61`; `semantics/core.k:124` | `core.k:125-127` | Loads and executes statements left-to-right. |
| `FuncDef`, `Params` | `syntax.k:53,57`; closure values `core.k:31` | `functions.k:14-16` | Binds the literal body as a closure in module scope. |
| `Call(Name("histogram"), ...)` | `syntax.k:28`; call continuation `call.k:19` | `call.k:20-21,69-74`; `core.k:189-191`; `functions.k:63-66,85-90` | Resolves the actual binding, evaluates the argument, pushes one frame, binds `test`, and restores all call state. |
| `Name` | `syntax.k:12`; lookup continuation `core.k:130` | `core.k:131-154` | Current-frame lookup is selected for locals; module lookup selects the loaded closure. |
| `Assign(Name, value)` | `syntax.k:41` | generated strictness; `controls.k:9-11` | RHS is evaluated before the current local map is updated. Cell/reference alternatives do not match this plain frame. |
| `Int`, `Str`, empty `DictExpr` | `syntax.k:9,13,18` | `core.k:194`; `str.k:14-17`; `dict.k:26-33` | Constants and empty dictionary evaluate to the corresponding modeled values. All literals are ASCII. |
| `For` / `#loop` over `str` | `syntax.k:45`; loop continuations `controls.k:65-67`; iterator protocol `iter.k:8` | `controls.k:69-74,85`; `str.k:8-10`; `tuple.k:31-34` | Iterable is evaluated once, characters are yielded as singleton strings in order, and the name target is rebound each iteration. |
| `If` | `syntax.k:49`; branch continuation `controls.k:51` | generated strictness; `controls.k:52-54`; `core.k:199-205` | Condition is evaluated before exactly one branch; Boolean comparison results use ordinary Boolean truth. |
| `Compare` (`!=`, `==`, `>`) | `syntax.k:30,32`; contexts `operators.k:15-16` | `operators.k:17`; string cases `str.k:25-26`; integer cases `int.k:24,26` | Both operands evaluate in order; each used comparison is exact on modeled strings/integers. Heap-reference priority rules do not match. |
| `BinOp("+", count, 1)` | `syntax.k:15` with `seqstrict(2,3)` | `operators.k:12`; `int.k:9` | Left then right evaluation, followed by unbounded integer addition. |
| `Assign(Subscript(Name("result"), letter), count)` | `syntax.k:22,41`; dict continuations `dict.k:76,86` | `dict.k:71,77-81`; helpers `dict.k:37-54`; `list.k:18-20` | RHS then key evaluation; insertion/update preserves first key position and changes only the local dictionary binding. |
| `Return` | `syntax.k:50` with strict evaluation | `functions.k:78-90` | Evaluates the result, discards only the callee continuation, records it, pops the one call frame, and restores module state. |

## Proof-local extensions

| Extension | Equations | Coverage / overlap / descent | Classification |
|---|---:|---|---|
| `countHistogramCode` | `verification.k:8-16` | Empty/cons are disjoint and exhaustive; the cons case consumes one code. | Truthful total definitional summary. |
| `validHistogramInput` | `verification.k:20-23` | Empty/cons are disjoint and exhaustive; the cons case consumes one code. | Truthful total domain predicate. |
| `maxHistogramCount` | `verification.k:33-46` | Empty/cons are disjoint and exhaustive; both conditional branches consume one remaining code. | Truthful total definitional summary of the first outer loop. |
| `buildHistogram` | `verification.k:54-84` | Empty/cons are disjoint and exhaustive; every branch consumes one remaining code; dictionary helpers are the fixed-semantics helpers used by assignment. | Truthful total definitional summary of the second outer loop. |
| `histogramResult` | `verification.k:87-93` | One unconditional equation composes the two folds. | Truthful total postcondition definition. |

There are no proof-local simplification, priority, concrete, `owise`,
operational, or opaque rules. The four loop claims are fixed-semantics
reachability lemmas. Each constrains every result-bearing local used by its
caller; omitted final temporary locals are existential and are not subsequently
observed before overwrite/return.

## Imported but theorem-inert boundaries

All remaining supplied rules in `assert.k`, `bool.k`, `builtins.k`,
`comprehension.k`, `concrete.k`, `float.k`, `methods.k`, `range.k`, `set.k`,
`sort.k`, the unused portions of `list.k`, `subscript.k`, and `tuple.k` have
left-hand-side symbols absent from the entry execution and all four loop
claims. In particular, the opaque `[no-evaluators]` symbols
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes` do not
occur in the submitted term, summaries, conditions, or postcondition.
