# Used-construct and proof-extension map

This map supplements the exhaustive row-level inventory and assessment. The
fixed tree is byte-identical to the launcher-supplied semantics; entries here
are the material path for this submitted constructor term.

## Material source constructor map

| Submitted construct | Declaration | Material fixed behavior |
|---|---|---|
| `Module`, `Stmts` | `syntax.k`; `core.k:124` | `core.k:125-127` loads and sequences every statement. |
| `ImportFrom("typing","List")` | `syntax.k` | `controls.k:36` treats this typing-only import as a no-op. The name `List` is never evaluated. |
| `FuncDef`, `Params` | `syntax.k` | `functions.k:14-16` stores the exact body as a closure in module scope. |
| `Call(Name("concatenate"), list(VS))` | `syntax.k`; `call.k:19` | `core.k:131-154` resolves the closure; `call.k:20-21`, `core.k:189-191`, and `call.k:69-74` evaluate one argument left-to-right, allocate a frame, and enter the exact body. |
| `Assign(Name(...), Str(""))` | `syntax.k` | `str.k:14-17` evaluates the empty literal; `controls.k:9-11` writes the current local scope. |
| `For(Name("string"), Name("strings"), BODY)` | `syntax.k`; `controls.k:65` | Name lookup is `core.k:131-154`; `controls.k:69-74` evaluates the iterable once and uses the iterator protocol; `list.k:9-10` consumes exactly one `ValSeq` head per iteration; `tuple.k:31-34` binds the loop target; `controls.k:85` resumes the next iteration. |
| `AugAssign(result, "+", string)` | `syntax.k` | Strict RHS/name lookup precedes `controls.k:20-23`; fixed `str.k:24` defines string `+` by `seqConcat` (`str.k:20-22`). The proof-local simplifier is extensionally identical under its string guard. |
| `Return(Name("result"))` | `syntax.k` | Strict name lookup precedes `functions.k:78-90`, which records the value, discards only the remaining callee body, restores the caller frame and returns the value to the exact continuation. |

No used source construct reaches any fixed `[no-evaluators]` opaque symbol,
`[concrete]` rule, priority bridge, sort primitive, float primitive, hash
primitive, assertion oracle, or unmodeled result.

## Proof-local extensions

| Extension | Classification | Complete domain and overlap | State/control footprint | Value influence and justification | Dependents |
|---|---|---|---|---|---|
| `stringCodes` + equations | Definitional summary | All `Val`: exact `str(S)` case and disjoint `[owise]` non-string case. | Pure; no cells or continuation. | Affects the domain predicate and folds. On strings returns exact codes. On non-strings the fallback cannot make a non-string constructor equal `str(...)`. | All claims through `isStringSeq`, `concatFrom`, `lastFrom`. |
| `isStringSeq` + equations | Definitional predicate | Both `ValSeq` constructors, disjoint and exhaustive; recursion strictly descends. | Pure. | True iff every head has the `str` constructor. | Guards step and entry claims. |
| `concatFrom` + equations | Definitional summary | Empty or guarded string-head cons; all uses are under `isStringSeq`. | Pure. | Exact left fold of fixed `seqConcat`; directly fixes final result and loop accumulator. | Step and entry postconditions. |
| `lastFrom` + equations | Definitional summary | Empty or guarded string-head cons; recursion strictly descends. | Pure. | Exact final loop-target value (old current on empty, otherwise final head). | Step loop postcondition. |
| guarded `applyBin` `[simplification]` | Derived equation, not an operational bridge | `applyBin("+",str(A),V)` where `V ==K str(stringCodes(V))`; this domain is exactly `V=str(B)`. It overlaps fixed `str.k:24` only there and both RHSs reduce to `str(seqConcat(A,B))`. | Pure K function term; no cells, binding, allocation, exceptions, stack, or continuation. | Accelerates the fixed string-add equation without introducing a fresh/opaque result. | Inductive loop proof. |
| `concat-loop-empty` | Derived reachability lemma | Exact body/target, empty list, `env=1`, exact local keys and parent. The `...` continuation and omitted cells are universally framed by the claim itself. | Preserves every cell and the continuation; no iteration writes occur. | Fixed `#iterDone` path leaves accumulator and prior target unchanged. | Entry proof. |
| `concat-loop-step` | Derived reachability lemma | Exact body/target, nonempty string list, same exact frame; guard covers every and only string head/tail sequence. | Fixed iterator, target bind, lookup, `AugAssign`, and loop control execute; only `result` and `string` change as summarized. | Exact concatenation fold and final target; independently proved before being trusted compositionally for the entry. | Entry proof. |
| `concatenate` | Target reachability claim | All finite semantic `ValSeq` satisfying `isStringSeq`, from the exact initial configuration. | Pins return value, environment restoration, scope counter, empty heap, heap counter, stack, return state, exception state, and exit code; module binding is existentially framed. | Result is `str(concatFrom(.IntSeq,VS))`, not a fresh variable or implication. | Final theorem. |

All proof-local equations have concrete true witnesses in
`stage5-proof-local-function-tests.log`. The simplification overlap is also
covered there. The body-sensitivity residual in
`stage5-body-sensitivity.log` is `str("x")`, showing that the theorem executes
the changed body rather than an external source-independent oracle.
