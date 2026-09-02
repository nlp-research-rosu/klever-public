# Static soundness review matrix

This matrix accompanies the exhaustive source-ordered inventory in
`k-rule-inventory.md`. The inventory contains every one of the 237 syntax
declarations, 717 rules, 45 priority rules, 117 `total` declarations, 23
`no-evaluators`/opaque declarations, six proof-local simplification rules, and
two claims from the clean source tree.

## Executed constructor-to-rule map

| Submitted MPY construct | Declaration/evaluation order | Rules exercised by the entry theorem | Review |
|---|---|---|---|
| `Module`, `FuncDef`, closure binding | `syntax.k:53,61`; `core.k:124-127`; `functions.k:14-16` | The entry claim starts after module loading with the exact binding produced by `FuncDef`. Fresh LLVM loading produced the same closure. | The omitted load step is a binding normalization, not a substituted body. Parsed KORE identity is recorded in `12-constructor-compare.log`. |
| `Call(Name("pluck"), list(INPUT))` | `syntax.k:28`; call routing is explicitly callee-first then arguments left-to-right | `core.k:131-154,185-191`; `call.k:20-21,69-75` | Binding, definition scope 0, argument value, new frame, stack continuation, and environment transition are all fixed. |
| Parameter binding and frame lifecycle | `functions.k:8-11` | `functions.k:63-66,78-90` | The parameter is bound in fresh scope 1; return sets `retV`, pops the frame, restores env/scopeLoc, removes scope 1, and retains allocated result objects. |
| Statement sequencing | `syntax.k:56` | `core.k:125-127` | Source order is preserved. |
| `Assign(Name, rhs)` | `syntax.k:41 [strict(2)]` | `controls.k:9-11` | RHS evaluates before the local scope write. Cell-write priority rule is inapplicable because the frame has no `$cells`. |
| `AugAssign(Name("index"), "+", Int(1))` | `syntax.k:44 [strict(3)]` | `controls.k:20-23`; fixed/projected integer addition | RHS evaluates first; the local binding is read and updated. Ref-special priority is inapplicable. |
| `For(Name("value"), Name("arr"), body)` | `syntax.k:45 [strict(2)]` | `controls.k:69-74`; `list.k:9-10`; `tuple.k:31-34` | Iterable expression evaluates once; each nonempty list yields the head, binds the target, executes the exact body, then resumes with the structural tail. Empty list terminates. |
| `If` | `syntax.k:49 [strict(1)]` | `controls.k:52-54`; `core.k:199-205` | Condition evaluates before the selected branch; integer/Boolean results have the expected truthiness. Ref priorities are inapplicable. |
| `Name`, `Int`, unary minus | `syntax.k:9,12,14` | `core.k:131-154,194`; `operators.k:10`; `int.k:7` | Name lookup is current-frame then parent; integer literals and `-1` have mathematical-Int meaning. |
| `BinOp("+", value, 0)` and index addition | `syntax.k:15 [seqstrict(2,3)]` | `operators.k:12`; `int.k:9`; proof-local guarded addition lemma | Left-to-right operands execute. The lemma is pure and agrees with the fixed typed rule on overlap; the bridge-free typed and casted connections close in `19-projection-typed-connection-proof.log`. |
| `BinOp("%", value, 2)` | same `BinOp` ordering | `operators.k:12`; `int.k:15,19-20` | `pyMod` is Python's floored modulo; denominator is fixed nonzero 2. On nonnegative inputs this is ordinary parity. |
| Integer comparisons | `syntax.k:30,32`; explicit Compare contexts in `operators.k:15-16` | `operators.k:17`; `int.k:22-27` | Left operand then wrapped right operand evaluate; all compared values are integers. |
| `ListExpr` return values | `syntax.k:17` | `list.k:14-15`; `core.k:185-191,117-121` | Elements evaluate left-to-right and a fresh heap reference is allocated. Empty and two-element outputs are both constrained. |
| `Return` | `syntax.k:50 [strict]` | `functions.k:78-90` | The expression evaluates, then abrupt return discards the remaining function continuation and pops exactly one frame. |

## Per-file exhaustive disposition

| Source | Inventory disposition |
|---|---|
| `semantics.k` | Assembly/import declarations only. `VERIFICATION` imports `MPY`, not `MPY-CONCRETE`; the clean build confirms that module boundary. |
| `syntax.k` | All 16 syntax blocks were reviewed. The used productions and strictness attributes are mapped above. Comprehension, dict, tuple, slice, lambda, import, assert, break/continue, and unrelated expression productions are absent from the submitted term. |
| `core.k` | All 37 syntax blocks and 46 rules were reviewed. Used configuration, allocation, sequencing, lookup, argument evaluation, literals, truthiness, dispatch declarations, and sequence helpers are faithful on the claimed domain. Cell/keyword/builtin machinery is pattern-disjoint from the reachable plain frame. |
| `iter.k`, `list.k`, `tuple.k` | All declarations/rules were reviewed. Only list iterator, list constructor, and plain-name target binding are reachable. Deep equality, mutators, membership, tuple literals/unpacking/index are unreachable. |
| `controls.k` | All 34 rules were reviewed. Plain assignment, integer augmented assignment, `If`, and `For` are reachable. Import, while, loop-control, heap-ref, and closure-cell alternatives are guard/pattern-disjoint. The helper claim contains no abrupt control and therefore safely frames an arbitrary continuation. |
| `functions.k`, `call.k` | All 36 combined rules were reviewed. Plain closure call/binding/return/pop are reachable. Annotated closures, cells, builtins, types, methods, and heap-ref argument alternatives do not match. |
| `operators.k`, `int.k` | All 26 combined rules were reviewed. Unary minus, integer `+`, `%`, and integer comparisons match exactly. Heap dereference and other operator domains do not match. The only overlap added by `verification.k` is integer addition and has the same RHS after guarded projection. |
| `bool.k` | All 13 rules and five priorities were reviewed; none is reached because the program has no `BoolOp`, Boolean arithmetic, or heap-ref Boolean operand. Boolean values produced by comparisons are consumed by fixed `If` truthiness. |
| `builtins.k` | All 38 syntax blocks and 137 rules were reviewed. No builtin call appears in the submitted body. Its one opaque MD5 symbol and all folds/evaluator helpers are unreachable. |
| `float.k` | All 34 syntax blocks, 121 rules, 19 opaque declarations, and four priorities were reviewed. No `Float`, math call, conversion, or float dispatch term is reachable. Repeated mixed numeric equations have identical RHSs on overlap and do not interact with the integer-only program. |
| `str.k`, `methods.k`, `set.k` | All 38 syntax blocks and 115 rules were reviewed. No string/set/method constructor is reachable; their pure recursive helpers cannot appear spontaneously. |
| `range.k`, `sort.k`, `subscript.k` | All 23 syntax blocks and 65 rules were reviewed. No range, sorted call, subscript, or slice occurs. Opaque `sortVS`/`sortKeyVS` and total out-of-bounds abstractions are therefore outside every proof path. |
| `dict.k` | All 12 syntax blocks and 28 rules were reviewed. No dict constructor, method, index, or write occurs. |
| `comprehension.k` | All three macro syntax blocks and seven macro equations were reviewed. The translator emitted no comprehension/generator term. |
| `assert.k`, `concrete.k` | `assert.k` is imported into `MPY` but no `Assert` occurs in the proof term. `concrete.k` is not imported by `MPY` and therefore contributes no proof axiom; it was used only in the separately rebuilt LLVM runtime. |

## Proof-local `verification.k` disposition

There are no `<k>`-cell rules, priorities, call interceptors, return shortcuts,
loop shortcuts, state rewrites, exception rewrites, or task-answer oracles.

| Extension/rules | Domain, overlap, totality, and result influence | Decision |
|---|---|---|
| `definedProjectInt` (one equation) | Exactly the generated `isInt` predicate on `Val`. Total and non-recursive. | Sound definition. |
| `projectIntTotal` plus `#Ceil` and four cast/collapse rules | Opaque only outside the integer sort. On the accepted domain, `allNonNegative` supplies `definedProjectInt`; the guarded cast, static-Int collapse, and idempotence agree. The two orientations use concrete/symbolic attributes and do not supply conflicting values. It influences parity, comparisons, accumulators, and output. | Sound on every proof use. Typed and casted bridge-free universal connections close; wrong value 8 for input 7 is rejected. |
| Guarded `applyBin("+", Val, Int)` simplifier | Complete guard is `isInt(V)`. Its overlap with fixed `applyBin("+", Int, Int)` reduces to the identical `J +Int I`. It changes no cell or control context. | Sound derived lemma, not an operational bridge. |
| `allNonNegative` (two equations) | Empty/cons coverage is exhaustive for finite `ValSeq`; structural descent. Each cons requires an actual `Int` and value `>= 0`. | Sound domain predicate. |
| `shouldTake` (one equation) | Exact source condition: even and either negative sentinel or strictly smaller. | Sound definition. |
| `nextBest`, `nextBestIndex` (four equations) | Complementary Boolean guards; agreeing source update for every integer accumulator/value. Equal values preserve the prior index. | Sound one-step summaries. |
| `scanBest`, `scanBestIndex` (four equations) | Empty/cons coverage; each recursion consumes one `ValSeq` constructor and applies the one-step summaries. | Sound structural folds. |
| `afterIndex` (two equations) | Empty/cons coverage; consumes one constructor and increments once. | Sound loop-index fold. |
| `resultList` (two equations) | Disjoint/exhaustive `B < 0` and `B >= 0` guards. Produces `[]` or exactly `[B,J]`. | Sound output constructor. |

## Reachability claims

- `SPEC.pluck-loop` executes one real nonempty iteration before circular reuse.
  It updates only `value`, `smallest`, `smallest_index`, and `index`; `arr` and
  omitted cells are framed. Its guards establish integer/nonnegative projection
  for the current head and tail. Generalizing the stored `arr`, prior `value`,
  accumulator integers, and trailing continuation is sound because the body
  neither reads `arr` nor uses abrupt control.
- `SPEC.pluck-entry` fixes the exact closure binding, definition scope, standard
  initial module/builtin scopes, empty heap and stack, call completion, result
  allocation, heap counter, return state, exception state, and exit code. Its
  postcondition is not free: heap location 0 is exactly
  `resultList(scanBest(INPUT,...), scanBestIndex(INPUT,...))`.
