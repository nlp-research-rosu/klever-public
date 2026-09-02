# Stage 5 static review ledger

The exhaustive machine inventory is `stage5-rule-inventory.log`: 26 K source
files (24 fixed semantics files plus `verification.k` and `spec.k`), 1,255
declaration records, 713 `rule` records (695 fixed and 18 proof-local), 236
`syntax` records, 112 declarations carrying `total`, 48 priority occurrences,
22 opaque `no-evaluators` declarations, two simplifications, and three claims.
The 24 files under `reference-semantics/` are byte-identical to the immutable trusted
SUPPLIED_SEMANTICS tree. They define the selected execution model. All
proof-local declarations and rules are below.

## Constructor-to-semantics map for `solution.mpy`

| Submitted constructor/operation | Declaration and execution rules |
|---|---|
| `Module`, statement sequencing | `syntax.k:56,61`; `core.k:124-127` |
| `FuncDef`, closure value, call frame, parameter binding, return/pop | `syntax.k:50,53`; `functions.k:8-20,62-90`; `call.k:18-21,69-74` |
| `Name` and builtin shadowing/lookup | `syntax.k:12`; `core.k:129-181` |
| `Str`, `Int`, unary minus | `syntax.k:9,13-14`; `str.k:12-17`; `core.k:193-196`; `operators.k:10`; `int.k:7` |
| `Assign`, `AugAssign`, string `+` | `syntax.k:41,44`; `controls.k:8-31`; `str.k:20-24` |
| `Call`, `Attribute`, left-to-right arguments | `syntax.k:28-29`; `core.k:183-191`; `call.k:15-32` |
| `s.split(" ")` | `methods.k:93-102` normally allocates `list(splitSep(...))`; candidate bridge `verification.k:98-105` preempts this |
| `list(word)` | `builtins.k:32-38`, including allocation |
| `sorted(...)` | `sort.k:18-37`, including allocation and trusted opaque `sortVS` |
| `"".join(...)` | `methods.k:23-31`; candidate bridge `verification.k:109-120` preempts the whole nested expression |
| `For`, list iteration, target binding | `syntax.k:45`; `controls.k:62-74,104-108`; `list.k:8-10`; `tuple.k:30-41`; candidate `wordsObj` iteration at `verification.k:93-96` |
| `Subscript(... Slice(... -1 ...))` | `syntax.k:22,38-39`; `subscript.k:43-121` |
| End-to-end loop execution | fixed loop rules above, preempted by candidate summary `verification.k:128-143` |

The cells read or modified on the real path are `<k>`, `<env>`, `<scopes>`,
`<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, and `<ret>`. `<exc>` and
`<exit-code>` remain unchanged on valid string inputs.

## Every proof-local syntax declaration

| Location | Declaration | Decision |
|---|---|---|
| `verification.k:8` | `antiLoopBody` macro | Sound exact constructor macro; mechanical comparison passes. |
| `verification.k:19` | `antiBody` macro | Sound exact constructor macro after expanding `antiLoopBody`; mechanical comparison passes. |
| `verification.k:36` | total function `sortWord` | Total definitional summary over `IntSeq`; its value depends on the fixed trusted `sortVS`. |
| `verification.k:42` | free algebra `Words` | Benign typed representation. |
| `verification.k:44` | total function `wordVals` | Total and structurally defined; dead in all submitted claims and bridges. |
| `verification.k:51` | total function `splitWords` | Total structural recursion with exhaustive, disjoint separator guards. |
| `verification.k:63` | total function `emitWordSeq` | Total structural recursion. |
| `verification.k:71` | total function `antiShuffleSpec` | Total result summary; split always yields at least one word, so the final `[:-1]` is defined on its emitted nonempty sequence. |
| `verification.k:93` | `wordsObj` subtype of `Iterable` | Benign representation by itself; connection to the fixed allocated list is not established. |

No proof-local `functional`, opaque `symbol`, or `no-evaluators` declaration
exists. The only proof-local priorities occur on the three unsound operational
bridges below. The only proof-local simplifications are the two valid list
monoid equations below.

## Every proof-local rule

| Location | Rule/class | Decision and complete reason |
|---|---|---|
| `verification.k:9-17` | `antiLoopBody` macro | Sound syntactic abbreviation. |
| `verification.k:20-31` | `antiBody` macro | Sound syntactic abbreviation. |
| `verification.k:37-38` | `sortWord` equation | Sound conditional on fixed `sortVS`; it exactly states empty-separator join of sorted one-character strings. `WORD-SPEC` proves the narrow fixed execution result. |
| `verification.k:45` | `wordVals(.Words)` | Sound base equation. |
| `verification.k:46-47` | `wordVals(wCons(...))` | Sound constructor homomorphism. |
| `verification.k:52-53` | empty `splitWords` | Sound and terminating. |
| `verification.k:54-56` | separator `splitWords` | Sound and terminating; guard `C ==Int SEP`. |
| `verification.k:57-59` | non-separator `splitWords` | Sound and terminating; complementary guard. |
| `verification.k:64` | empty `emitWordSeq` | Sound base equation. |
| `verification.k:65-66` | cons `emitWordSeq` | Sound recursive definition. |
| `verification.k:72-77` | `antiShuffleSpec` | Sound declarative construction conditional on `sortVS`. |
| `verification.k:81` | `seqConcat(A,.IntSeq) => A [simplification]` | Valid right identity derived by induction from fixed `seqConcat`; decreases size. |
| `verification.k:82-84` | associativity simplification | Valid by induction; right-associates and does not conflict with fixed left identity or right identity. |
| `verification.k:94` | empty `wordsObj` iterator | Sound representation rule. |
| `verification.k:95-96` | cons `wordsObj` iterator | Sound representation rule. |
| `verification.k:98-105` | priority-35 split operational bridge | **Unsound.** Complete match accepts an arbitrary continuation and omits `<heap>`/`<heapLoc>`. Fixed semantics returns a fresh list reference and increments the allocator. Ground fixed and extended claims prove the contradictory transitions for the same `"a b"` redex (`stage5-split-fixed.log`, `stage5-split-extended.log`). No bridge-free connection theorem exists. |
| `verification.k:109-120` | priority-40 word operational bridge | **Unsound.** It preempts callee lookup, argument evaluation, two allocations, and possible binding failures; it accepts arbitrary heap/control context. `WORD-SPEC` establishes only a value result under a narrower empty-module/builtin environment with existential final heap. Ground claims prove that fixed execution allocates locations 0 and 1 while the bridge proves the same result with an unchanged empty heap (`stage5-word-fixed.log`, `stage5-word-extended.log`). |
| `verification.k:128-143` | priority-40 loop operational bridge | **Unsound and result-smuggling.** The supporting `ANTI-LOOP-SPEC` has the exact suffix `~> Name("result")` and existentializes final scopes/heap; it does not prove an arbitrary-continuation state transformer. The bridge omits iteration target updates and allocations. With admitted suffix `~> Name("word")`, fixed loop execution yields `"ba"` while the bridge yields the stale `""` (`stage5-loop-fixed.log`, `stage5-loop-extended.log`). More seriously, changing the actually executed loop body to append `!` leaves the old universal result proof at `#Top`, although trusted concrete execution returns `ab!a` for `"ba a"` (`stage4-*body-mutation*`). |

## Claims

| Claim | Plain-language precondition and postcondition | Decision |
|---|---|---|
| `WORD-SPEC.sort-word-summary` | For any code sequence `W`, in an empty module scope with builtin names and two fresh heap locations, executing `list(W)`, `sorted`, and empty-separator `join` returns `sortWord(W)`; final heap/counter are existential. | Narrow result theorem closes under fixed semantics and is sound. It does not justify the broader word bridge's state, binding, or continuation domain. |
| `ANTI-LOOP-SPEC.anti-loop` | For any typed remaining words and result prefix in the exact three-scope frame, execute the loop and then read `result`; the read value is prefix plus emitted sorted words. Final scopes/heap/counter are existential. | Closes in the definition without the final loop summary. It constrains the read result, but does not justify an arbitrary-context state rewrite. |
| `ANTI-SHUFFLE-SPEC.anti-shuffle-correct` | From an empty initial module/heap and any `IntSeq` string input, call the exact translated closure body and return `antiShuffleSpec(S)`. | Syntactically pins the submitted body and constrains a result over an unrestricted symbolic input, but closes through the three invalid operational bridges. It is not a legitimate theorem about fixed execution. |

Concrete satisfying states appear in `stage4-ground-spec.k` and
`stage5-bridge-witnesses.k`. The input `"ba a"` satisfies the end-to-end
precondition; both trusted Python implementations return `"ab a"`, and the
ground candidate claim closes to that value. This does not rescue the
universally unsound proof theory.

## Fixed semantics and opaque inventory

All 695 fixed rules are immutable selected-semantics records and are itemized
with guards/attributes in `stage5-rule-inventory.log`. The used slice above was
checked for evaluation order, call binding, allocations, loop control, returns,
slicing, and state. Fixed declarations/rules outside that slice are
constructor-unreachable from the submitted program and do not contribute to
claim closure.

Of the 22 fixed opaque `no-evaluators` symbols inventoried, only
`sortVS(ValSeq)` is reachable here. It is an explicit supplied trusted
primitive intended to denote ascending sort; it affects every word result and
the final postcondition. The remaining 21 opaque float/keyed-sort/MD5 symbols
are unreachable. Finite Python differential evidence supports the `sortVS`
intent bridge on the recorded inputs, but is not a universal connection
theorem.
