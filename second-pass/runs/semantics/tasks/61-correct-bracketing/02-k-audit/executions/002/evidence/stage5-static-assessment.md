# Stage 5 static assessment

This assessment is keyed to the exhaustive source inventory in
`stage5-rule-inventory.log`. That inventory contains every statement start and
source location in all 24 supplied-semantics K files, `verification.k`, and
`spec.k`; its cross-check counted 697 `rule` declarations and 228 `syntax`
declarations. There are 146 function-bearing syntax declarations, 108 marked
`total`, no `functional` declarations, 22 `no-evaluators` declarations, 45
priority-attribute occurrences, and no simplification rules.

## Per-file disposition

| File/module | Rules | Disposition after rule-by-rule review |
|---|---:|---|
| `semantics/assert.k` | 3 | Models successful and failing assertions and heap-reference truthiness. Concrete-smoke only. No false-conclusion witness found. |
| `semantics/bool.k` | 13 | Boolean comparison and short-circuit rules preserve order and returned-object identity. No false-conclusion witness found. |
| `semantics/builtins.k` | 137 | Defines the declared builtin subset and its structural folds. Partial/unmodeled exceptional cases can stick; they do not fabricate a result for this program. The opaque `md5hexCodes` trust boundary is unused here. No false-conclusion witness found on this task’s path. |
| `semantics/call.k` | 21 | Evaluates callee then arguments, dispatches by resolved value, and creates frames. These rules would be needed by a real entry claim, but the candidate claim starts after them. No false-conclusion witness found. |
| `semantics/comprehension.k` | 7 | Macro expansion only; unused. No false-conclusion witness found. |
| `semantics/concrete.k` | 16 | LLVM-only deep equality and keyed sorting. It is not imported by the Haskell proof module and is unused by this function. No false-conclusion witness found. |
| `semantics/controls.k` | 34 | Assignment, `if`, and `for/#loop` rules are the principal used rules. They update the active scope, evaluate the iterable once, bind each yielded character, sequence the body, and preserve abrupt return. The generic import/no-op and list-snapshot limitations are unused. No false-conclusion witness found on the claim domain. |
| `semantics/core.k` | 46 | Supplies the configuration, module loading, sequencing, lookup, literals, truthiness, argument evaluation, allocation, and structural helpers. The used paths are ordinary and state-preserving. Compiler-noted totality gaps are evidence limitations, not false equations, and are unused by this program. |
| `semantics/dict.k` | 28 | Ordered-dict subset; unused. Exceptional/malformed cases may stick. No false-conclusion witness found. |
| `semantics/float.k` | 121 | Float operations are mostly explicit opaque proof primitives with LLVM-only concrete twins. All are unused by the submitted function and its claim. Their existence is a broad supplied-semantics trust boundary, not a proof-local correctness shortcut for this task. |
| `semantics/functions.k` | 15 | Defines function binding, parameter binding, return, and frame pop. Return/pop is used in the loop claim; module binding/call entry is not. The documented no-escaping-closure subset is irrelevant here. No false-conclusion witness found. |
| `semantics/int.k` | 16 | Integer `+`, `-`, `<`, and `==` exactly implement the used balance operations. Other arithmetic rules are unused. No false-conclusion witness found. |
| `semantics/iter.k` | 0 | Iterator protocol declarations only. |
| `semantics/list.k` | 27 | List subset; unused by the target program. No false-conclusion witness found. |
| `semantics/methods.k` | 75 | String/list method subset; unused. No false-conclusion witness found. |
| `semantics/operators.k` | 10 | Enforces left-to-right comparison heating and dispatches used comparisons to string/integer equations. Heap-reference cases are unused. No false-conclusion witness found. |
| `semantics/range.k` | 6 | Range equations/iteration; unused. Step-zero is excluded by the range constructor rule. No false-conclusion witness found. |
| `semantics/set.k` | 12 | Set-of-character-code subset; unused. No false-conclusion witness found. |
| `semantics/sort.k` | 19 | `sortVS`/`sortKeyVS` are explicitly opaque proof primitives; unused by this target. No claim here depends on their interpretation. |
| `semantics/str.k` | 28 | String literal conversion, equality, concatenation, membership, ordering, and iteration. The used literal conversion is ASCII-safe for `""` and `"("`; string iteration yields one-character strings in order. No false-conclusion witness found on this program path. |
| `semantics/subscript.k` | 40 | Index/slice subset; unused. `valSeqAt` is total but deliberately underspecified out of bounds; no claim here observes it. |
| `semantics/syntax.k` | 0 | Sixteen syntax declarations define the constructor language. They make no semantic conclusion. |
| `semantics/tuple.k` | 21 | The used `#bindTgt(Name(...), V)` rule writes the current loop variable; tuple/list unpacking is unused. No false-conclusion witness found. |
| `semantics.k` | 0 | Assembly/import modules only. Haskell `VERIFICATION` imports `MPY`, not `MPY-CONCRETE`; LLVM `MPY-KRUN` imports both. |
| `verification.k` | 2 | `correctCodes` is a definitional summary, not an operational bridge. The empty and cons equations are disjoint, exhaustive on `IntSeq`, structurally decreasing, and match the actual loop for every code (code 40 is `"("`; every other code follows the program’s `else`). It is result-bearing but fully fixed by equations; it is not opaque and introduces no priority or simplification rule. |
| `spec.k` | 0 rules, 1 claim | The claim is a satisfiable, result-constraining circularity over an already initialized active loop frame. Its failure is adequacy/pinning: it is not a theorem from the submitted module or function entry. |

## Used-constructor mapping

| Submitted constructor | Declaration | Operational rules |
|---|---|---|
| `Module`, statement sequence | `semantics/syntax.k:61`, `:56` | `semantics/core.k:124-127` (`#loadAll`, sequencing, empty statements) |
| `FuncDef`, `Params` | `semantics/syntax.k:53`, `:57` | `semantics/functions.k:14-16` binds `closureVal` |
| `Assign` | `semantics/syntax.k:41` (`strict(2)`) | `semantics/controls.k:9-27`; ordinary active-scope write is used |
| `Name` | `semantics/syntax.k:12` | `semantics/core.k:131-154`; active/local lookup is used |
| `Int`, `Bool` | `semantics/syntax.k:9`, `:11` | `semantics/core.k:194-196` |
| `Str` | `semantics/syntax.k:13` | `semantics/str.k:13-17`; `"("` and `""` are ASCII and reduce |
| `For` | `semantics/syntax.k:45` (`strict(2)`) | `semantics/controls.k:65-74`; `semantics/str.k:7-10`; `semantics/tuple.k:31-41` |
| `If` | `semantics/syntax.k:49` (`strict(1)`) | `semantics/controls.k:51-54` |
| `Compare`, `CmpOp` | `semantics/syntax.k:30`, `:32` | `semantics/operators.k:15-17`; string `==` in `str.k:25`; integer `<`/`==` in `int.k:22-27` |
| `AugAssign` | `semantics/syntax.k:44` (`strict(3)`) | `semantics/controls.k:20-27`; integer `+`/`-` in `int.k:8-12` |
| `Return` | `semantics/syntax.k:50` (`strict`) | `semantics/functions.k:78-91` (`retV`, `#pop`, continuation/frame restoration) |

The material execution order is: lookup the iterable once; convert `For` to
`#loop`; take the next string code; bind `bracket`; compare it with `"("`;
update `balance`; compare the new balance with zero; either return `false`
abruptly or recur; on exhaustion compare final balance with zero and pop the
frame. The claim’s LHS follows this used-rule path, but it begins at `#loop` and
therefore never uses module load, function binding, parameter binding, the two
initialization statements, or function-call setup.

## Proof-extension classification

`correctCodes` is the only proof-local extension:

- Class: definitional summary.
- Match domain: all finite `IntSeq` values and all integer balances.
- State footprint: none; it is a pure function.
- Value influence: it is the entire RHS result of the loop claim.
- Coverage/overlap: `.IntSeq` and `iCons` are disjoint and exhaustive.
- Descent: the recursive rule calls only on the strict tail `R`.
- Mathematical validity: code 40 increments; any other code at balance zero
  yields `false`; otherwise it decrements; empty input returns whether balance
  is zero. These are exactly the body and early-return behavior executed by the
  fixed supplied semantics.
- Dependents: the sole `loop` claim.
- Operational bridge: none. No program term is rewritten to `correctCodes`;
  fixed semantics executes the loop, and the reachability destination names
  its result.

No proof-local opaque symbol, priority rule, totality shortcut beyond the
exhaustive recursive definition, or simplification rule exists.
