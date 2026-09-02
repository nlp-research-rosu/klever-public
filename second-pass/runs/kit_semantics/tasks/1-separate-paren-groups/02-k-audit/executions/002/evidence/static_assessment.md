# Static soundness assessment

The exhaustive normalized source inventory is `rule_inventory.md`/`.json`
(943 sentences: 230 syntax declarations, 705 rules, 5 contexts, 1
configuration, and 2 claims). This file records the manual judgments that
accompany that mechanical inventory.

## Task-local declarations and rules

| Source | Classification | Coverage/overlap/descent | Judgment |
|---|---|---|---|
| `verification.k:8` `scanParenGroups` | Result-bearing definitional summary; `[function,total]`; not an operational bridge | Equations at lines 11 and 14 split `.IntSeq` from `iCons`; the recursive equation consumes exactly one constructor. Its nested conditions exhaust space (32), open (40), and the source program's `else` case. | Sound. It names the loop's mathematical accumulator without rewriting `<k>`. |
| `verification.k:11` empty scanner equation | Definitional equation | Disjoint from the `iCons` equation; returns the accumulated output exactly when iteration ends. | Sound. |
| `verification.k:14` nonempty scanner equation | Definitional equation | Every branch consumes `REST`. Space preserves accumulators. Nonspace appends the code to `CUR`; open adds one to depth, the source `else` subtracts one; a zero new depth appends the completed string and resets current. Nested `#if` branches are total and disjoint. | Sound over all arguments, including arbitrary integer depths and non-parenthesis codes; it mirrors the submitted body's literal `else`. |
| `verification.k:61-63` `separateParenGroupsSpec` | Definitional initializer | One unconditional equation; initializes depth/current/output to zero/empty. | Sound. |
| `verification.k:66-70` `validParenInput` | Definitional domain predicate | One unconditional equation starts the suffix predicate at depth zero. | Sound. |
| `verification.k:72` empty suffix | Definitional domain equation | Disjoint from every `iCons`; accepts exactly final depth zero. | Sound. |
| `verification.k:75` space suffix | Definitional domain equation | Code 32 is disjoint from 40, 41, and the guarded catch-all; consumes one code and preserves depth. | Sound. |
| `verification.k:78` open suffix | Definitional domain equation | Code 40 is disjoint; consumes one code and increments depth. | Sound. |
| `verification.k:81,85` close suffix | Definitional domain equations | Both require code 41. Guards `D > 0` and `D <= 0` are exhaustive and disjoint over `Int`; a legal close consumes one code and an illegal close returns false. | Sound. |
| `verification.k:89` other-code suffix | Definitional domain equation | Guard excludes 32, 40, and 41, so it is disjoint from all preceding `iCons` equations and covers every remaining code. | Sound. |

There are no task-local priority rules, simplification rules, macros, opaque
symbols, `no-evaluators` symbols, ordinary `<k>` rewrites, or trusted
primitives. The `[total]` declarations are supported by exhaustive, disjoint,
structurally descending equations.

## Claims

| Source | Classification and footprint | Judgment |
|---|---|---|
| `spec.k:6` `loop-invariant` | Derived reachability claim/circularity over the exact translated `#loop` body. It reads the current environment and exact five-variable local scope; it allows framed outer scopes/heap; it changes `char`, `current`, `depth`, and heap location `H`; it preserves allocation counters, stack, return, exception, and exit cells. Existential final scalar locals are intentionally unconstrained because only the returned group list is observable after the frame is popped. | Sound. The fixed semantics executes `#iterNext`, target binding, all source statements, and `#loopLbl` before recurrence. The summary exactly follows those steps and no operational bridge preempts them. |
| `spec.k:55` `function-correct` | Entry claim. It starts from lookup/call of the target name in a fully pinned scope, runs the exact KAST-equal closure body at defining scope 0, and constrains normal return to `ref(0)`, the allocated heap list to `separateParenGroupsSpec(S)`, allocation cells, empty stack, `noRet`, `NoExc`, and exit 0. Its only precondition is `validParenInput(S)`. | Sound and result-constraining. The complete two-claim proof closes, the false-result mutation is rejected, and concrete satisfying witnesses exist. |

## Used-construct map

| Submitted construct/effect | Supplied declaration and rules used | Static check |
|---|---|---|
| `Module`, typing import, function definition | `syntax.k:41-61`; `core.k:123-127`; `controls.k:35-44`; `functions.k:14-16` | Trusted translation is byte-identical. The target entry claim starts after installation but pins the exact binding/body. `ImportFrom("typing",...)` is a fixed-semantics no-op and is typing-only for this program. |
| Name lookup and call evaluation | `core.k:130-154,183-191`; `call.k:16-32,69-74`; `functions.k:63-66` | Lookup selects the pinned local binding before its builtin parent. Callee then the sole argument evaluate left-to-right. A new local frame is allocated, the parameter is bound, and the exact body executes. |
| Statement sequencing and literals | `core.k:123-127,193-205`; `str.k:13-17`; `syntax.k` strict attributes | Empty list/string/int initialization evaluates in source order. Intended literals are ASCII and covered by `strToCodes`. |
| List construction/allocation | `list.k:13-20`; `core.k:117-121` | Empty `ListExpr` evaluates arguments then allocates a fresh heap object at the monotone `heapLoc`. The entry state makes location 0 fresh. |
| Assignment and augmented assignment | `controls.k:9-31`; `int.k:9-16`; `str.k:20-26` | Plain-frame variables do not satisfy the higher-priority closure-cell/ref guards, so the ordinary scope update applies. String `+`, integer `+`/`-`, and equality have their ordinary mathematical meanings. |
| String iteration | `controls.k:62-74`; `iter.k:8`; `str.k:8-10`; `tuple.k:31-34` | `For` evaluates the string once. Each step yields one one-code string, binds `char`, executes the body, then recurs on the suffix. Empty suffix terminates the loop. |
| Conditions and comparisons | `syntax.k:30,49`; `operators.k:14-20`; `controls.k:50-60`; `str.k:24-26`; `int.k:22-27`; `core.k:198-205` | Operand contexts preserve evaluation order. String and integer equality/inequality reduce to Boolean values; `If` chooses exactly one branch. |
| `groups.append(current)` | `call.k:16,20-24,52-67`; `list.k:52-55`; `core.k:183-191` | Attribute cooling produces a bound method. The exact higher-priority append rule retains the reference and mutates only heap location `H`, appending the evaluated current string. |
| Return/frame cleanup | `functions.k:77-90` | Return evaluates `groups`, stores `retV(ref(H))`, pops exactly one frame, restores caller environment/scope counter, clears the frame, and resumes with the returned value. The heap allocation intentionally escapes. |
| Configuration/control observations | `core.k:44-60` | Entry and postcondition explicitly constrain all material cells: computation, environment/scopes, scope allocation, heap/allocation, stack, return, exception, and exit code. |

## Priorities, overlaps, and evaluation

- The task adds no priority rules. Relevant fixed priorities are the
  closure-cell/ref special cases and list append. Their guards are false for
  plain integer/string locals, while the append rule's exact receiver/method
  shape is true. Thus they select the Python-faithful path and do not create an
  overlap that can fabricate a result.
- `Call`'s fixed `[owise]` routing has no task-local interception. The target
  body therefore executes through ordinary callee/argument evaluation,
  closure dispatch, and method dispatch.
- `ListExpr`, `Call`, `For`, `If`, `Assign`, `AugAssign`, `Return`,
  `Attribute`, `BinOp`, and `Compare` all follow the supplied strictness,
  contexts, or explicit continuation rules. No material operation is
  unmodeled or silently replaced.
- The scanner's summary and domain equations have pairwise-disjoint
  constructor/guard cases and strict structural descent. No totality
  declaration is serving as an unconstrained oracle.

## Opaque and unused fixed-semantics boundary

The supplied proof module contains 22 explicit `no-evaluators` symbols:
`md5hexCodes`, `sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. It also contains concrete-only symbolic float helpers `floorFI`,
`toF`, and `ceilF`, partial/extensible dispatch functions, and intentionally
total abstract out-of-bounds/sorted indexing behavior.

None of those symbols is reachable from the submitted function, its summary,
its precondition, or either positive claim. `MPY-CONCRETE` is included only in
the LLVM build and is not imported by `VERIFICATION`. These are limitations of
the selected supplied language model, not task-local assumptions or
result-bearing oracles for this theorem.

The inventory found no `[simplification]` or `[functional]` sentences. It found
45 fixed-semantics priority sentences and 35 concrete sentences; every one is
listed by exact source location in the exhaustive inventory. Unused supplied
rules were checked for task-name/task-answer references and have no dependency
path from the submitted program. They remain part of the fixed-semantics trust
boundary rather than proof extensions.

No rule is labeled unsound in this audit, so no false-conclusion witness is
asserted. The narrower evidence limitation is that the fixed supplied semantics
is a deliberately partial Python model and is trusted only for the used
constructs mapped above.
